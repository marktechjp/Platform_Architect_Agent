import os
import glob
import sys
import argparse
import json
from langchain_google_vertexai import VertexAI
import google.auth
import re

# コーディングエージェント用のプロンプトテンプレート
CODING_AGENT_PROMPT = """
あなたは、指定された技術スタックに精通した、世界クラスのソフトウェアエンジニアです。
以下のプロジェクト概要と担当業務の設計書に基づいて、具体的なファイル名とソースコードを生成してください。

## プロジェクト概要
{project_overview}

## 担当業務の設計書
{design_document}

## 指示
- 上記の情報を基に、担当業務を遂行するために必要なソースコードを1つ生成してください。
- 以前のタスクで生成されたコードは考慮せず、この設計書で指示された単一のタスクに集中してください。
- 生成するコードは、プロジェクトの技術スタックに完全に準拠している必要があります。
- **ファイル名は、必ず `{target_path_prefix}` から始まるパスにしてください。**
- 返答は、必ず以下のJSON形式で、ファイル名とソースコードのみを出力してください。その他の説明は一切含めないでください。

```json
{{
  "file_name": "{target_path_prefix}/src/components/example.tsx",
  "source_code": "ここにソースコードを記述"
}}
```
"""

def get_llm():
    """VertexAIのLLMインスタンスを取得する"""
    try:
        project_id = "denkojobcenter"
        print(f"✅ GCPプロジェクト '{project_id}' を使用します。")
        return VertexAI(model_name="gemini-2.5-pro", temperature=0.1, project=project_id)
    except Exception as e:
        print(f"❌ VertexAIの初期化中にエラーが発生しました: {e}")
        return None

class FullAgentOrchestrator:
    def __init__(self, project_dir):
        if not os.path.isdir(project_dir):
            raise ValueError(f"指定されたディレクトリが見つかりません: {project_dir}")
        self.project_dir = project_dir
        self.llm = get_llm()
        self.project_overview = self._load_project_overview()
        # 担当エージェントと保存先ディレクトリのマッピング
        self.agent_path_map = {
            "architect": ".",
            "ui_ux_engineer": "frontend",
            "ux_ui_designer": "frontend",
            "api_data_engineer": "backend",
            "infra_cicd": ".",
            "quality_assurance": ".",
        }

    def _load_project_overview(self):
        """プロジェクト概要JSONファイルを読み込む"""
        overview_file = os.path.join(self.project_dir, "00_project_overview.json")
        if not os.path.exists(overview_file):
            raise ValueError(f"プロジェクト概要ファイルが見つかりません: {overview_file}")
        
        with open(overview_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data.get("project_overview", {}), ensure_ascii=False, indent=2)

    def execute(self):
        """統括エージェントのメイン実行フロー"""
        project_name = os.path.basename(self.project_dir)
        print(f"📂 プロジェクト '{project_name}' の処理を開始します。")
        print("-" * 50)

        if not self.llm:
            print("LLMが初期化されていないため、処理を中断します。")
            return

        design_files = sorted(glob.glob(os.path.join(self.project_dir, "*.md")))
        if not design_files:
            print(f"📂 設計書ファイル（.md）が {self.project_dir} 内に見つかりませんでした。")
            return
            
        print("📋 以下の設計書に基づいて、孫エージェントによるコーディングを開始します。")
        for design_file in design_files:
            self.process_design_file(design_file)
            
        print("-" * 50)
        print("✅ すべての設計書の処理が完了しました。")

    def process_design_file(self, file_path):
        """個別の設計書ファイルを処理し、AIにコーディングを指示する"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                design_content = f.read()
            
            base_name = os.path.basename(file_path).replace('.md', '')
            # "01_architect" から "architect" を抽出
            agent_type_key = base_name.split('_', 1)[-1] 
            
            print(f"\n🤖 孫エージェント（コーディング担当）を起動: `{base_name}`")
            
            # マッピングに基づいて保存先のプレフィックスを決定
            target_path_prefix = self.agent_path_map.get(agent_type_key, ".")
            
            prompt = CODING_AGENT_PROMPT.format(
                project_overview=self.project_overview,
                design_document=design_content,
                target_path_prefix=target_path_prefix
            )
            
            print(f"   - 担当: {agent_type_key} -> 保存先プレフィックス: '{target_path_prefix}'")
            print("   - AIにコーディングを指示中...")
            response_text = self.llm.invoke(prompt)
            print("   - AIからの応答を受信。")
            self._save_generated_code(response_text)

        except Exception as e:
            print(f"❌ ファイル処理中にエラーが発生しました ({file_path}): {e}")

    def _save_generated_code(self, response_text):
        """AIの応答からコードを抽出し、ファイルに保存する"""
        try:
            match = re.search(r"```json\s*([\s\S]+?)\s*```", response_text, re.DOTALL)
            json_str = match.group(1) if match else response_text
            data = json.loads(json_str)
            file_name = data.get("file_name")
            source_code = data.get("source_code")

            if not file_name or source_code is None:
                print("   - 応答JSONに'file_name'または'source_code'がありません。")
                return

            output_path = os.path.join(self.project_dir, file_name)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(source_code)
            print(f"   ✅ コードを保存しました: {output_path}")

        except json.JSONDecodeError:
            print(f"   - 応答のJSON形式が不正です。")
            print(f"     AIの応答: {response_text}")
        except Exception as e:
            print(f"   - コードの保存中にエラーが発生しました: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="設計書フォルダを処理して、各担当のコーディングタスクを実行するオーケストレーター")
    parser.add_argument("project_directory", help="処理対象の設計書が含まれるディレクトリのパス")
    args = parser.parse_args()

    try:
        orchestrator = FullAgentOrchestrator(args.project_directory)
        orchestrator.execute()
    except ValueError as e:
        print(f"エラー: {e}")
        sys.exit(1)
