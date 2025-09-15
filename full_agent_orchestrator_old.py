import os
import glob
from datetime import datetime

class FullAgentOrchestrator:
    def __init__(self, base_directory="."):
        self.base_directory = base_directory
        self.latest_project_dir = self.find_latest_project_directory()

    def find_latest_project_directory(self):
        """日付プレフィックスを持つ最新のプロジェクトディレクトリを見つける"""
        # --- デバッグコード ---
        print(f"\n[デバッグ情報]")
        abs_base_directory = os.path.abspath(self.base_directory)
        print(f"検索ベースディレクトリ: {abs_base_directory}")
        
        pattern = os.path.join(self.base_directory, "[0-9]" * 8 + "_*")
        print(f"検索パターン: {pattern}")
        
        try:
            print(f"ベースディレクトリ内のファイル/フォルダ一覧:")
            for item in os.listdir(self.base_directory):
                print(f"  - {item}")
        except Exception as e:
            print(f"  - ディレクトリ一覧の取得に失敗: {e}")
        # --- デバッグコードここまで ---

        project_dirs = glob.glob(pattern)
        
        # --- デバッグコード ---
        print(f"globで検出されたディレクトリ数: {len(project_dirs)}")
        if project_dirs:
            print("検出されたディレクトリ:")
            for p_dir in project_dirs:
                print(f"  - {p_dir}")
        print("[デバッグ情報ここまで]\n")
        # --- デバッグコードここまで ---
        
        if not project_dirs:
            return None

        # ディレクトリ名の日付部分でソートして最新のものを取得
        latest_dir = max(project_dirs, key=lambda d: os.path.basename(d).split('_')[0])
        return latest_dir

    def execute(self):
        """統括エージェントのメイン実行フロー"""
        if not self.latest_project_dir:
            print("❌ 設計書フォルダが見つかりませんでした。")
            print("   まずは `poc/main.py` を実行して設計書を生成してください。")
            return

        print(f"📂 最新のプロジェクトフォルダを検出しました: {os.path.basename(self.latest_project_dir)}")
        print("-" * 50)

        # 設計書ファイル（.md）を順番に読み込む
        design_files = sorted(glob.glob(os.path.join(self.latest_project_dir, "*.md")))

        if not design_files:
            print("📂 設計書ファイル（.md）が見つかりませんでした。")
            return
            
        print("📋 以下の設計書に基づいて、孫エージェントによるコーディングを開始します。")

        for design_file in design_files:
            self.process_design_file(design_file)
            
        print("-" * 50)
        print("✅ すべての設計書の処理が完了しました。")

    def process_design_file(self, file_path):
        """個別の設計書ファイルを処理する（将来のコーディングAI呼び出し部分）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ファイル名から担当名を取得 (例: 01_architect.md -> architect)
            agent_name = os.path.basename(file_path).split('_', 1)[1].replace('.md', '')
            
            print(f"\n🤖孫エージェントを準備中: `{agent_name}` 担当")
            print(f"   設計書: {os.path.basename(file_path)}")
            
            # --- ここからが孫エージェント（コーディングAI）の呼び出し部分 ---
            # 今回はシミュレーションとして、設計書の冒頭部分を表示する
            print("   [将来の処理] 以下の設計書を基にコーディングを指示します...")
            
            first_line = content.splitlines()[0] if content else ""
            print(f"   設計書内容プレビュー: \"{first_line}...\"")
            # ----------------------------------------------------------------

        except Exception as e:
            print(f"❌ ファイル処理中にエラーが発生しました ({file_path}): {e}")


if __name__ == '__main__':
    # 検索対象のベースディレクトリを . (カレントディレクトリ) に指定
    orchestrator = FullAgentOrchestrator(base_directory=".")
    orchestrator.execute()
