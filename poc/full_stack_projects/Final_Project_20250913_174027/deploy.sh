#!/bin/bash
# AIによって生成されたデプロイスクリプト

set -e # エラーが発生したらスクリプトを停止

echo "🚀 Final_Project_20250913_174027 のデプロイを開始します..."
echo "--------------------------------------------------"

# --- 変数設定 (環境に合わせて変更してください) ---
GCP_PROJECT_ID="your-gcp-project-id"
GCP_REGION="asia-northeast1"
FRONTEND_SERVICE_NAME="final-project-20250913-174027-frontend"
BACKEND_SERVICE_NAME="final-project-20250913-174027-backend"

# --- GCPプロジェクト設定 ---
echo "1. GCPプロジェクトを設定します: $GCP_PROJECT_ID"
gcloud config set project $GCP_PROJECT_ID


# --- フロントエンドのデプロイ ---
echo "\n2. フロントエンドをビルドしてCloud Runにデプロイします..."
cd frontend

# Dockerイメージをビルド
echo "   - Dockerイメージをビルド中: $FRONTEND_SERVICE_NAME"
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$FRONTEND_SERVICE_NAME

# Cloud Runにデプロイ
echo "   - Cloud Runにデプロイ中: $FRONTEND_SERVICE_NAME"
gcloud run deploy $FRONTEND_SERVICE_NAME \
  --image gcr.io/$GCP_PROJECT_ID/$FRONTEND_SERVICE_NAME \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated

cd ..

# --- バックエンドのデプロイ ---
echo "\n3. バックエンドをビルドしてCloud Runにデプロイします..."
cd backend

# Dockerイメージをビルド
echo "   - Dockerイメージをビルド中: $BACKEND_SERVICE_NAME"
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$BACKEND_SERVICE_NAME

# Cloud Runにデプロイ
echo "   - Cloud Runにデプロイ中: $BACKEND_SERVICE_NAME"
gcloud run deploy $BACKEND_SERVICE_NAME \
  --image gcr.io/$GCP_PROJECT_ID/$BACKEND_SERVICE_NAME \
  --platform managed \
  --region $GCP_REGION \
  --allow-unauthenticated # 必要に応じて変更

cd ..

echo "--------------------------------------------------"
echo "🎉 全てのデプロイが完了しました！"

# ここでCloud RunのURLなどを表示
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE_NAME --platform managed --region $GCP_REGION --format 'value(status.url)')
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE_NAME --platform managed --region $GCP_REGION --format 'value(status.url)')

echo "   - フロントエンドURL: $FRONTEND_URL"
echo "   - バックエンドURL: $BACKEND_URL"
