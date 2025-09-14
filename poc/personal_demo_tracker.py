#!/usr/bin/env python3
"""
個人デモ実行トラッカー
ユーザーのデモ実行結果を追跡・分析するツール
"""
import os
import json
import time
from datetime import datetime

class PersonalDemoTracker:
    """個人デモ実行の追跡と分析"""
    
    def __init__(self):
        self.demo_start_time = datetime.now()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []
        
    def monitor_generated_projects(self):
        """生成されたプロジェクトを監視"""
        print("🔍 生成されたプロジェクトを監視中...")
        
        # 生成ディレクトリのチェック
        directories_to_monitor = [
            'generated_agents',
            'generated_code', 
            'generated_backend',
            'integrated_projects',
            'full_stack_projects'
        ]
        
        initial_state = {}
        for directory in directories_to_monitor:
            if os.path.exists(directory):
                initial_state[directory] = self._get_directory_contents(directory)
            else:
                initial_state[directory] = []
        
        print(f"📊 初期状態記録完了: {sum(len(v) for v in initial_state.values())}ファイル")
        
        return initial_state
    
    def check_for_new_results(self, initial_state):
        """新しい生成結果をチェック"""
        new_results = {}
        
        for directory, initial_files in initial_state.items():
            if os.path.exists(directory):
                current_files = self._get_directory_contents(directory)
                new_files = [f for f in current_files if f not in initial_files]
                if new_files:
                    new_results[directory] = new_files
        
        return new_results
    
    def analyze_demo_results(self, user_input="Unknown", execution_time=0):
        """デモ結果の分析"""
        print(f"\n🎯 個人デモ実行結果分析")
        print("=" * 50)
        
        analysis = {
            "session_info": {
                "session_id": self.session_id,
                "user_input": user_input,
                "execution_time_seconds": execution_time,
                "timestamp": datetime.now().isoformat()
            },
            "generated_content": {},
            "quality_metrics": {},
            "user_experience": {}
        }
        
        # 生成されたエージェント分析
        if os.path.exists('generated_agents'):
            agent_files = [f for f in os.listdir('generated_agents') if f.endswith('.md')]
            analysis["generated_content"]["agents"] = {
                "count": len(agent_files),
                "files": agent_files
            }
            print(f"🤖 生成エージェント: {len(agent_files)}個")
            
            # エージェント詳細分析
            for agent_file in agent_files:
                agent_path = f"generated_agents/{agent_file}"
                try:
                    with open(agent_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        analysis["generated_content"][agent_file] = {
                            "size_chars": len(content),
                            "lines": len(content.split('\n')),
                            "has_responsibilities": "## 責任範囲" in content,
                            "has_autonomy": "自律レベル" in content
                        }
                except Exception as e:
                    print(f"⚠️ {agent_file}読み込みエラー: {e}")
        
        # フルスタックプロジェクト分析
        if os.path.exists('full_stack_projects'):
            projects = [d for d in os.listdir('full_stack_projects') if os.path.isdir(f'full_stack_projects/{d}')]
            analysis["generated_content"]["full_stack_projects"] = {
                "count": len(projects),
                "projects": projects
            }
            print(f"🏗️ フルスタックプロジェクト: {len(projects)}個")
            
            # 最新プロジェクトの詳細分析
            if projects:
                latest_project = projects[-1]
                project_path = f"full_stack_projects/{latest_project}"
                analysis["generated_content"]["latest_project"] = self._analyze_project_structure(project_path)
        
        # 品質メトリクス計算
        analysis["quality_metrics"] = self._calculate_quality_metrics(analysis["generated_content"])
        
        # ユーザーエクスペリエンス評価
        analysis["user_experience"] = {
            "ease_of_use": "Excellent" if execution_time < 10 else "Good",
            "speed": "Lightning Fast" if execution_time < 5 else "Fast",
            "completeness": self._assess_completeness(analysis["generated_content"]),
            "recommendation": self._generate_recommendation(analysis)
        }
        
        # 結果保存
        report_filename = f"personal_demo_report_{self.session_id}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print(f"💾 分析レポート保存: {report_filename}")
        
        return analysis
    
    def _get_directory_contents(self, directory):
        """ディレクトリ内容取得"""
        contents = []
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), directory)
                    contents.append(rel_path)
        except Exception:
            pass
        return contents
    
    def _analyze_project_structure(self, project_path):
        """プロジェクト構造分析"""
        structure = {
            "has_frontend": False,
            "has_backend": False,
            "has_docker": False,
            "has_documentation": False,
            "total_files": 0
        }
        
        try:
            for root, dirs, files in os.walk(project_path):
                structure["total_files"] += len(files)
                
                for file in files:
                    if file.endswith(('.tsx', '.jsx', '.vue', '.html')):
                        structure["has_frontend"] = True
                    elif file.endswith(('.js', '.py', '.java')) and 'server' in file.lower():
                        structure["has_backend"] = True
                    elif file == 'docker-compose.yml' or file == 'Dockerfile':
                        structure["has_docker"] = True
                    elif file.endswith(('.md', '.txt')) and 'readme' in file.lower():
                        structure["has_documentation"] = True
        except Exception:
            pass
        
        return structure
    
    def _calculate_quality_metrics(self, generated_content):
        """品質メトリクス計算"""
        metrics = {
            "completeness_score": 0,
            "technical_coverage": 0,
            "documentation_quality": 0,
            "overall_rating": "Pending"
        }
        
        # 完全性スコア
        completeness_factors = []
        if generated_content.get("agents", {}).get("count", 0) > 0:
            completeness_factors.append(30)  # エージェント生成
        if generated_content.get("full_stack_projects", {}).get("count", 0) > 0:
            completeness_factors.append(40)  # フルスタック生成
        
        latest_project = generated_content.get("latest_project", {})
        if latest_project.get("has_frontend"):
            completeness_factors.append(10)
        if latest_project.get("has_backend"):
            completeness_factors.append(10)
        if latest_project.get("has_docker"):
            completeness_factors.append(5)
        if latest_project.get("has_documentation"):
            completeness_factors.append(5)
        
        metrics["completeness_score"] = sum(completeness_factors)
        
        # 技術カバレッジ
        tech_coverage = 0
        if latest_project.get("has_frontend") and latest_project.get("has_backend"):
            tech_coverage = 85
        elif latest_project.get("has_frontend") or latest_project.get("has_backend"):
            tech_coverage = 60
        
        metrics["technical_coverage"] = tech_coverage
        
        # ドキュメント品質
        doc_quality = 70 if latest_project.get("has_documentation") else 40
        metrics["documentation_quality"] = doc_quality
        
        # 総合評価
        overall_score = (metrics["completeness_score"] + tech_coverage + doc_quality) / 3
        if overall_score >= 80:
            metrics["overall_rating"] = "Excellent"
        elif overall_score >= 60:
            metrics["overall_rating"] = "Good"
        else:
            metrics["overall_rating"] = "Needs Improvement"
        
        return metrics
    
    def _assess_completeness(self, generated_content):
        """完全性評価"""
        if generated_content.get("full_stack_projects", {}).get("count", 0) > 0:
            return "Complete Full-Stack Solution"
        elif generated_content.get("agents", {}).get("count", 0) >= 3:
            return "Comprehensive Agent Design"
        elif generated_content.get("agents", {}).get("count", 0) > 0:
            return "Basic Agent Generation"
        else:
            return "Minimal Output"
    
    def _generate_recommendation(self, analysis):
        """推奨事項生成"""
        quality = analysis["quality_metrics"]["overall_rating"]
        
        if quality == "Excellent":
            return "即座に本格プロジェクトで活用可能。チーム展開を推奨。"
        elif quality == "Good":
            return "軽微なカスタマイズで実用可能。追加機能検討を推奨。"
        else:
            return "基本機能確認完了。より詳細な要件での再実行を推奨。"
    
    def display_interactive_summary(self, analysis):
        """インタラクティブサマリー表示"""
        print(f"\n🎉 個人デモ実行完了サマリー")
        print("=" * 60)
        
        session = analysis["session_info"]
        print(f"📅 実行日時: {session['timestamp'][:19]}")
        print(f"⏱️ 実行時間: {session['execution_time_seconds']}秒")
        print(f"📝 入力要件: {session['user_input']}")
        
        print(f"\n🎯 生成結果:")
        content = analysis["generated_content"]
        print(f"   🤖 エージェント: {content.get('agents', {}).get('count', 0)}個")
        print(f"   🏗️ フルスタックプロジェクト: {content.get('full_stack_projects', {}).get('count', 0)}個")
        
        print(f"\n📊 品質評価:")
        quality = analysis["quality_metrics"]
        print(f"   完全性: {quality['completeness_score']}/100")
        print(f"   技術カバレッジ: {quality['technical_coverage']}%")
        print(f"   総合評価: {quality['overall_rating']}")
        
        print(f"\n💡 ユーザーエクスペリエンス:")
        ux = analysis["user_experience"]
        print(f"   使いやすさ: {ux['ease_of_use']}")
        print(f"   速度: {ux['speed']}")
        print(f"   完全性: {ux['completeness']}")
        print(f"   推奨: {ux['recommendation']}")
        
        print(f"\n🚀 次のステップ提案:")
        if quality['overall_rating'] == 'Excellent':
            print(f"   ✅ チーム全体での評価・導入検討")
            print(f"   ✅ より大規模なプロジェクトでの実証")
            print(f"   ✅ 経営陣への成果報告")
        elif quality['overall_rating'] == 'Good':
            print(f"   🔄 追加機能・カスタマイズの検討")
            print(f"   📋 他の要件パターンでの再実行")
            print(f"   👥 チームメンバーとの結果共有")
        else:
            print(f"   🔍 より詳細な要件での再挑戦")
            print(f"   📚 使用方法・ベストプラクティスの確認")
            print(f"   🤝 サポートチームへの相談")


def main():
    """メイン実行"""
    tracker = PersonalDemoTracker()
    
    print("🚀 個人デモ実行トラッカー開始")
    print("現在のデモ実行を監視・分析します...")
    
    # 初期状態記録
    initial_state = tracker.monitor_generated_projects()
    
    print("\n⏳ Platform Architect Agentでのデモ実行を継続してください...")
    print("デモ完了後、このスクリプトで結果分析を実行します。")
    
    input("デモ完了後、Enterキーを押してください...")
    
    # 結果チェック
    new_results = tracker.check_for_new_results(initial_state)
    
    if new_results:
        print(f"\n✅ 新しい生成結果を検出: {len(new_results)}カテゴリ")
        for category, files in new_results.items():
            print(f"   📁 {category}: {len(files)}ファイル")
    
    # 分析実行
    user_input = input("\n📝 入力した要件を教えてください（分析に使用）: ")
    execution_time = float(input("⏱️ デモ実行時間（秒）を教えてください: ") or "0")
    
    analysis = tracker.analyze_demo_results(user_input, execution_time)
    tracker.display_interactive_summary(analysis)
    
    print(f"\n🎊 お疲れ様でした！Platform Architect Agentの革新的な力を体験していただきました！")


if __name__ == "__main__":
    main()
