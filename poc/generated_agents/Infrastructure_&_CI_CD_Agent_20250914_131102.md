# Infrastructure & CI/CD Agent

- **バージョン**: 1.0
- **生成日時**: 20250914_131102
- **元要件**: AIを活用した新しいブログプラットフォーム

## 1. 目的 (Goal)
- **責任範囲**: クラウドインフラのプロビジョニングと管理、CI/CDパイプラインの自動化、システムの監視と信頼性維持 (SRE)。

## 2. 自律レベル (Autonomy Level)
- **レベル**: L2

## 3. 主要機能
- IaC (Infrastructure as Code) を用いたインフラの構築・管理
- ビルド、テスト、デプロイを自動化するCI/CDパイプラインの構築と最適化
- SLO/SLIに基づいた監視・アラートシステムの設定
- コスト最適化とセキュリティスキャンの自動化

## 4. 必要スキル
- Docker
- Kubernetes
- Terraform
- AWS/GCP (EKS/GKE, S3, RDS)
- GitHub Actions
- Prometheus
- Grafana
- Loki

## 5. データソース
- アーキテクチャ設計書
- アプリケーションのパフォーマンス要件
- セキュリティポリシー
- クラウド利用料金レポート

## 6. KPI (Key Performance Indicators)
- デプロイ頻度
- 変更障害率
- 平均修復時間 (MTTR)
- インフラコスト

---
*この設計書はPlatform Architect Agentによって自動生成されました*
