#!/usr/bin/env python3
"""
Full Agent Orchestrator - Phase 3
Platform Architect Agent + Frontend Developer Agent + Backend Developer Agent の完全統合
"""
import os
import json
from datetime import datetime
from pathlib import Path
import requests # HTTPリクエストのために追加
import time
import google.auth

# 既存のエージェントをインポート
from frontend_developer_agent import FrontendDeveloperAgent
from simple_backend_agent import BackendDeveloperAgent
from qa_agent import QAEngineerAgent # QAエージェントをインポート
from deploy_agent import DeployAgent # Deploy Agent をインポート
from security_agent import SecurityAgent # Security Agent をインポート

class FullAgentOrchestrator:
    """全エージェントの統合オーケストレータ"""
    
    def __init__(self):
        self.project_name = ""
        self.requirement = ""
        self.agents = {}
        self.workflow_history = []
        self.project_artifacts = {}
        
    def initialize_project(self, requirement, project_name=None):
        """プロジェクトの初期化"""
        self.requirement = requirement
        self.project_name = project_name or f"FullProject_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.workflow_history = []
        self.project_artifacts = {}
        
        print(f"🚀 フルスタックプロジェクト初期化: {self.project_name}")
        print(f"📋 要件: {requirement}")
        
    def run_platform_architect(self):
        """Platform Architect Agentの実行"""
        print(f"\n🏗️  Platform Architect Agent 実行中...")
        
        design_result = self._generate_project_design(self.requirement)
        
        self.workflow_history.append({
            "step": 1,
            "agent": "Platform Architect Agent",
            "action": "プロジェクト設計書生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": design_result
        })
        
        self.project_artifacts["design"] = design_result
        
        print(f"✅ 設計書生成完了")
        print(f"🤖 生成エージェント数: {len(design_result.get('required_agents', []))}")
        # APIからのレスポンス形式に合わせてキーを修正
        overview = design_result.get('project_overview', {})
        tech_stack = overview.get('technical_stack', [])
        print(f"🛠️  推奨技術スタック: {', '.join(tech_stack)}")
        
        return design_result
    
    def run_frontend_agent(self, design_result):
        """Frontend Developer Agentの実行"""
        print(f"\n🎨 Frontend Developer Agent 実行中...")
        
        tech_stack = design_result["project_overview"].get("technical_stack", ["React", "TypeScript"])
        
        frontend_agent = FrontendDeveloperAgent()
        self.agents["frontend"] = frontend_agent
        
        generated_code = frontend_agent.generate_login_page(
            project_name=self.project_name,
            tech_stack=tech_stack
        )
        
        output_dir = f"full_stack_projects/{self.project_name}/frontend"
        project_dir = frontend_agent.save_generated_code(
            generated_code,
            "App",
            output_dir
        )
        
        self.workflow_history.append({
            "step": 2,
            "agent": "Frontend Developer Agent",
            "action": "フロントエンドコード生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "framework": generated_code["framework"],
                "features": generated_code["features"],
                "project_dir": project_dir
            }
        })
        
        self.project_artifacts["frontend"] = {
            "code": generated_code,
            "location": project_dir
        }
        
        print(f"✅ フロントエンド生成完了: {generated_code['framework']}")
        print(f"📁 保存先: {project_dir}")
        
        return generated_code, project_dir
    
    def run_backend_agent(self, design_result):
        """Backend Developer Agentの実行"""
        print(f"\n⚙️  Backend Developer Agent 実行中...")
        
        tech_stack = design_result["project_overview"].get("technical_stack", ["Node.js", "Express"])
        requirements = ["ログイン機能", "ユーザー登録", "認証"]
        
        backend_agent = BackendDeveloperAgent()
        self.agents["backend"] = backend_agent
        
        generated_code = backend_agent.generate_backend_api(
            project_name=self.project_name,
            tech_stack=tech_stack,
            requirements=requirements
        )
        
        output_dir = f"full_stack_projects/{self.project_name}/backend"
        project_dir = backend_agent.save_generated_backend(
            generated_code,
            "API",
            output_dir
        )
        
        self.workflow_history.append({
            "step": 3,
            "agent": "Backend Developer Agent",
            "action": "バックエンドAPI生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "framework": generated_code["framework"],
                "features": generated_code["features"],
                "endpoints": generated_code["endpoints"],
                "project_dir": project_dir
            }
        })
        
        self.project_artifacts["backend"] = {
            "code": generated_code,
            "location": project_dir
        }
        
        print(f"✅ バックエンド生成完了: {generated_code['framework']}")
        print(f"📁 保存先: {project_dir}")
        print(f"🔗 API エンドポイント: {len(generated_code['endpoints'])}個")
        
        return generated_code, project_dir
    
    def run_qa_agent(self):
        """QA Engineer Agentの実行"""
        print(f"\n🔬 QA Engineer Agent 実行中...")
        project_dir = f"full_stack_projects/{self.project_name}"
        
        qa_agent = QAEngineerAgent()
        self.agents["qa"] = qa_agent
        
        qa_result = qa_agent.run_qa_workflow(project_dir)
        
        self.workflow_history.append({
            "step": 4, # ステップ番号を更新
            "agent": "QA Engineer Agent",
            "action": "テストコード自動生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "generated_tests_count": len(qa_result.get("generated_tests", [])),
                "generated_files": qa_result.get("generated_tests", [])
            }
        })
        
        self.project_artifacts["qa"] = qa_result
        
        print(f"✅ QA Agent 実行完了")
        print(f"📄 生成テストファイル数: {len(qa_result.get('generated_tests', []))}")
        
        return qa_result

    def run_deploy_agent(self):
        """Deploy Agentの実行"""
        print(f"\n🚀 Deploy Agent 実行中...")
        project_dir = f"full_stack_projects/{self.project_name}"
        
        deploy_agent = DeployAgent()
        self.agents["deploy"] = deploy_agent
        
        deploy_result = deploy_agent.run_deployment_preparation(project_dir)
        
        self.workflow_history.append({
            "step": 5, # ステップ番号を更新
            "agent": "Deploy Agent",
            "action": "デプロイ成果物生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "generated_artifacts_count": len(deploy_result.get("generated_artifacts", [])),
                "generated_files": deploy_result.get("generated_artifacts", [])
            }
        })
        
        self.project_artifacts["deploy"] = deploy_result
        
        print(f"✅ Deploy Agent 実行完了")
        print(f"📦 生成されたデプロイ成果物数: {len(deploy_result.get('generated_artifacts', []))}")
        
        return deploy_result

    def run_security_agent(self, llm):
        """Security Agentの実行"""
        print(f"\n🛡️ Security Agent 実行中...")
        project_dir = f"full_stack_projects/{self.project_name}"
        
        security_agent = SecurityAgent(llm)
        self.agents["security"] = security_agent
        
        report_path = security_agent.run(project_dir)
        
        self.workflow_history.append({
            "step": 6, # ステップ番号を更新
            "agent": "Security Agent",
            "action": "セキュリティ監査実行",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "report_path": report_path
            }
        })
        
        self.project_artifacts["security_report"] = report_path
        
        print(f"✅ Security Agent 実行完了")
        print(f"📄 監査レポート: {report_path}")
        
        return report_path

    def generate_integration_artifacts(self):
        """統合用の成果物生成"""
        print(f"\n🔄 統合成果物生成中...")
        
        # Docker Compose生成
        docker_compose = self._generate_docker_compose()
        
        # プロジェクト全体のREADME生成
        main_readme = self._generate_main_readme()
        
        # 開発環境セットアップスクリプト
        setup_script = self._generate_setup_script()
        
        # API統合設定
        api_config = self._generate_api_config()
        
        integration_artifacts = {
            "docker-compose.yml": docker_compose,
            "README.md": main_readme,
            "setup.sh": setup_script,
            "api-config.json": api_config
        }
        
        # 統合ファイル保存
        integration_dir = f"full_stack_projects/{self.project_name}/integration"
        os.makedirs(integration_dir, exist_ok=True)
        
        for filename, content in integration_artifacts.items():
            with open(f"{integration_dir}/{filename}", 'w', encoding='utf-8') as f:
                f.write(content)
        
        self.workflow_history.append({
            "step": 7, # ステップ番号を更新
            "agent": "Integration Manager",
            "action": "統合成果物生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "artifacts": list(integration_artifacts.keys()),
                "location": integration_dir
            }
        })
        
        self.project_artifacts["integration"] = {
            "artifacts": integration_artifacts,
            "location": integration_dir
        }
        
        print(f"✅ 統合成果物生成完了")
        print(f"📁 保存先: {integration_dir}")
        print(f"📦 生成ファイル: {', '.join(integration_artifacts.keys())}")
        
        return integration_artifacts, integration_dir
    
    def generate_final_summary(self):
        """最終プロジェクトサマリー生成"""
        print(f"\n📊 最終プロジェクトサマリー生成中...")
        
        summary = {
            "project_info": {
                "name": self.project_name,
                "requirement": self.requirement,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_duration": self._calculate_total_duration()
            },
            "architecture": {
                "frontend": {
                    "framework": self.project_artifacts["frontend"]["code"]["framework"],
                    "features": self.project_artifacts["frontend"]["code"]["features"],
                    "location": self.project_artifacts["frontend"]["location"]
                },
                "backend": {
                    "framework": self.project_artifacts["backend"]["code"]["framework"],
                    "features": self.project_artifacts["backend"]["code"]["features"],
                    "endpoints": self.project_artifacts["backend"]["code"]["endpoints"],
                    "location": self.project_artifacts["backend"]["location"]
                },
                "integration": {
                    "artifacts": list(self.project_artifacts["integration"]["artifacts"].keys()),
                    "location": self.project_artifacts["integration"]["location"]
                }
            },
            "workflow_summary": {
                "total_steps": len(self.workflow_history),
                "agents_involved": len(set(step["agent"] for step in self.workflow_history)),
                "execution_timeline": self.workflow_history
            },
            "deliverables": {
                "frontend_app": f"{self.project_artifacts['frontend']['location']}/",
                "backend_api": f"{self.project_artifacts['backend']['location']}/",
                "integration": f"{self.project_artifacts['integration']['location']}/",
                "documentation": f"full_stack_projects/{self.project_name}/"
            },
            "next_phase_recommendations": [
                "QA Agent による自動テスト生成",
                "Deploy Agent による CI/CD パイプライン構築",
                "Monitoring Agent によるログ・メトリクス設定",
                "Security Agent によるセキュリティ監査",
                "Performance Agent による最適化実装"
            ]
        }
        
        # 最終サマリー保存
        summary_dir = f"full_stack_projects/{self.project_name}"
        with open(f"{summary_dir}/project_final_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 最終サマリー保存完了: {summary_dir}/project_final_summary.json")
        return summary
    
    def run_full_stack_workflow(self, requirement, project_name=None):
        """フルスタック完全ワークフローの実行"""
        print("🌟 フルスタック完全ワークフロー開始")
        print("=" * 70)
        
        # 1. プロジェクト初期化
        self.initialize_project(requirement, project_name)
        
        # 2. Platform Architect Agent実行
        design_result = self.run_platform_architect()
        
        # 3. Frontend Developer Agent実行
        self.run_frontend_agent(design_result)
        
        # 4. Backend Developer Agent実行  
        self.run_backend_agent(design_result)
        
        # 5. QA Engineer Agent実行
        self.run_qa_agent()
        
        # 6. Deploy Agent実行 (新規追加)
        self.run_deploy_agent()

        # 7. Security Agent実行 (新規追加)
        # Platform Architect Agentが使用しているLLMを渡す必要がある
        # ここでは仮のインスタンス化を行うが、将来的には一元管理すべき
        project_path = f"full_stack_projects/{self.project_name}"
        # --------------------------------------------------------------------------
        # Step 7: Security Agent
        # --------------------------------------------------------------------------
        print("\n🛡️ Security Agent 実行中...")
        from security_agent import SecurityAgent
        # from langchain_community.llms.vertexai import VertexAI
        from langchain_google_vertexai import VertexAI
        
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            try:
                _, project_id = google.auth.default()
            except google.auth.exceptions.DefaultCredentialsError:
                print("❌ Google Cloud credentials not found. Please run 'gcloud auth application-default login'.")
                return

        llm = VertexAI(project=project_id, model_name="gemini-2.5-pro")
        security_agent = SecurityAgent(llm=llm)
        report_path = security_agent.run(project_path)
        print(f"✅ Security Agent 実行完了")
        print(f"📄 監査レポート: {report_path}")

        # --------------------------------------------------------------------------
        # Step 8: Integration Artifacts
        # --------------------------------------------------------------------------
        self.generate_integration_artifacts()
        
        # 9. 最終サマリー生成 (旧8)
        final_summary = self.generate_final_summary()
        
        print("\n" + "=" * 70)
        print("🎉 フルスタックワークフロー完了!")
        print(f"📋 プロジェクト: {self.project_name}")
        print(f"🤖 実行エージェント: {final_summary['workflow_summary']['agents_involved']}個")
        print(f"📦 成果物: フロントエンド + バックエンド + 統合ツール")
        print(f"📁 プロジェクトディレクトリ: full_stack_projects/{self.project_name}/")
        print("\n🚀 次のステップ:")
        for step in final_summary["next_phase_recommendations"][:3]:
            print(f"   - {step}")
        
        return final_summary
    
    def _generate_project_design(self, requirement):
        """プロジェクト設計書生成を、稼働中のPlatform Architect Agentサーバーに依頼する"""
        url = "http://localhost:8080/"
        payload = {"business_requirements": requirement}
        
        try:
            response = requests.post(url, json=payload, timeout=180) # タイムアウトを延長
            response.raise_for_status() # エラーがあれば例外を発生
            
            result = response.json()
            # APIからのレスポンス形式に合わせて 'generated_design' を抽出
            if result.get("success") and "generated_design" in result:
                return result["generated_design"]
            else:
                print(f"❌ APIからの応答エラー: {result.get('error', '不明なエラー')}")
                raise Exception(f"API Error: {result.get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Platform Architect Agentサーバーへの接続に失敗しました: {e}")
            print("   - サーバー (main.py) が本番モードで起動しているか確認してください。")
            print("   - サーバーログにエラーが表示されていないか確認してください。")
            raise
    
    def _generate_docker_compose(self):
        """Docker Compose設定生成"""
        return '''version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
    depends_on:
      - backend
    volumes:
      - ./frontend/src:/app/src

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=development
      - JWT_SECRET=your-secret-key
      - MONGODB_URI=mongodb://mongodb:27017/myapp
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
'''
    
    def _generate_main_readme(self):
        """メインREADME生成"""
        frontend_framework = self.project_artifacts["frontend"]["code"]["framework"]
        backend_framework = self.project_artifacts["backend"]["code"]["framework"]
        
        return f'''# {self.project_name}

**要件**: {self.requirement}
**生成日時**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🏗️ アーキテクチャ

このプロジェクトは3つのエージェントによって自動生成されました：

- **Platform Architect Agent**: プロジェクト設計・技術選定
- **Frontend Developer Agent**: {frontend_framework} アプリケーション
- **Backend Developer Agent**: {backend_framework} API サーバー

## 🚀 クイックスタート

### 前提条件
- Node.js (v16以上)
- Docker & Docker Compose
- Git

### 開発環境セットアップ

```bash
# プロジェクトクローン
git clone <repository-url>
cd {self.project_name}

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
{self.project_name}/
├── frontend/           # {frontend_framework} アプリケーション
├── backend/            # {backend_framework} API サーバー
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
{chr(10).join([f"- {feature}" for feature in self.project_artifacts["frontend"]["code"]["features"]])}

### バックエンド
{chr(10).join([f"- {feature}" for feature in self.project_artifacts["backend"]["code"]["features"]])}

### API エンドポイント
{chr(10).join([f"- {endpoint}" for endpoint in self.project_artifacts["backend"]["code"]["endpoints"]])}

## 🚀 次のステップ

1. QA Agent による自動テスト生成
2. Deploy Agent による CI/CD 構築  
3. Security Agent によるセキュリティ監査
4. Performance Agent による最適化

---
*このプロジェクトはFull Agent Orchestratorによって自動生成されました*
'''
    
    def _generate_setup_script(self):
        """セットアップスクリプト生成"""
        return '''#!/bin/bash

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
'''
    
    def _generate_api_config(self):
        """API統合設定生成"""
        config = {
            "api_base_url": "http://localhost:5000/api",
            "frontend_url": "http://localhost:3000",
            "endpoints": self.project_artifacts["backend"]["code"]["endpoints"],
            "cors_config": {
                "allowed_origins": ["http://localhost:3000"],
                "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
                "allowed_headers": ["Content-Type", "Authorization"]
            },
            "authentication": {
                "type": "JWT",
                "header": "Authorization",
                "prefix": "Bearer"
            }
        }
        return json.dumps(config, indent=2)
    
    def _calculate_total_duration(self):
        """実行時間計算"""
        if len(self.workflow_history) < 2:
            return "< 1分"
        
        start_time = datetime.strptime(self.workflow_history[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(self.workflow_history[-1]["timestamp"], "%Y-%m-%d %H:%M:%S")
        duration = end_time - start_time
        
        return f"{duration.total_seconds():.1f}秒"


def main():
    """オーケストレーターのメイン実行関数"""
    print("🌟 Full Agent Orchestrator - 完全統合デモ")
    print("=" * 70)
    
    orchestrator = FullAgentOrchestrator()
    
    # デモ用のビジネス要件 (新しい要件に更新)
    business_requirement = "地域の農家と都市部のレストランを直接つなぐ、新鮮な食材のマッチングプラットフォーム。農家は収穫情報を投稿でき、レストランは必要な食材を検索・注文できる。"
    
    # 既存のプロジェクトがあれば削除してクリーンな状態から開始
    project_name = f"Secure_Project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    project_path = Path(f"full_stack_projects/{project_name}")
    if project_path.exists():
        import shutil
        shutil.rmtree(project_path)
        print(f"🗑️ 既存プロジェクト '{project_name}' をクリーンアップしました。")

    # 完全ワークフローの実行
    orchestrator.run_full_stack_workflow(business_requirement, project_name)


if __name__ == "__main__":
    main()
