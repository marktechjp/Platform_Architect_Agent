#!/usr/bin/env python3
"""
Platform Architect Agent - スタンドアロンデモ
.envファイルなしで直接実行できるデモ版
"""
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

class SimpleMockLLM:
    """シンプルなデモ用モックLLMクラス"""
    
    def generate_response(self, requirement):
        """要件に基づいてレスポンスを生成"""
        if "ログイン" in requirement or "ブログ" in requirement:
            return self._generate_blog_response()
        elif "マッチング" in requirement or "相談" in requirement:
            return self._generate_matching_response()
        elif "書店" in requirement or "EC" in requirement:
            return self._generate_ecommerce_response()
        else:
            return self._generate_generic_response(requirement)
    
    def _generate_blog_response(self):
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
                    "responsibility": "技術アーキテクチャの設計と開発チームの技術的意思決定",
                    "skills": ["システム設計", "技術選定", "チームリーダーシップ", "コードレビュー"],
                    "autonomy_level": "L2",
                    "main_functions": ["アーキテクチャ設計", "技術標準策定", "コードレビュー", "技術課題解決"],
                    "data_sources": ["技術ドキュメント", "業界ベストプラクティス", "パフォーマンス指標"],
                    "kpis": ["コード品質スコア", "技術的負債削減率", "チーム生産性向上"]
                },
                {
                    "agent_name": "Frontend Developer Agent",
                    "agent_type": "frontend_developer",
                    "responsibility": "ユーザーインターフェースとフロントエンド機能の実装",
                    "skills": ["React", "TypeScript", "CSS", "レスポンシブデザイン", "アクセシビリティ"],
                    "autonomy_level": "L2",
                    "main_functions": ["UI/UXコンポーネント開発", "状態管理実装", "APIクライアント実装", "テスト作成"],
                    "data_sources": ["デザインシステム", "UIライブラリ", "ユーザビリティガイドライン"],
                    "kpis": ["UI開発速度", "コンポーネント再利用率", "アクセシビリティスコア"]
                },
                {
                    "agent_name": "Backend Developer Agent",
                    "agent_type": "backend_developer",
                    "responsibility": "サーバーサイドロジックとAPI開発",
                    "skills": ["Node.js", "Express", "MongoDB", "認証システム", "REST API"],
                    "autonomy_level": "L2",
                    "main_functions": ["API開発", "データベース設計", "認証機能実装", "セキュリティ実装"],
                    "data_sources": ["APIドキュメント", "データベーススキーマ", "セキュリティガイドライン"],
                    "kpis": ["API応答時間", "セキュリティ脆弱性数", "データベースパフォーマンス"]
                }
            ]
        }

    def _generate_matching_response(self):
        return {
            "project_overview": {
                "name": "電気工事士向けキャリア相談マッチングプラットフォーム",
                "description": "電気工事士と経験豊富なメンターをつなぐキャリア相談プラットフォーム",
                "technical_stack": ["Vue.js", "Python", "Django", "PostgreSQL", "Redis", "WebRTC"],
                "estimated_timeline": "12-16週間"
            },
            "required_agents": [
                {
                    "agent_name": "Business Analyst Agent",
                    "agent_type": "business_analyst",
                    "responsibility": "業界要件分析とビジネスロジック設計",
                    "skills": ["業界知識", "要件分析", "ビジネスプロセス設計", "データ分析"],
                    "autonomy_level": "L3",
                    "main_functions": ["業界調査", "ユーザーニーズ分析", "ビジネスモデル検証", "KPI定義"],
                    "data_sources": ["業界レポート", "ユーザーフィードバック", "競合分析データ"],
                    "kpis": ["要件充足率", "ユーザー満足度", "ビジネス目標達成率"]
                },
                {
                    "agent_name": "Matching Algorithm Agent",
                    "agent_type": "algorithm_specialist",
                    "responsibility": "メンターとメンティーの最適マッチングアルゴリズム開発",
                    "skills": ["機械学習", "レコメンデーションシステム", "データサイエンス", "統計学"],
                    "autonomy_level": "L2",
                    "main_functions": ["マッチングアルゴリズム設計", "推薦精度改善", "A/Bテスト実施", "パフォーマンス最適化"],
                    "data_sources": ["ユーザープロファイル", "マッチング履歴", "フィードバックデータ"],
                    "kpis": ["マッチング成功率", "ユーザー継続率", "推薦精度スコア"]
                },
                {
                    "agent_name": "Communication System Agent",
                    "agent_type": "communication_specialist",
                    "responsibility": "リアルタイム通信機能とビデオ通話システムの実装",
                    "skills": ["WebRTC", "チャットシステム", "リアルタイム通信", "動画配信技術"],
                    "autonomy_level": "L2",
                    "main_functions": ["ビデオ通話実装", "チャット機能開発", "ファイル共有機能", "通話品質管理"],
                    "data_sources": ["通話品質データ", "ネットワーク統計", "ユーザー利用パターン"],
                    "kpis": ["通話成功率", "音質・画質スコア", "接続安定性"]
                }
            ]
        }

    def _generate_ecommerce_response(self):
        return {
            "project_overview": {
                "name": "オンライン書店Webアプリケーション",
                "description": "本の検索・購入・レビュー機能を持つECサイト",
                "technical_stack": ["React", "Python", "FastAPI", "PostgreSQL", "Stripe"],
                "estimated_timeline": "10-14週間"
            },
            "required_agents": [
                {
                    "agent_name": "E-commerce Specialist Agent",
                    "agent_type": "ecommerce_specialist",
                    "responsibility": "EC機能とビジネスロジック設計",
                    "skills": ["EC設計", "決済システム", "在庫管理", "顧客体験設計"],
                    "autonomy_level": "L2",
                    "main_functions": ["商品管理機能設計", "決済フロー実装", "レビューシステム構築", "在庫管理"],
                    "data_sources": ["EC業界ベストプラクティス", "決済プロバイダAPI", "顧客行動データ"],
                    "kpis": ["変換率", "平均注文金額", "顧客満足度"]
                },
                {
                    "agent_name": "Search & Recommendation Agent",
                    "agent_type": "search_specialist",
                    "responsibility": "書籍検索とレコメンデーション機能",
                    "skills": ["検索エンジン", "推薦アルゴリズム", "自然言語処理", "データマイニング"],
                    "autonomy_level": "L2",
                    "main_functions": ["検索機能実装", "推薦システム構築", "フィルタリング機能", "類似商品提案"],
                    "data_sources": ["書籍メタデータ", "ユーザー検索履歴", "購入履歴"],
                    "kpis": ["検索成功率", "推薦クリック率", "検索→購入転換率"]
                },
                {
                    "agent_name": "Payment & Security Agent",
                    "agent_type": "security_specialist",
                    "responsibility": "決済処理とセキュリティ実装",
                    "skills": ["決済システム", "セキュリティ", "PCI DSS", "不正検知"],
                    "autonomy_level": "L3",
                    "main_functions": ["決済処理実装", "セキュリティ監査", "不正取引検知", "データ暗号化"],
                    "data_sources": ["決済ログ", "セキュリティイベント", "不正検知パターン"],
                    "kpis": ["決済成功率", "セキュリティインシデント数", "不正検知精度"]
                }
            ]
        }

    def _generate_generic_response(self, requirement):
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
                    "responsibility": "技術的な意思決定とアーキテクチャ設計",
                    "skills": ["システム設計", "技術選定", "チームリーダーシップ"],
                    "autonomy_level": "L2",
                    "main_functions": ["アーキテクチャ設計", "技術標準策定", "コードレビュー"],
                    "data_sources": ["技術ドキュメント", "ベストプラクティス"],
                    "kpis": ["コード品質スコア", "技術的負債削減率"]
                },
                {
                    "agent_name": "Full Stack Developer Agent",
                    "agent_type": "fullstack_developer",
                    "responsibility": "フロントエンドとバックエンドの統合開発",
                    "skills": ["JavaScript", "React", "Node.js", "データベース設計"],
                    "autonomy_level": "L2",
                    "main_functions": ["フルスタック開発", "API設計", "UI実装"],
                    "data_sources": ["API仕様", "UIデザイン", "データベーススキーマ"],
                    "kpis": ["開発速度", "バグ発生率", "コード再利用率"]
                }
            ]
        }

# モックLLMインスタンス
mock_llm = SimpleMockLLM()

def save_generated_designs(design_data, timestamp, requirement):
    """生成された設計書をファイルに保存する"""
    try:
        # 出力ディレクトリを作成
        output_dir = "generated_agents"
        os.makedirs(output_dir, exist_ok=True)
        
        # プロジェクト概要ファイルを保存
        project_file = f"{output_dir}/project_overview_{timestamp}.json"
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "business_requirement": requirement,
                "project_overview": design_data.get("project_overview", {}),
                "agents_count": len(design_data.get("required_agents", []))
            }, f, ensure_ascii=False, indent=2)
        
        # 各エージェントの設計書を個別のMarkdownファイルとして保存
        for agent in design_data.get("required_agents", []):
            agent_name = agent.get("agent_name", "Unknown Agent")
            safe_name = agent_name.replace(" ", "_").replace("/", "_")
            
            agent_file = f"{output_dir}/{safe_name}_{timestamp}.md"
            with open(agent_file, 'w', encoding='utf-8') as f:
                f.write(generate_agent_markdown(agent, timestamp, requirement))
        
        print(f"Generated design documents saved in {output_dir}/")
        return len(design_data.get("required_agents", []))
        
    except Exception as e:
        print(f"Error saving generated designs: {e}")
        return 0


def generate_agent_markdown(agent_data, timestamp, requirement):
    """エージェントデータからMarkdown形式の設計書を生成する"""
    markdown = f"""# {agent_data.get('agent_name', 'Unknown Agent')}

- **バージョン**: 1.0
- **生成日時**: {timestamp}
- **元要件**: {requirement}

## 1. 目的 (Goal)
- **責任範囲**: {agent_data.get('responsibility', 'Not specified')}

## 2. 自律レベル (Autonomy Level)
- **レベル**: {agent_data.get('autonomy_level', 'L2')}

## 3. 主要機能
"""
    
    for func in agent_data.get('main_functions', []):
        markdown += f"- {func}\n"
    
    markdown += f"""
## 4. 必要スキル
"""
    
    for skill in agent_data.get('skills', []):
        markdown += f"- {skill}\n"
    
    markdown += f"""
## 5. データソース
"""
    
    for data_source in agent_data.get('data_sources', []):
        markdown += f"- {data_source}\n"
    
    markdown += f"""
## 6. KPI (Key Performance Indicators)
"""
    
    for kpi in agent_data.get('kpis', []):
        markdown += f"- {kpi}\n"
    
    markdown += f"""
---
*この設計書はPlatform Architect Agent（デモ版）によって自動生成されました*
"""
    
    return markdown


def run_interactive_demo():
    """対話式デモの実行"""
    print("🏗️  Platform Architect Agent - インタラクティブデモ")
    print("=" * 60)
    print("ビジネス要件を入力すると、必要な子エージェントの設計書を自動生成します。")
    print()
    
    # サンプル要件
    samples = [
        "ログイン機能付きのブログサイト",
        "電気工事士向けのキャリア相談ができるマッチングプラットフォーム",
        "オンライン書店のWebアプリケーション"
    ]
    
    print("サンプル要件:")
    for i, sample in enumerate(samples, 1):
        print(f"  {i}. {sample}")
    print()
    
    while True:
        try:
            # ユーザー入力
            print("要件を入力してください（'quit'で終了）:")
            choice = input("> ").strip()
            
            if choice.lower() in ['quit', 'q', 'exit']:
                print("デモを終了します。")
                break
            
            # 数字が入力された場合はサンプルを使用
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(samples):
                    requirement = samples[idx]
                else:
                    print("無効な番号です。")
                    continue
            else:
                requirement = choice
            
            if not requirement:
                print("要件が空です。再入力してください。")
                continue
            
            print(f"\n📋 処理中: {requirement}")
            print("-" * 40)
            
            # エージェント設計書生成
            design_data = mock_llm.generate_response(requirement)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 結果表示
            overview = design_data.get("project_overview", {})
            agents = design_data.get("required_agents", [])
            
            print(f"✅ プロジェクト名: {overview.get('name')}")
            print(f"📝 概要: {overview.get('description')}")
            print(f"🛠️  技術スタック: {', '.join(overview.get('technical_stack', []))}")
            print(f"⏱️  見積もり期間: {overview.get('estimated_timeline')}")
            print()
            
            print(f"🤖 生成されたエージェント ({len(agents)}個):")
            for i, agent in enumerate(agents, 1):
                print(f"  {i}. {agent.get('agent_name')}")
                print(f"     責任範囲: {agent.get('responsibility')}")
                print(f"     自律レベル: {agent.get('autonomy_level')}")
                print()
            
            # ファイル保存
            saved_count = save_generated_designs(design_data, timestamp, requirement)
            print(f"💾 {saved_count}個のエージェント設計書をgenerated_agents/に保存しました")
            print("=" * 60)
            print()
            
        except KeyboardInterrupt:
            print("\nデモを終了します。")
            break
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            print()


if __name__ == "__main__":
    print("Platform Architect Agent - デモ版")
    print("複数の実行モードを選択できます:")
    print("1. インタラクティブデモ (推奨)")
    print("2. Webサーバーモード")
    print()
    
    mode = input("実行モードを選択してください (1 or 2): ").strip()
    
    if mode == "1":
        run_interactive_demo()
    elif mode == "2":
        # Webサーバーモード
        @app.route("/", methods=["POST"])
        def generate_design_document():
            try:
                data = request.get_json()
                if not data or "requirement" not in data:
                    return jsonify({"error": "Missing 'requirement' in request body"}), 400
                
                business_requirement = data["requirement"]
                print(f"Received requirement: {business_requirement}")

                design_data = mock_llm.generate_response(business_requirement)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_generated_designs(design_data, timestamp, business_requirement)
                
                return jsonify({
                    "success": True,
                    "timestamp": timestamp,
                    "business_requirement": business_requirement,
                    "generated_design": design_data,
                    "mode": "demo_standalone"
                }), 200
                    
            except Exception as e:
                print(f"Error in generate_design_document: {e}")
                return jsonify({"error": f"Internal server error: {str(e)}"}), 500

        @app.route("/health", methods=["GET"])
        def health_check():
            return jsonify({"status": "healthy", "mode": "demo_standalone"}), 200
        
        port = 8080
        print(f"🌐 Webサーバーを起動中... ポート: {port}")
        print(f"ヘルスチェック: http://localhost:{port}/health")
        app.run(debug=True, host="0.0.0.0", port=port)
    else:
        print("無効な選択です。インタラクティブデモを実行します。")
        run_interactive_demo()
