#!/usr/bin/env python3
"""
Agent Orchestrator - エージェント間連携ワークフロー
Platform Architect Agent + Frontend Developer Agent の統合
"""
import os
import json
from datetime import datetime
from pathlib import Path

# 既存のエージェントをインポート
from frontend_developer_agent import FrontendDeveloperAgent

class AgentOrchestrator:
    """エージェント間の連携を管理するオーケストレータ"""
    
    def __init__(self):
        self.project_name = ""
        self.requirement = ""
        self.agents = {}
        self.workflow_history = []
        
    def initialize_project(self, requirement, project_name=None):
        """プロジェクトの初期化"""
        self.requirement = requirement
        self.project_name = project_name or f"Project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.workflow_history = []
        
        print(f"🚀 プロジェクト初期化: {self.project_name}")
        print(f"📋 要件: {requirement}")
        
    def run_platform_architect(self):
        """Platform Architect Agentの実行（簡易版）"""
        print(f"\n🏗️  Platform Architect Agent 実行中...")
        
        # 簡易的な設計書生成（実際のAgentと同等の処理）
        design_result = self._generate_project_design(self.requirement)
        
        self.workflow_history.append({
            "step": 1,
            "agent": "Platform Architect Agent", 
            "action": "プロジェクト設計書生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": design_result
        })
        
        print(f"✅ 設計書生成完了")
        print(f"🤖 生成エージェント数: {len(design_result['required_agents'])}")
        
        return design_result
    
    def run_frontend_agent(self, design_result):
        """Frontend Developer Agentの実行"""
        print(f"\n🎨 Frontend Developer Agent 実行中...")
        
        # 設計書からフロントエンド技術スタックを抽出
        tech_stack = design_result["project_overview"].get("technical_stack", ["React", "TypeScript"])
        
        # Frontend Developer Agentを初期化
        frontend_agent = FrontendDeveloperAgent()
        self.agents["frontend"] = frontend_agent
        
        # ログインページ生成
        generated_code = frontend_agent.generate_login_page(
            project_name=self.project_name,
            tech_stack=tech_stack
        )
        
        # コード保存
        output_dir = f"integrated_projects/{self.project_name}_frontend"
        project_dir = frontend_agent.save_generated_code(
            generated_code, 
            "LoginPage", 
            output_dir
        )
        
        self.workflow_history.append({
            "step": 2,
            "agent": "Frontend Developer Agent",
            "action": "ログインページコード生成",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "output": {
                "framework": generated_code["framework"],
                "features": generated_code["features"],
                "project_dir": project_dir
            }
        })
        
        print(f"✅ コード生成完了: {generated_code['framework']}")
        print(f"📁 保存先: {project_dir}")
        
        return generated_code, project_dir
    
    def generate_project_summary(self, design_result, frontend_result):
        """プロジェクト全体のサマリー生成"""
        print(f"\n📊 プロジェクトサマリー生成中...")
        
        summary = {
            "project_info": {
                "name": self.project_name,
                "requirement": self.requirement,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "design_phase": {
                "project_overview": design_result["project_overview"],
                "agents_designed": len(design_result["required_agents"]),
                "agent_list": [agent["agent_name"] for agent in design_result["required_agents"]]
            },
            "implementation_phase": {
                "frontend_framework": frontend_result[0]["framework"],
                "frontend_features": frontend_result[0]["features"],
                "code_location": frontend_result[1]
            },
            "workflow_history": self.workflow_history,
            "next_steps": [
                "Backend Developer Agentの実装",
                "データベース設計の自動化",
                "API設計書の生成",
                "テストコードの自動生成",
                "デプロイメントパイプラインの構築"
            ]
        }
        
        # サマリーファイル保存
        summary_dir = f"integrated_projects/{self.project_name}_summary"
        os.makedirs(summary_dir, exist_ok=True)
        
        with open(f"{summary_dir}/project_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # README生成
        readme_content = self._generate_project_readme(summary)
        with open(f"{summary_dir}/README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ サマリー保存完了: {summary_dir}")
        return summary
    
    def run_full_workflow(self, requirement, project_name=None):
        """完全なワークフローの実行"""
        print("🔄 完全ワークフロー開始")
        print("=" * 60)
        
        # 1. プロジェクト初期化
        self.initialize_project(requirement, project_name)
        
        # 2. Platform Architect Agent実行
        design_result = self.run_platform_architect()
        
        # 3. Frontend Developer Agent実行
        frontend_result = self.run_frontend_agent(design_result)
        
        # 4. プロジェクトサマリー生成
        summary = self.generate_project_summary(design_result, frontend_result)
        
        print("\n" + "=" * 60)
        print("🎉 ワークフロー完了!")
        print(f"📋 プロジェクト: {self.project_name}")
        print(f"🤖 実行エージェント: Platform Architect Agent → Frontend Developer Agent")
        print(f"📁 成果物ディレクトリ: integrated_projects/{self.project_name}_*")
        
        return summary
    
    def _generate_project_design(self, requirement):
        """プロジェクト設計書生成（Platform Architect Agentのロジック）"""
        if "ログイン" in requirement or "ブログ" in requirement:
            return {
                "project_overview": {
                    "name": "ログイン機能付きブログサイト",
                    "description": "ユーザー認証機能を持つ個人ブログプラットフォーム",
                    "technical_stack": ["React", "Node.js", "Express", "MongoDB", "JWT認証"],
                    "estimated_timeline": "8-10週間"
                },
                "required_agents": [
                    {
                        "agent_name": "Tech Lead Agent",
                        "agent_type": "tech_lead",
                        "responsibility": "技術アーキテクチャの設計と開発チームの技術的意思決定"
                    },
                    {
                        "agent_name": "Frontend Developer Agent",
                        "agent_type": "frontend_developer",
                        "responsibility": "ユーザーインターフェースとフロントエンド機能の実装"
                    },
                    {
                        "agent_name": "Backend Developer Agent", 
                        "agent_type": "backend_developer",
                        "responsibility": "サーバーサイドロジックとAPI開発"
                    }
                ]
            }
        elif "マッチング" in requirement:
            return {
                "project_overview": {
                    "name": "キャリア相談マッチングプラットフォーム",
                    "description": "専門家とメンティーをつなぐキャリア相談プラットフォーム",
                    "technical_stack": ["Vue.js", "Python", "Django", "PostgreSQL", "Redis"],
                    "estimated_timeline": "12-16週間"
                },
                "required_agents": [
                    {
                        "agent_name": "Business Analyst Agent",
                        "agent_type": "business_analyst", 
                        "responsibility": "業界要件分析とビジネスロジック設計"
                    },
                    {
                        "agent_name": "Frontend Developer Agent",
                        "agent_type": "frontend_developer",
                        "responsibility": "ユーザーインターフェースとフロントエンド機能の実装"
                    },
                    {
                        "agent_name": "Matching Algorithm Agent",
                        "agent_type": "algorithm_specialist",
                        "responsibility": "最適マッチングアルゴリズム開発"
                    }
                ]
            }
        else:
            return {
                "project_overview": {
                    "name": "カスタムWebアプリケーション",
                    "description": f"要件「{requirement}」に基づくWebアプリケーション",
                    "technical_stack": ["React", "Node.js", "MongoDB"],
                    "estimated_timeline": "6-10週間"
                },
                "required_agents": [
                    {
                        "agent_name": "Tech Lead Agent",
                        "agent_type": "tech_lead",
                        "responsibility": "技術的な意思決定とアーキテクチャ設計"
                    },
                    {
                        "agent_name": "Frontend Developer Agent",
                        "agent_type": "frontend_developer",
                        "responsibility": "フロントエンドとバックエンドの統合開発"
                    }
                ]
            }
    
    def _generate_project_readme(self, summary):
        """プロジェクトREADME生成"""
        return f'''# {summary["project_info"]["name"]}

**要件**: {summary["project_info"]["requirement"]}
**生成日時**: {summary["project_info"]["timestamp"]}

## 🏗️ プロジェクト概要

{summary["design_phase"]["project_overview"]["description"]}

**技術スタック**: {", ".join(summary["design_phase"]["project_overview"]["technical_stack"])}
**見積もり期間**: {summary["design_phase"]["project_overview"]["estimated_timeline"]}

## 🤖 エージェント設計

設計されたエージェント数: **{summary["design_phase"]["agents_designed"]}個**

{chr(10).join([f"- {agent}" for agent in summary["design_phase"]["agent_list"]])}

## 💻 実装状況

### フロントエンド
- **フレームワーク**: {summary["implementation_phase"]["frontend_framework"]}
- **機能**: {", ".join(summary["implementation_phase"]["frontend_features"])}
- **コード場所**: `{summary["implementation_phase"]["code_location"]}`

## 📋 ワークフロー履歴

{chr(10).join([f"{i+1}. **{step['agent']}** - {step['action']} ({step['timestamp']})" for i, step in enumerate(summary["workflow_history"])])}

## 🚀 次のステップ

{chr(10).join([f"- {step}" for step in summary["next_steps"]])}

---
*このプロジェクトはAgent Orchestratorによって自動生成されました*

## 🔧 開発環境セットアップ

### フロントエンド
```bash
cd {summary["implementation_phase"]["code_location"]}
npm install
npm start
```

### 推奨次ステップ
1. バックエンドAPI開発
2. データベース設計
3. 認証システム実装
4. テスト環境構築
'''


def demo_agent_orchestrator():
    """Agent Orchestratorのデモ"""
    print("🔄 Agent Orchestrator - エージェント連携デモ")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator()
    
    # テストケース
    test_requirements = [
        "ログイン機能付きのブログサイト",
        "電気工事士向けのキャリア相談ができるマッチングプラットフォーム"
    ]
    
    for i, requirement in enumerate(test_requirements, 1):
        print(f"\n🧪 テストケース {i}: {requirement}")
        print("-" * 60)
        
        project_name = f"IntegratedProject_{i}"
        summary = orchestrator.run_full_workflow(requirement, project_name)
        
        print(f"\n📊 完了サマリー:")
        print(f"   フレームワーク: {summary['implementation_phase']['frontend_framework']}")
        print(f"   エージェント数: {summary['design_phase']['agents_designed']}")
        print(f"   ワークフロー: {len(summary['workflow_history'])}ステップ")
        
        if i < len(test_requirements):
            print("\n" + "="*60)


if __name__ == "__main__":
    demo_agent_orchestrator()
