#!/usr/bin/env python3
"""
簡易版Platform Architect Agentのテスト
"""
import requests
import json
import time

def test_server():
    """サーバーのテスト"""
    base_url = "http://localhost:8080"
    
    print("🏗️  Platform Architect Agent (簡易版) テスト")
    print("=" * 50)
    
    # 1. ヘルスチェック
    print("1. ヘルスチェック...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ サーバーは正常に動作しています")
            print(f"   レスポンス: {response.json()}")
        else:
            print(f"❌ ヘルスチェック失敗: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ サーバーに接続できません")
        print("   simple_main.py が起動していることを確認してください")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False
    
    # 2. エージェント生成テスト
    test_cases = [
        "ログイン機能付きのブログサイト",
        "電気工事士向けのキャリア相談ができるマッチングプラットフォーム", 
        "オンライン書店のWebアプリケーション"
    ]
    
    for i, requirement in enumerate(test_cases, 1):
        print(f"\n{i + 1}. エージェント生成テスト: {requirement}")
        
        payload = {"requirement": requirement}
        
        try:
            response = requests.post(f"{base_url}/", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 成功! タイムスタンプ: {result.get('timestamp')}")
                
                agents = result.get('generated_design', {}).get('required_agents', [])
                print(f"🤖 生成されたエージェント数: {len(agents)}")
                
                for j, agent in enumerate(agents, 1):
                    print(f"   {j}. {agent.get('agent_name')} - {agent.get('responsibility')}")
                
                # プロジェクト概要表示
                overview = result.get('generated_design', {}).get('project_overview', {})
                print(f"📋 プロジェクト名: {overview.get('name')}")
                print(f"⏱️  見積もり期間: {overview.get('estimated_timeline')}")
                
            else:
                print(f"❌ エラー: {response.status_code}")
                print(f"   レスポンス: {response.text}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    print("\n" + "=" * 50)
    print("✅ テスト完了! generated_agents/ フォルダで生成されたファイルを確認してください。")
    return True

if __name__ == "__main__":
    test_server()
