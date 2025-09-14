#!/usr/bin/env python3
"""
クリーンアップ&再スタートツール
生成されたファイルを整理してクリーンな状態から開始
"""
import os
import shutil
from datetime import datetime

def cleanup_generated_files():
    """生成されたファイルをクリーンアップ"""
    print("🧹 Platform Architect Agent - クリーンアップ開始")
    print("=" * 60)
    
    # 削除対象ディレクトリ
    cleanup_dirs = [
        'generated_agents',
        'generated_code', 
        'generated_backend',
        'full_stack_projects',
        'integrated_projects'
    ]
    
    removed_count = 0
    backup_created = False
    
    # バックアップの作成（オプション）
    backup_choice = input("🤔 既存ファイルをバックアップしますか？ (y/n): ").lower()
    
    if backup_choice == 'y':
        backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        for dir_name in cleanup_dirs:
            if os.path.exists(dir_name):
                try:
                    shutil.copytree(dir_name, f"{backup_dir}/{dir_name}")
                    print(f"📦 {dir_name} をバックアップしました")
                    backup_created = True
                except Exception as e:
                    print(f"⚠️ {dir_name} のバックアップに失敗: {e}")
        
        if backup_created:
            print(f"✅ バックアップ完了: {backup_dir}/")
    
    # クリーンアップ実行
    print(f"\n🗑️ 生成ファイルの削除開始...")
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            try:
                # ディレクトリ内のファイル数をカウント
                file_count = 0
                for root, dirs, files in os.walk(dir_name):
                    file_count += len(files)
                
                shutil.rmtree(dir_name)
                print(f"🗑️ {dir_name}/ を削除しました ({file_count}ファイル)")
                removed_count += file_count
                
            except Exception as e:
                print(f"❌ {dir_name} の削除に失敗: {e}")
        else:
            print(f"ℹ️ {dir_name}/ は存在しません")
    
    # 検証レポートファイルも削除
    report_files = [f for f in os.listdir('.') if f.startswith('system_verification_report_')]
    for report_file in report_files:
        try:
            os.remove(report_file)
            print(f"🗑️ {report_file} を削除しました")
            removed_count += 1
        except Exception as e:
            print(f"⚠️ {report_file} の削除に失敗: {e}")
    
    print(f"\n✅ クリーンアップ完了!")
    print(f"📊 削除されたファイル総数: {removed_count}")
    
    if backup_created:
        print(f"💾 バックアップ保存先: {backup_dir}/")
    
    return removed_count

def setup_clean_environment():
    """クリーンな環境をセットアップ"""
    print(f"\n🚀 クリーンな環境セットアップ")
    print("-" * 40)
    
    # 必要なディレクトリを作成
    required_dirs = [
        'generated_agents',
        'generated_code',
        'generated_backend', 
        'full_stack_projects',
        'integrated_projects'
    ]
    
    for dir_name in required_dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"📁 {dir_name}/ を作成しました")
    
    # README作成
    with open('generated_agents/README.md', 'w', encoding='utf-8') as f:
        f.write("""# Generated Agents

このディレクトリには、Platform Architect Agentによって生成されたエージェント設計書が保存されます。

## ファイル命名規則
- `{AgentName}_Agent_{timestamp}.md` - エージェント設計書
- `project_overview_{timestamp}.json` - プロジェクト概要

## 生成される内容
- エージェントの責任範囲
- 自律レベル（L1, L2, L3）
- 主要機能・スキル
- KPI指標
""")
    
    print("✅ READMEファイルを作成しました")
    print("🌟 クリーンな環境の準備完了!")

def display_next_steps():
    """次のステップを表示"""
    print(f"\n🎯 次のステップ")
    print("=" * 60)
    print("1. 🚀 Platform Architect Agentを新規起動")
    print("   → python simple_demo.py")
    print()
    print("2. 📝 要件を入力してテスト")
    print("   例: 'ECサイト（商品管理、カート、決済）'")
    print()
    print("3. 📊 生成結果の確認")
    print("   → generated_agents/フォルダを確認")
    print()
    print("4. 🔍 品質検証の実行")
    print("   → python quick_analysis.py")
    print()
    print("🌟 これで分かりやすく、整理された状態でデモを体験できます！")

def main():
    """メイン実行"""
    print("🎯 Platform Architect Agent - クリーンアップ&再スタート")
    print("現在の混乱した状態をクリアして、分かりやすい環境を作成します。")
    print()
    
    # 現在の状況確認
    current_files = 0
    check_dirs = ['generated_agents', 'generated_code', 'generated_backend', 'full_stack_projects', 'integrated_projects']
    
    for dir_name in check_dirs:
        if os.path.exists(dir_name):
            for root, dirs, files in os.walk(dir_name):
                current_files += len(files)
    
    print(f"📊 現在の生成ファイル数: {current_files}")
    
    if current_files > 0:
        proceed = input("🤔 クリーンアップを実行しますか？ (y/n): ").lower()
        
        if proceed == 'y':
            removed = cleanup_generated_files()
            setup_clean_environment()
            display_next_steps()
        else:
            print("ℹ️ クリーンアップをキャンセルしました")
    else:
        print("✅ 既にクリーンな状態です")
        setup_clean_environment()
        display_next_steps()

if __name__ == "__main__":
    main()
