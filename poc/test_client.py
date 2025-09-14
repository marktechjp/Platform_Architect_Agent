#!/usr/bin/env python3
"""
Platform Architect Agentのテスト用クライアント
"""
import requests
import json
import sys

def test_agent_generation(requirement):
    """エージェント生成APIをテストする"""
    url = "http://localhost:8080/"
    
    payload = {
        "business_requirements": requirement
    }
    
    try:
        print(f"要件を送信中: {requirement}")
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功! タイムスタンプ: {result.get('timestamp')}")
            print(f"🤖 生成されたエージェント数: {len(result.get('generated_design', {}).get('required_agents', []))}")
            
            # 生成されたエージェントの概要を表示
            agents = result.get('generated_design', {}).get('required_agents', [])
            for i, agent in enumerate(agents, 1):
                print(f"   {i}. {agent.get('agent_name')} - {agent.get('responsibility')}")
                
            return True
        else:
            print(f"❌ エラー: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ サーバーに接続できません。Flask アプリが起動していることを確認してください。")
        return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False

def main():
    """メイン関数"""
    print("🏗️  Platform Architect Agent テストクライアント")
    print("=" * 50)
    
    # テストケース
    test_cases = [
        "ログイン機能付きのブログサイト",
        "電気工事士向けのキャリア相談ができるマッチングプラットフォーム",
        "オンライン書店のWebアプリケーション"
    ]
    
    if len(sys.argv) > 1:
        # コマンドライン引数が指定された場合
        requirement = " ".join(sys.argv[1:])
        test_agent_generation(requirement)
    else:
        # 対話式でテストケースを選択
        print("テストケースを選択してください:")
        for i, case in enumerate(test_cases, 1):
            print(f"  {i}. {case}")
        print(f"  {len(test_cases) + 1}. カスタム要件を入力")
        
        try:
            choice = int(input("\n選択 (番号): "))
            
            if 1 <= choice <= len(test_cases):
                requirement = test_cases[choice - 1]
            elif choice == len(test_cases) + 1:
                requirement = input("カスタム要件を入力してください: ")
            else:
                print("無効な選択です。")
                return
                
            test_agent_generation(requirement)
            
        except (ValueError, KeyboardInterrupt):
            print("\n終了します。")

if __name__ == "__main__":
    main()
