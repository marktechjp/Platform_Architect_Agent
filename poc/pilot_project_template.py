#!/usr/bin/env python3
"""
パイロットプロジェクト実行テンプレート
社内での実際のプロジェクト適用用
"""
import os
import json
from datetime import datetime
from pathlib import Path

# 既存のオーケストレータをインポート
from full_agent_orchestrator import FullAgentOrchestrator

class PilotProjectManager:
    """パイロットプロジェクト管理クラス"""
    
    def __init__(self):
        self.orchestrator = FullAgentOrchestrator()
        self.pilot_data = {}
        
    def run_pilot_project(self, project_info):
        """パイロットプロジェクトの実行"""
        print("🚀 社内パイロットプロジェクト開始")
        print("=" * 60)
        
        # プロジェクト情報の記録
        self.pilot_data = {
            "project_info": project_info,
            "start_time": datetime.now(),
            "phases": []
        }
        
        # フェーズ1: 要件分析・検証
        self._phase1_requirement_analysis(project_info)
        
        # フェーズ2: 自動生成実行
        self._phase2_generation(project_info)
        
        # フェーズ3: 品質検証
        self._phase3_quality_verification()
        
        # フェーズ4: 実証・レポート
        self._phase4_validation_report()
        
        return self.pilot_data
    
    def _phase1_requirement_analysis(self, project_info):
        """フェーズ1: 要件分析・検証"""
        print("\n📋 Phase 1: 要件分析・検証")
        print("-" * 40)
        
        phase_start = datetime.now()
        
        # 要件の妥当性チェック
        requirement = project_info["requirement"]
        stakeholder = project_info.get("stakeholder", "Unknown")
        priority = project_info.get("priority", "Medium")
        
        print(f"要件: {requirement}")
        print(f"ステークホルダー: {stakeholder}")
        print(f"優先度: {priority}")
        
        # 要件分析結果
        analysis_result = {
            "requirement_clarity": self._analyze_requirement_clarity(requirement),
            "technical_feasibility": "High",
            "estimated_complexity": self._estimate_complexity(requirement),
            "recommended_approach": "Full Agent Orchestrator"
        }
        
        phase_end = datetime.now()
        
        self.pilot_data["phases"].append({
            "phase": 1,
            "name": "要件分析・検証",
            "start_time": phase_start,
            "end_time": phase_end,
            "duration_minutes": (phase_end - phase_start).total_seconds() / 60,
            "result": analysis_result,
            "status": "completed"
        })
        
        print(f"✅ 要件分析完了 - 複雑度: {analysis_result['estimated_complexity']}")
    
    def _phase2_generation(self, project_info):
        """フェーズ2: 自動生成実行"""
        print("\n🏗️ Phase 2: 自動生成実行")
        print("-" * 40)
        
        phase_start = datetime.now()
        
        # Full Agent Orchestratorでの生成
        requirement = project_info["requirement"]
        project_name = project_info.get("project_name") or f"PilotProject_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            generation_result = self.orchestrator.run_full_stack_workflow(
                requirement=requirement,
                project_name=project_name
            )
            
            phase_end = datetime.now()
            
            self.pilot_data["phases"].append({
                "phase": 2,
                "name": "自動生成実行",
                "start_time": phase_start,
                "end_time": phase_end,
                "duration_minutes": (phase_end - phase_start).total_seconds() / 60,
                "result": {
                    "success": True,
                    "project_name": project_name,
                    "generated_components": {
                        "frontend": generation_result["architecture"]["frontend"]["framework"],
                        "backend": generation_result["architecture"]["backend"]["framework"],
                        "integration": "Docker Compose + 統合ツール"
                    },
                    "agents_executed": generation_result["workflow_summary"]["agents_involved"],
                    "execution_steps": generation_result["workflow_summary"]["total_steps"]
                },
                "status": "completed"
            })
            
            print(f"✅ 自動生成完了 - プロジェクト: {project_name}")
            
        except Exception as e:
            phase_end = datetime.now()
            
            self.pilot_data["phases"].append({
                "phase": 2,
                "name": "自動生成実行",
                "start_time": phase_start,
                "end_time": phase_end,
                "duration_minutes": (phase_end - phase_start).total_seconds() / 60,
                "result": {
                    "success": False,
                    "error": str(e)
                },
                "status": "failed"
            })
            
            print(f"❌ 自動生成エラー: {e}")
    
    def _phase3_quality_verification(self):
        """フェーズ3: 品質検証"""
        print("\n🔍 Phase 3: 品質検証")
        print("-" * 40)
        
        phase_start = datetime.now()
        
        # システム実証テストの実行
        try:
            from system_verification_test import SystemVerificationTest
            
            tester = SystemVerificationTest()
            verification_results = tester.run_full_verification()
            
            # 結果サマリー
            total_tests = len(verification_results)
            passed_tests = sum(1 for result in verification_results if result["passed"])
            success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            phase_end = datetime.now()
            
            self.pilot_data["phases"].append({
                "phase": 3,
                "name": "品質検証",
                "start_time": phase_start,
                "end_time": phase_end,
                "duration_minutes": (phase_end - phase_start).total_seconds() / 60,
                "result": {
                    "success": True,
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "success_rate": success_rate,
                    "assessment": self._get_quality_assessment(success_rate)
                },
                "status": "completed"
            })
            
            print(f"✅ 品質検証完了 - 成功率: {success_rate:.1f}%")
            
        except Exception as e:
            phase_end = datetime.now()
            
            self.pilot_data["phases"].append({
                "phase": 3,
                "name": "品質検証",
                "start_time": phase_start,
                "end_time": phase_end,
                "duration_minutes": (phase_end - phase_start).total_seconds() / 60,
                "result": {
                    "success": False,
                    "error": str(e)
                },
                "status": "failed"
            })
            
            print(f"❌ 品質検証エラー: {e}")
    
    def _phase4_validation_report(self):
        """フェーズ4: 実証・レポート"""
        print("\n📊 Phase 4: 実証・レポート生成")
        print("-" * 40)
        
        phase_start = datetime.now()
        
        # 総合評価の生成
        total_duration = (datetime.now() - self.pilot_data["start_time"]).total_seconds() / 60
        
        # 成功フェーズ数の計算
        successful_phases = sum(1 for phase in self.pilot_data["phases"] if phase["status"] == "completed")
        total_phases = len(self.pilot_data["phases"])
        
        # ROI計算（従来開発との比較）
        traditional_estimate = self._estimate_traditional_development_time()
        ai_driven_time = total_duration
        time_saving = ((traditional_estimate - ai_driven_time) / traditional_estimate * 100) if traditional_estimate > 0 else 0
        
        evaluation = {
            "overall_success": successful_phases == total_phases,
            "total_duration_minutes": total_duration,
            "successful_phases": f"{successful_phases}/{total_phases}",
            "roi_analysis": {
                "traditional_estimate_hours": traditional_estimate,
                "actual_time_hours": ai_driven_time / 60,
                "time_saving_percentage": time_saving,
                "estimated_cost_saving": self._calculate_cost_saving(time_saving)
            },
            "recommendations": self._generate_recommendations()
        }
        
        phase_end = datetime.now()
        
        self.pilot_data["phases"].append({
            "phase": 4,
            "name": "実証・レポート",
            "start_time": phase_start,
            "end_time": phase_end,
            "duration_minutes": (phase_end - phase_start).total_seconds() / 60,
            "result": evaluation,
            "status": "completed"
        })
        
        # レポートファイル保存
        self._save_pilot_report()
        
        print(f"✅ パイロットプロジェクト完了")
        print(f"   成功率: {successful_phases}/{total_phases} フェーズ")
        print(f"   時間短縮: {time_saving:.1f}%")
        print(f"   総所要時間: {total_duration:.1f}分")
    
    def _analyze_requirement_clarity(self, requirement):
        """要件の明確性分析"""
        keywords = ["機能", "ユーザー", "システム", "管理", "処理", "画面", "API"]
        clarity_score = sum(1 for keyword in keywords if keyword in requirement)
        
        if clarity_score >= 4:
            return "High"
        elif clarity_score >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _estimate_complexity(self, requirement):
        """複雑度推定"""
        complex_keywords = ["管理", "認証", "決済", "検索", "マッチング", "レポート", "分析"]
        complexity_score = sum(1 for keyword in complex_keywords if keyword in requirement)
        
        if complexity_score >= 3:
            return "High"
        elif complexity_score >= 1:
            return "Medium"
        else:
            return "Low"
    
    def _get_quality_assessment(self, success_rate):
        """品質評価"""
        if success_rate >= 90:
            return "Excellent"
        elif success_rate >= 80:
            return "Good"
        elif success_rate >= 70:
            return "Acceptable"
        else:
            return "Needs Improvement"
    
    def _estimate_traditional_development_time(self):
        """従来開発時間の推定（時間）"""
        complexity = self.pilot_data["phases"][0]["result"]["estimated_complexity"]
        
        if complexity == "High":
            return 320  # 8週間 * 40時間
        elif complexity == "Medium":
            return 160  # 4週間 * 40時間
        else:
            return 80   # 2週間 * 40時間
    
    def _calculate_cost_saving(self, time_saving_percentage):
        """コスト削減計算"""
        # 仮定: 開発者時給 5000円
        traditional_hours = self._estimate_traditional_development_time()
        saved_hours = traditional_hours * (time_saving_percentage / 100)
        cost_saving = saved_hours * 5000
        
        return {
            "saved_hours": saved_hours,
            "cost_saving_yen": int(cost_saving),
            "cost_saving_formatted": f"¥{cost_saving:,.0f}"
        }
    
    def _generate_recommendations(self):
        """推奨事項生成"""
        return [
            "本格的な社内展開を推奨",
            "開発チーム向けトレーニング実施",
            "追加エージェント（QA/Security）の導入検討",
            "継続的なフィードバック収集とプロセス改善"
        ]
    
    def _save_pilot_report(self):
        """パイロットレポート保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"pilot_project_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.pilot_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"📄 パイロットレポート保存: {report_file}")


def run_sample_pilot():
    """サンプルパイロットプロジェクトの実行"""
    
    # 社内プロジェクト例
    sample_projects = [
        {
            "project_name": "EmployeeTimeTracker",
            "requirement": "社員の勤怠管理・有給申請・承認ワークフローができるWebアプリケーション",
            "stakeholder": "人事部",
            "priority": "High",
            "expected_users": 100
        },
        {
            "project_name": "ProjectDashboard", 
            "requirement": "プロジェクト進捗管理・タスク追跡・レポート生成機能付きダッシュボード",
            "stakeholder": "開発部",
            "priority": "Medium",
            "expected_users": 50
        },
        {
            "project_name": "CustomerFeedback",
            "requirement": "顧客フィードバック収集・分析・レポート機能を持つCRMツール",
            "stakeholder": "営業部",
            "priority": "High",
            "expected_users": 30
        }
    ]
    
    print("🏢 社内パイロットプロジェクト選択")
    print("=" * 50)
    
    for i, project in enumerate(sample_projects, 1):
        print(f"{i}. {project['project_name']}")
        print(f"   要件: {project['requirement']}")
        print(f"   部門: {project['stakeholder']}")
        print(f"   優先度: {project['priority']}")
        print()
    
    try:
        choice = int(input("実行するプロジェクト番号を選択 (1-3): "))
        
        if 1 <= choice <= len(sample_projects):
            project_info = sample_projects[choice - 1]
            
            manager = PilotProjectManager()
            result = manager.run_pilot_project(project_info)
            
            return result
        else:
            print("無効な選択です。")
            return None
            
    except (ValueError, KeyboardInterrupt):
        print("パイロットプロジェクトを終了します。")
        return None


if __name__ == "__main__":
    run_sample_pilot()
