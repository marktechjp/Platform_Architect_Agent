#!/usr/bin/env python3
"""
Gemini API 接続テストエージェント
"""
import os
import sys
from dotenv import load_dotenv

try:
    from langchain_google_vertexai import VertexAI
    import google.auth
    from google.api_core.exceptions import PermissionDenied
except ImportError:
    print("❌ 必要なライブラリが不足しています。 'pip install langchain-google-vertexai google-auth google-api-core' を実行してください。")
    sys.exit(1)

def run_test():
    """Gemini APIへの接続をテストする"""
    print("☁️ Gemini API 接続テストを開始します...")
    load_dotenv()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("❌ 環境変数 'GOOGLE_CLOUD_PROJECT' が.envファイルに設定されていません。")
        return

    print(f"🔑 プロジェクトID '{project_id}' を使用して接続を試みます。")

    try:
        # 認証情報を確認
        credentials, detected_project_id = google.auth.default()
        print("✅ Google Cloudの認証情報を正常に読み込みました。")

        # VertexAIクライアントの初期化
        # ユーザー指定のモデルに変更
        llm = VertexAI(project=project_id, model_name="gemini-2.5-pro")
        print("✅ VertexAIクライアントの初期化に成功。")

        # API呼び出しテスト
        print("🗣️ APIに応答をリクエストしています...")
        response = llm.invoke("1+1は？")

        if response:
            print("🎉 接続成功！ APIから応答がありました。")
            print(f"   Geminiの答え: '{response.strip()}'")
        else:
            print("❌ 接続に失敗しました。APIから空の応答がありました。")

    except PermissionDenied as e:
        print(f"❌ 権限エラー: Vertex AI APIが有効になっていないか、必要な権限がありません。")
        print(f"   👉 エラー詳細: {e.message}")
        print(f"   👉 確認URL: https://console.cloud.google.com/apis/library/aiplatform.googleapis.com?project={project_id}")
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    run_test()
