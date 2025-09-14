#!/usr/bin/env python3
"""
クイック分析ツール - デモ結果の即座分析
"""
import os
import json
from datetime import datetime

def quick_demo_analysis():
    """デモ結果のクイック分析"""
    print("🔍 Platform Architect Agent - デモ結果クイック分析")
    print("=" * 60)
    
    # 生成されたファイルの確認
    results = {
        "agents": [],
        "projects": [],
        "backend": [],
        "frontend": []
    }
    
    # エージェント確認
    if os.path.exists('generated_agents'):
        agent_files = [f for f in os.listdir('generated_agents') if f.endswith('.md')]
        results["agents"] = agent_files
        print(f"🤖 生成エージェント: {len(agent_files)}個")
        for agent in agent_files:
            print(f"   📄 {agent}")
    
    # フルスタックプロジェクト確認
    if os.path.exists('full_stack_projects'):
        projects = [d for d in os.listdir('full_stack_projects') if os.path.isdir(f'full_stack_projects/{d}')]
        results["projects"] = projects
        print(f"\n🏗️ フルスタックプロジェクト: {len(projects)}個")
        for project in projects:
            print(f"   📁 {project}")
    
    # バックエンド確認
    if os.path.exists('generated_backend'):
        backend_projects = [d for d in os.listdir('generated_backend') if os.path.isdir(f'generated_backend/{d}')]
        results["backend"] = backend_projects
        print(f"\n⚙️ バックエンドプロジェクト: {len(backend_projects)}個")
    
    # フロントエンド確認
    if os.path.exists('generated_code'):
        frontend_projects = [d for d in os.listdir('generated_code') if os.path.isdir(f'generated_code/{d}')]
        results["frontend"] = frontend_projects
        print(f"\n🎨 フロントエンドプロジェクト: {len(frontend_projects)}個")
    
    # 効果試算
    total_artifacts = len(results["agents"]) + len(results["projects"]) + len(results["backend"]) + len(results["frontend"])
    
    print(f"\n📊 生成アーティファクト総数: {total_artifacts}")
    
    if total_artifacts >= 5:
        time_saved = "8-12週間"
        cost_saved = "¥1,000,000-2,000,000"
        rating = "🌟 Excellent"
    elif total_artifacts >= 3:
        time_saved = "4-6週間"
        cost_saved = "¥500,000-1,000,000"
        rating = "✅ Good"
    else:
        time_saved = "2-3週間"
        cost_saved = "¥200,000-500,000"
        rating = "📋 Basic"
    
    print(f"\n💰 推定効果:")
    print(f"   ⏱️ 時間短縮: {time_saved}")
    print(f"   💸 コスト削減: {cost_saved}")
    print(f"   🏆 評価: {rating}")
    
    # 次のアクション提案
    print(f"\n🚀 推奨次ステップ:")
    if total_artifacts >= 5:
        print(f"   ✅ 即座にチーム導入検討")
        print(f"   ✅ 経営陣への成果報告")
        print(f"   ✅ より大規模プロジェクトでの実証")
    elif total_artifacts >= 3:
        print(f"   🔄 追加要件での再実行")
        print(f"   👥 チームメンバーとの共有")
        print(f"   📋 詳細機能の確認")
    else:
        print(f"   🔍 より具体的要件での再挑戦")
        print(f"   📚 使用方法の確認")
        print(f"   🤝 サポートへの相談")
    
    return results

if __name__ == "__main__":
    quick_demo_analysis()
