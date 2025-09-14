import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
import google.auth
import re

# .envファイルから環境変数を読み込む (ローカル開発用)
# GCPのCloud Runで実行する際は、環境変数はCloud Runのサービス設定から読み込まれます。
load_dotenv()

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 子エージェント設計書生成用のプロンプトテンプレート
AGENT_DESIGN_PROMPT = """
あなたは経験豊富なプラットフォームアーキテクトです。以下のビジネス要件に基づいて、必要な子エージェントの設計書を生成してください。

## ビジネス要件:
{business_requirement}

## 出力形式:
以下のJSON形式で、必要な子エージェントのリストと各エージェントの設計書を出力してください：

```json
{{
  "project_overview": {{
    "name": "プロジェクト名",
    "description": "プロジェクトの概要説明",
    "technical_stack": ["使用技術1", "使用技術2", "..."],
    "estimated_timeline": "開発期間の見積もり"
  }},
  "required_agents": [
    {{
      "agent_name": "Tech Lead Agent",
      "agent_type": "tech_lead",
      "responsibility": "技術的な意思決定とアーキテクチャ設計",
      "skills": ["スキル1", "スキル2", "..."],
      "autonomy_level": "L2",
      "main_functions": ["機能1", "機能2", "..."],
      "data_sources": ["データソース1", "データソース2", "..."],
      "kpis": ["KPI1", "KPI2", "..."]
    }},
    {{
      "agent_name": "Frontend Developer Agent",
      "agent_type": "frontend_developer",
      "responsibility": "フロントエンド開発とUI/UX実装",
      "skills": ["React", "TypeScript", "CSS", "..."],
      "autonomy_level": "L2",
      "main_functions": ["UI開発", "コンポーネント設計", "..."],
      "data_sources": ["デザインシステム", "APIドキュメント", "..."],
      "kpis": ["開発速度", "品質指標", "..."]
    }}
  ]
}}
```

## 注意事項:
- 設計書は日本語で記述してください
- 各エージェントの責任範囲が重複しないよう設計してください
- 自律レベルは L1（完全自動）、L2（条件付き自動）、L3（人間の承認必要）から適切なものを選択してください
- ビジネス要件に最適な技術スタックを提案してください
"""

def save_generated_designs(design_data, timestamp, requirement):
    """生成された設計書を日付とプロジェクト名のフォルダに分かりやすく整理して保存する"""
    try:
        # --- フォルダ名の設定 ---
        date_str = datetime.now().strftime("%Y%m%d")
        project_name = design_data.get("project_overview", {}).get("name", "Unnamed_Project")
        
        # ファイル名として使えるようにプロジェクト名をサニタイズ
        # 英数字、アンダースコア、ハイフンのみを許可
        safe_project_name = re.sub(r'[^\w\-]', '_', project_name)
        
        output_dir = f"{date_str}_{safe_project_name}"
        os.makedirs(output_dir, exist_ok=True)

        # --- ファイル名のマッピング定義 ---
        agent_filename_map = {
            "tech_lead": "01_architect",
            "frontend_developer": "02_ui_ux_engineer",
            "backend_developer": "03_api_data_engineer",
            "ml_engineer": "04_ai_core_engineer",
            "devops_engineer": "05_infra_cicd",
            "qa_engineer": "06_quality_assurance",
            # 必要に応じて他の役割も追加
        }

        # --- プロジェクト概要ファイルの保存 ---
        project_file = os.path.join(output_dir, "00_project_overview.json")
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "business_requirement": requirement,
                "project_overview": design_data.get("project_overview", {}),
                "agents_count": len(design_data.get("required_agents", []))
            }, f, ensure_ascii=False, indent=2)

        # --- 各エージェントの設計書を保存 ---
        agents = design_data.get("required_agents", [])
        for i, agent in enumerate(agents):
            agent_type = agent.get("agent_type", "unknown")
            
            # マップからファイル名を取得、なければデフォルト名を作成
            base_name = agent_filename_map.get(agent_type, f"{str(i+1).zfill(2)}_{agent_type}")
            
            # 最終的なファイルパスを作成
            agent_file = os.path.join(output_dir, f"{base_name}.md")
            
            with open(agent_file, 'w', encoding='utf-8') as f:
                f.write(generate_agent_markdown(agent, timestamp, requirement))

        print(f"Generated design documents saved in '{output_dir}/'")

    except Exception as e:
        print(f"Error saving generated designs: {e}")


def generate_agent_markdown(agent_data, timestamp, requirement):
    """エージェントデータからMarkdown形式の設計書を生成する"""
    markdown = f"""# {agent_data.get('agent_name', 'Unknown Agent')}

- **バージョン**: 1.0
- **生成日時**: {timestamp}
- **元要件**: {requirement}

## 1. 目的 (Goal)
- **責任範囲**: {agent_data.get('responsibility', 'Not specified')}

## 2. 自律レベル (Autonomy Level)
- **レベル**: {agent_data.get('autonomy_level', 'L2')}

## 3. 主要機能
"""
    
    for func in agent_data.get('main_functions', []):
        markdown += f"- {func}\n"
    
    markdown += f"""
## 4. 必要スキル
"""
    
    for skill in agent_data.get('skills', []):
        markdown += f"- {skill}\n"
    
    markdown += f"""
## 5. データソース
"""
    
    for data_source in agent_data.get('data_sources', []):
        markdown += f"- {data_source}\n"
    
    markdown += f"""
## 6. KPI (Key Performance Indicators)
"""
    
    for kpi in agent_data.get('kpis', []):
        markdown += f"- {kpi}\n"
    
    markdown += f"""
---
*この設計書はPlatform Architect Agentによって自動生成されました*
"""
    
    return markdown


def get_llm(demo_mode):
    """実行モードに応じてLLMインスタンスを返す"""
    if demo_mode:
        print("🤖 MockLLM (デモモード) を使用します。")
        return MockLLM()
    else:
        print("☁️  Google VertexAI (本番モード) を使用します。")
        try:
            # GCP認証情報の確認
            credentials, project_id = google.auth.default()
            print(f"✅ GCP認証成功 (Project ID: {project_id})")

            # VertexAIの初期化
            return VertexAI(model_name="gemini-2.5-pro")
        except google.auth.exceptions.DefaultCredentialsError:
            print("❌ Google Cloud の認証情報が見つかりません。")
            print("   gcloud auth application-default login を実行して認証してください。")
            return None
        except Exception as e:
            print(f"❌ VertexAIの初期化中にエラーが発生しました: {e}")
            return None


class MockLLM:
    """デモ用のモックLLMクラス"""
    
    def invoke(self, prompt):
        """モックレスポンスを返す"""
        # プロンプトからビジネス要件を抽出
        if "ログイン機能付きのブログサイト" in prompt:
            return self._generate_blog_response()
        elif "マッチングプラットフォーム" in prompt:
            return self._generate_matching_response()
        else:
            return self._generate_generic_response(prompt)
    
    def _generate_blog_response(self):
        return '''```json
{
  "project_overview": {
    "name": "ログイン機能付きブログサイト",
    "description": "ユーザー認証機能を持つ個人ブログプラットフォーム",
    "technical_stack": ["React", "Node.js", "Express", "MongoDB", "JWT認証"],
    "estimated_timeline": "8-10週間"
  },
  "required_agents": [
    {
      "agent_name": "Tech Lead Agent",
      "agent_type": "tech_lead",
      "responsibility": "技術アーキテクチャの設計と開発チームの技術的意思決定",
      "skills": ["システム設計", "技術選定", "チームリーダーシップ", "コードレビュー"],
      "autonomy_level": "L2",
      "main_functions": ["アーキテクチャ設計", "技術標準策定", "コードレビュー", "技術課題解決"],
      "data_sources": ["技術ドキュメント", "業界ベストプラクティス", "パフォーマンス指標"],
      "kpis": ["コード品質スコア", "技術的負債削減率", "チーム生産性向上"]
    },
    {
      "agent_name": "Frontend Developer Agent",
      "agent_type": "frontend_developer", 
      "responsibility": "ユーザーインターフェースとフロントエンド機能の実装",
      "skills": ["React", "TypeScript", "CSS", "レスポンシブデザイン", "アクセシビリティ"],
      "autonomy_level": "L2",
      "main_functions": ["UI/UXコンポーネント開発", "状態管理実装", "APIクライアント実装", "テスト作成"],
      "data_sources": ["デザインシステム", "UIライブラリ", "ユーザビリティガイドライン"],
      "kpis": ["UI開発速度", "コンポーネント再利用率", "アクセシビリティスコア"]
    },
    {
      "agent_name": "Backend Developer Agent",
      "agent_type": "backend_developer",
      "responsibility": "サーバーサイドロジックとAPI開発", 
      "skills": ["Node.js", "Express", "MongoDB", "認証システム", "REST API"],
      "autonomy_level": "L2",
      "main_functions": ["API開発", "データベース設計", "認証機能実装", "セキュリティ実装"],
      "data_sources": ["APIドキュメント", "データベーススキーマ", "セキュリティガイドライン"],
      "kpis": ["API応答時間", "セキュリティ脆弱性数", "データベースパフォーマンス"]
    }
  ]
}```'''

    def _generate_matching_response(self):
        return '''```json
{
  "project_overview": {
    "name": "電気工事士向けキャリア相談マッチングプラットフォーム",
    "description": "電気工事士と経験豊富なメンターをつなぐキャリア相談プラットフォーム",
    "technical_stack": ["Vue.js", "Python", "Django", "PostgreSQL", "Redis", "WebRTC"],
    "estimated_timeline": "12-16週間"
  },
  "required_agents": [
    {
      "agent_name": "Business Analyst Agent",
      "agent_type": "business_analyst",
      "responsibility": "業界要件分析とビジネスロジック設計",
      "skills": ["業界知識", "要件分析", "ビジネスプロセス設計", "データ分析"],
      "autonomy_level": "L3",
      "main_functions": ["業界調査", "ユーザーニーズ分析", "ビジネスモデル検証", "KPI定義"],
      "data_sources": ["業界レポート", "ユーザーフィードバック", "競合分析データ"],
      "kpis": ["要件充足率", "ユーザー満足度", "ビジネス目標達成率"]
    },
    {
      "agent_name": "Matching Algorithm Agent",
      "agent_type": "algorithm_specialist",
      "responsibility": "メンターとメンティーの最適マッチングアルゴリズム開発",
      "skills": ["機械学習", "レコメンデーションシステム", "データサイエンス", "統計学"],
      "autonomy_level": "L2",
      "main_functions": ["マッチングアルゴリズム設計", "推薦精度改善", "A/Bテスト実施", "パフォーマンス最適化"],
      "data_sources": ["ユーザープロファイル", "マッチング履歴", "フィードバックデータ"],
      "kpis": ["マッチング成功率", "ユーザー継続率", "推薦精度スコア"]
    },
    {
      "agent_name": "Communication System Agent",
      "agent_type": "communication_specialist",
      "responsibility": "リアルタイム通信機能とビデオ通話システムの実装",
      "skills": ["WebRTC", "チャットシステム", "リアルタイム通信", "動画配信技術"],
      "autonomy_level": "L2",
      "main_functions": ["ビデオ通話実装", "チャット機能開発", "ファイル共有機能", "通話品質管理"],
      "data_sources": ["通話品質データ", "ネットワーク統計", "ユーザー利用パターン"],
      "kpis": ["通話成功率", "音質・画質スコア", "接続安定性"]
    }
  ]
}```'''

    def _generate_generic_response(self, prompt):
        return '''```json
{
  "project_overview": {
    "name": "Webアプリケーション開発プロジェクト",
    "description": "要件に基づくカスタムWebアプリケーション",
    "technical_stack": ["React", "Node.js", "MongoDB"],
    "estimated_timeline": "6-8週間"
  },
  "required_agents": [
    {
      "agent_name": "Tech Lead Agent",
      "agent_type": "tech_lead",
      "responsibility": "技術的な意思決定とアーキテクチャ設計",
      "skills": ["システム設計", "技術選定", "チームリーダーシップ"],
      "autonomy_level": "L2",
      "main_functions": ["アーキテクチャ設計", "技術標準策定", "コードレビュー"],
      "data_sources": ["技術ドキュメント", "ベストプラクティス"],
      "kpis": ["コード品質スコア", "技術的負債削減率"]
    },
    {
      "agent_name": "Full Stack Developer Agent",
      "agent_type": "fullstack_developer",
      "responsibility": "フロントエンドとバックエンドの統合開発",
      "skills": ["JavaScript", "React", "Node.js", "データベース設計"],
      "autonomy_level": "L2", 
      "main_functions": ["フルスタック開発", "API設計", "UI実装"],
      "data_sources": ["API仕様", "UIデザイン", "データベーススキーマ"],
      "kpis": ["開発速度", "バグ発生率", "コード再利用率"]
    }
  ]
}```'''


@app.route('/', methods=['POST'])
def generate_designs():
    """ビジネス要件を受け取り、エージェントの設計図を生成する"""
    try:
        if request.is_json:
            data = request.get_json()
            business_requirement = data.get("business_requirements")
        else:
            business_requirement = request.form.get("business_requirements")

        if not business_requirement:
            return jsonify({"error": "business_requirements is required"}), 400

        print(f"Received requirement: {business_requirement}")

        # 環境変数からDEMO_MODEを取得
        demo_mode = os.getenv('DEMO_MODE', 'true').lower() == 'true'

        # LLMを取得
        llm = get_llm(demo_mode)
        if llm is None and not demo_mode:
            return jsonify({"error": "Failed to initialize VertexAI. Check authentication."}), 500

        # プロンプトを作成して実行
        prompt = AGENT_DESIGN_PROMPT.format(business_requirement=business_requirement)

        # LLMに問い合わせを実行
        print("Generating agent design documents...")
        response = llm.invoke(prompt)

        # レスポンスからJSONを抽出
        try:
            json_start = response.find("```json")
            json_end = response.find("```", json_start + 7)

            if json_start != -1 and json_end != -1:
                json_content = response[json_start + 7:json_end].strip()
                design_data = json.loads(json_content)

                # 生成された設計書を保存
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_generated_designs(design_data, timestamp, business_requirement)

                return jsonify({
                    "success": True,
                    "timestamp": timestamp,
                    "business_requirement": business_requirement,
                    "generated_design": design_data
                }), 200
            else:
                return jsonify({
                    "error": "Could not extract JSON from LLM response",
                    "raw_response": response
                }), 500

        except json.JSONDecodeError as e:
            return jsonify({
                "error": f"Invalid JSON in LLM response: {str(e)}",
                "raw_response": response
            }), 500

    except Exception as e:
        print(f"Error in generate_designs: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    # .envファイルから環境変数を読み込む
    load_dotenv()

    # DEMO_MODEが設定されていなければ、デフォルトでtrueに設定
    if 'DEMO_MODE' not in os.environ:
        os.environ['DEMO_MODE'] = 'true'
        print("⚠️  DEMO_MODEが設定されていなかったため、'true'に設定しました。")

    # ポート番号を取得
    port = int(os.getenv('PORT', 8080))

    # Gunicornでの実行を推奨するメッセージ
    print("\n--- サーバー起動ガイド ---")
    print(f"開発サーバーを http://127.0.0.1:{port} で起動します。")
    print("本番環境ではGunicornの使用を推奨します:")
    print(f"gunicorn --bind 0.0.0.0:{port} --workers 1 --threads 8 main:app")
    print("--------------------------\n")

    app.run(host='0.0.0.0', port=port, debug=True)
