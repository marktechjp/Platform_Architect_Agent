#!/usr/bin/env python3
"""
Deploy Agent - Phase 4
品質保証済みのコードをクラウド環境に自動デプロイするためのエージェント
"""
import os
from pathlib import Path

class DeployAgent:
    """デプロイスクリプトを自動生成するデプロイエージェント"""

    def __init__(self):
        self.deployment_plan = {}

    def analyze_project(self, project_path):
        """プロジェクトを分析し、デプロイ計画を立案する"""
        print(f"🔬 プロジェクト分析開始 (デプロイ観点): {project_path}")
        
        project_name = Path(project_path).name
        frontend_path = Path(project_path) / "frontend"
        backend_path = Path(project_path) / "backend"
        
        analysis = {
            "project_name": project_name,
            "has_frontend": frontend_path.exists(),
            "has_backend": backend_path.exists(),
            "deployment_target": "Cloud Run" # このPoCでのターゲット
        }
        
        print(f"✅ デプロイ分析完了。ターゲット: {analysis['deployment_target']}")
        return analysis

    def generate_deployment_artifacts(self, project_path, analysis):
        """分析結果に基づいてデプロイ用の成果物を生成する"""
        print(f"🚀 デプロイ成果物生成開始: {analysis['project_name']}")
        
        generated_files = []
        
        # フロントエンドのDockerfile生成
        if analysis["has_frontend"]:
            fe_dockerfile = self._get_frontend_dockerfile_template()
            fe_path = Path(project_path) / "frontend" / "Dockerfile"
            self._save_artifact(fe_path, fe_dockerfile)
            generated_files.append(str(fe_path))

        # バックエンドのDockerfile生成
        if analysis["has_backend"]:
            be_dockerfile = self._get_backend_dockerfile_template()
            be_path = Path(project_path) / "backend" / "Dockerfile"
            self._save_artifact(be_path, be_dockerfile)
            generated_files.append(str(be_path))
            
        # deploy.sh スクリプト生成
        deploy_script = self._get_deploy_script_template(analysis)
        script_path = Path(project_path) / "deploy.sh"
        self._save_artifact(script_path, deploy_script, make_executable=True)
        generated_files.append(str(script_path))

        print(f"✅ デプロイ成果物生成完了。 {len(generated_files)} ファイル")
        return generated_files

    def _save_artifact(self, file_path, content, make_executable=False):
        """生成された成果物をファイルに保存する"""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if make_executable:
                os.chmod(file_path, 0o755)
                
            print(f"   - 📄 成果物保存: {file_path}")
        except Exception as e:
            print(f"   - ❌ 保存失敗: {file_path} ({e})")

    def run_deployment_preparation(self, project_path):
        """指定されたプロジェクトに対してデプロイ準備ワークフローを実行する"""
        print("\n" + "="*70)
        print(f"🏭 Deploy Agent ワークフロー開始: {Path(project_path).name}")
        print("="*70)
        
        # 1. プロジェクト分析
        analysis = self.analyze_project(project_path)
        
        # 2. デプロイ成果物生成
        generated_artifacts = self.generate_deployment_artifacts(project_path, analysis)
        
        print("\n🎉 デプロイ準備完了!")
        print(f"   - {analysis['project_name']} のデプロイ準備が整いました。")
        print(f"   - {len(generated_artifacts)} 個のデプロイ用ファイルが生成されました。")
        print(f"   - 次のステップ: `{Path(project_path) / 'deploy.sh'}` を実行して、クラウドへのデプロイを開始してください。")
        print("="*70 + "\n")
        
        return {"analysis": analysis, "generated_artifacts": generated_artifacts}

    # --- テンプレート ---

    def _get_frontend_dockerfile_template(self):
        return """
# Stage 1: ビルド環境
FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係をコピーしてインストール
COPY package*.json ./
RUN npm install

# ソースコードをコピー
COPY . .

# アプリケーションをビルド
RUN npm run build

# Stage 2: 本番環境
FROM nginx:1.21-alpine

# ビルド成果物をNginxの公開ディレクトリにコピー
COPY --from=builder /app/build /usr/share/nginx/html

# Nginxの設定ファイルをコピー (オプション)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
"""

    def _get_backend_dockerfile_template(self):
        return """
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 8080

CMD ["node", "server.js"]
"""

    def _get_deploy_script_template(self, analysis):
        project_name = analysis['project_name'].lower().replace('_', '-')
        gcp_project_id = "your-gcp-project-id" # ここは手動で設定する必要がある
        gcp_region = "asia-northeast1"

        script = f"""#!/bin/bash
# AIによって生成されたデプロイスクリプト

set -e # エラーが発生したらスクリプトを停止

echo "🚀 {analysis['project_name']} のデプロイを開始します..."
echo "--------------------------------------------------"

# --- 変数設定 (環境に合わせて変更してください) ---
GCP_PROJECT_ID="{gcp_project_id}"
GCP_REGION="{gcp_region}"
FRONTEND_SERVICE_NAME="{project_name}-frontend"
BACKEND_SERVICE_NAME="{project_name}-backend"

# --- GCPプロジェクト設定 ---
echo "1. GCPプロジェクトを設定します: $GCP_PROJECT_ID"
gcloud config set project $GCP_PROJECT_ID

"""
        if analysis['has_frontend']:
            script += f"""
# --- フロントエンドのデプロイ ---
echo "\\n2. フロントエンドをビルドしてCloud Runにデプロイします..."
cd frontend

# Dockerイメージをビルド
echo "   - Dockerイメージをビルド中: $FRONTEND_SERVICE_NAME"
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$FRONTEND_SERVICE_NAME

# Cloud Runにデプロイ
echo "   - Cloud Runにデプロイ中: $FRONTEND_SERVICE_NAME"
gcloud run deploy $FRONTEND_SERVICE_NAME \\
  --image gcr.io/$GCP_PROJECT_ID/$FRONTEND_SERVICE_NAME \\
  --platform managed \\
  --region $GCP_REGION \\
  --allow-unauthenticated

cd ..
"""
        if analysis['has_backend']:
            script += f"""
# --- バックエンドのデプロイ ---
echo "\\n3. バックエンドをビルドしてCloud Runにデプロイします..."
cd backend

# Dockerイメージをビルド
echo "   - Dockerイメージをビルド中: $BACKEND_SERVICE_NAME"
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$BACKEND_SERVICE_NAME

# Cloud Runにデプロイ
echo "   - Cloud Runにデプロイ中: $BACKEND_SERVICE_NAME"
gcloud run deploy $BACKEND_SERVICE_NAME \\
  --image gcr.io/$GCP_PROJECT_ID/$BACKEND_SERVICE_NAME \\
  --platform managed \\
  --region $GCP_REGION \\
  --allow-unauthenticated # 必要に応じて変更

cd ..
"""

        script += """
echo "--------------------------------------------------"
echo "🎉 全てのデプロイが完了しました！"

# ここでCloud RunのURLなどを表示
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE_NAME --platform managed --region $GCP_REGION --format 'value(status.url)')
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE_NAME --platform managed --region $GCP_REGION --format 'value(status.url)')

echo "   - フロントエンドURL: $FRONTEND_URL"
echo "   - バックエンドURL: $BACKEND_URL"
"""
        return script

def demo_deploy_agent():
    """Deploy Agentのデモ実行"""
    deploy_agent = DeployAgent()
    
    # 実行対象のプロジェクトパス
    target_project_path = "full_stack_projects/FullStack_Project_2"
    
    if not Path(target_project_path).exists():
        print(f"❌ デプロイ対象のプロジェクトが見つかりません: {target_project_path}")
        print("   先に `full_agent_orchestrator.py` を実行してプロジェクトを生成してください。")
        return
        
    deploy_agent.run_deployment_preparation(target_project_path)

if __name__ == "__main__":
    demo_deploy_agent()
