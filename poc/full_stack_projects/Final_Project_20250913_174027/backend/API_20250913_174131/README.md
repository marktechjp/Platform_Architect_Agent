# Backend API

Backend Developer Agent によって自動生成されたAPIサーバーです。

## セットアップ

```bash
npm install
npm start
```

## API エンドポイント

- POST /api/auth/register - ユーザー登録
- POST /api/auth/login - ログイン
- GET /api/auth/me - ユーザー情報取得
- GET /health - ヘルスチェック

## 使用例

### ユーザー登録
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "firstName": "太郎",
    "lastName": "山田"
  }'
```

### ログイン
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```
