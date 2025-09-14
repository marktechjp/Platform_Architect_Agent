# Platform Architect Agent - PoC

このPoC（概念実証）は、ビジネス要件から自動的に子エージェントの設計書を生成するPlatform Architect Agentの実装です。

## 機能概要

- ビジネス要件を自然言語で入力
- Gemini 2.0を使用して必要な子エージェントを分析・設計
- 各エージェントの詳細な設計書（Markdownファイル）を自動生成
- プロジェクト概要とエージェント情報をJSONで出力

## セットアップ

### 1. 依存関係のインストール

```bash
cd poc
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成し、Google Cloud設定を記載：

```bash
cp .env.example .env
# .envファイルを編集してプロジェクトIDなどを設定
```

必要な環境変数：
- `GOOGLE_CLOUD_PROJECT`: Google CloudプロジェクトID
- `GOOGLE_CLOUD_LOCATION`: Vertex AIの地域（デフォルト: us-central1）

### 3. Google Cloud認証

開発環境では以下のいずれかの方法で認証：

```bash
# オプション1: gcloud CLIでログイン（推奨）
gcloud auth application-default login

# オプション2: サービスアカウントキーを使用
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

## 使用方法

### 1. サーバー起動

```bash
python main.py
```

サーバーが`http://localhost:8080`で起動します。

### 2. テストクライアントでの実行（推奨）

```bash
# 対話式でテストケースを選択
python test_client.py

# 直接要件を指定
python test_client.py "ログイン機能付きのブログサイト"
```

### 3. HTTP APIでの直接呼び出し

```bash
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{"requirement": "ログイン機能付きのブログサイト"}'
```

## 出力ファイル

生成された設計書は`generated_agents/`ディレクトリに保存されます：

- `project_overview_YYYYMMDD_HHMMSS.json`: プロジェクト概要
- `{エージェント名}_YYYYMMDD_HHMMSS.md`: 各エージェントの設計書

## API仕様

### POST /

**リクエスト:**
```json
{
  "requirement": "ビジネス要件の説明"
}
```

**レスポンス（成功時）:**
```json
{
  "success": true,
  "timestamp": "20250912_143022",
  "business_requirement": "ログイン機能付きのブログサイト",
  "generated_design": {
    "project_overview": { ... },
    "required_agents": [ ... ]
  }
}
```

## テストケース例

1. **ログイン機能付きのブログサイト**
   - Tech Lead Agent
   - Frontend Developer Agent
   - Backend Developer Agent

2. **電気工事士向けキャリア相談マッチングプラットフォーム**
   - ビジネスアナリストエージェント
   - マッチングアルゴリズムエージェント
   - UI/UXデザイナーエージェント

3. **オンライン書店Webアプリケーション**
   - データベース設計エージェント
   - 決済システムエージェント
   - レコメンデーションエージェント

## アーキテクチャ

```
[ビジネス要件] → [Platform Architect Agent] → [子エージェント設計書群]
      ↓                    ↓                          ↓
  自然言語入力        Gemini 2.0分析           Markdownファイル群
```

## 今後の拡張予定

- **フェーズ2**: 生成された子エージェントが実際にコード生成を実行
- **フェーズ3**: 複数エージェントの連携による完全自動開発
- Docker化とCloud Runへのデプロイ
- Workload Identityによる認証強化

## トラブルシューティング

### よくある問題

1. **認証エラー**
   ```
   Error initializing LLM: Vertex AI authentication failed
   ```
   → Google Cloud認証を確認してください

2. **JSON解析エラー**
   ```
   Invalid JSON in LLM response
   ```
   → プロンプトが複雑すぎる可能性があります。シンプルな要件から試してください

3. **接続エラー**
   ```
   サーバーに接続できません
   ```
   → Flask アプリが起動していることを確認してください

### デバッグ

- `FLASK_ENV=development`を設定してデバッグモードで実行
- LLMの生成結果が`raw_response`に含まれるため、エラー時に確認可能

---

**注意**: このPoCは開発・テスト目的です。本番環境では追加のセキュリティ対策とスケーラビリティ考慮が必要です。
