#!/bin/bash

echo "🚀 プロジェクトセットアップ開始..."

# フロントエンド依存関係インストール
echo "📦 フロントエンド依存関係インストール中..."
cd ../frontend
npm install

# バックエンド依存関係インストール  
echo "📦 バックエンド依存関係インストール中..."
cd ../backend
npm install

# 環境変数設定
echo "🔧 環境変数設定中..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  .envファイルを編集してください"
fi

echo "✅ セットアップ完了!"
echo ""
echo "🌐 開発サーバー起動:"
echo "  フロントエンド: cd frontend && npm start"
echo "  バックエンド: cd backend && npm run dev"
echo ""
echo "🐳 Docker起動:"
echo "  docker-compose up -d"
