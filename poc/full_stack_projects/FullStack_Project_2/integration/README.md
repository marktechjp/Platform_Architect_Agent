# FullStack_Project_2

**要件**: 電気工事士向けのキャリア相談ができるマッチングプラットフォーム
**生成日時**: 2025-09-13 17:30:17

## 🏗️ アーキテクチャ

このプロジェクトは3つのエージェントによって自動生成されました：

- **Platform Architect Agent**: プロジェクト設計・技術選定
- **Frontend Developer Agent**: Vanilla HTML/CSS/JS アプリケーション
- **Backend Developer Agent**: Node.js + Express API サーバー

## 🚀 クイックスタート

### 前提条件
- Node.js (v16以上)
- Docker & Docker Compose
- Git

### 開発環境セットアップ

```bash
# プロジェクトクローン
git clone <repository-url>
cd FullStack_Project_2

# Docker Composeで全サービス起動
cd integration
docker-compose up -d

# または個別起動
./setup.sh
```

### アクセス
- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:5000
- **API ドキュメント**: http://localhost:5000/docs

## 📁 プロジェクト構成

```
FullStack_Project_2/
├── frontend/           # Vanilla HTML/CSS/JS アプリケーション
├── backend/            # Node.js + Express API サーバー
├── integration/        # Docker Compose & 統合設定
└── docs/              # ドキュメント
```

## 🔧 開発

### フロントエンド開発
```bash
cd frontend
npm install
npm start
```

### バックエンド開発
```bash
cd backend
npm install
npm run dev
```

## 📋 機能

### フロントエンド
- モダンJS (ES6+)
- レスポンシブデザイン
- フォームバリデーション

### バックエンド
- JWT認証
- ユーザー登録・ログイン
- CORS対応
- エラーハンドリング

### API エンドポイント
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me
- GET /health

## 🚀 次のステップ

1. QA Agent による自動テスト生成
2. Deploy Agent による CI/CD 構築  
3. Security Agent によるセキュリティ監査
4. Performance Agent による最適化

---
*このプロジェクトはFull Agent Orchestratorによって自動生成されました*
