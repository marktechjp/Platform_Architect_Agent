#!/usr/bin/env python3
"""
QA Engineer Agent - Phase 4
生成されたコードの品質を保証するため、自動でテストコードを生成するエージェント
"""
import os
import json
from pathlib import Path

class QAEngineerAgent:
    """テストコードを自動生成するQAエンジニアエージェント"""

    def __init__(self):
        self.report = {}

    def analyze_project(self, project_path):
        """プロジェクトを分析し、テスト戦略を立案する"""
        print(f"🔬 プロジェクト分析開始: {project_path}")
        
        frontend_path = Path(project_path) / "frontend"
        backend_path = Path(project_path) / "backend"
        
        analysis = {
            "project_name": Path(project_path).name,
            "frontend": self._analyze_component(frontend_path, "Frontend"),
            "backend": self._analyze_component(backend_path, "Backend"),
        }
        
        print("✅ プロジェクト分析完了。")
        return analysis

    def _analyze_component(self, component_path, component_name):
        """コンポーネント（フロントエンド/バックエンド）を分析する"""
        if not component_path.exists():
            print(f"⚠️ {component_name} ディレクトリが見つかりません。")
            return None
            
        # 実際にはここで package.json などを解析してフレームワークを特定する
        # このPoCでは、既存の生成物からフレームワークを仮定する
        framework = "React/Next.js" if component_name == "Frontend" else "Node.js/Express"
        
        return {
            "path": str(component_path),
            "framework": framework,
            "files_to_test": [str(p) for p in component_path.glob("**/*.js")] # 仮
        }

    def generate_test_code(self, project_analysis):
        """分析結果に基づいてテストコードを生成する"""
        print(f"✍️ テストコード生成開始: {project_analysis['project_name']}")
        
        generated_files = []
        
        # フロントエンドのテスト生成
        if project_analysis["frontend"]:
            fe_tests = self._generate_frontend_tests(project_analysis["frontend"])
            generated_files.extend(self._save_tests(fe_tests, "frontend"))

        # バックエンドのテスト生成
        if project_analysis["backend"]:
            be_tests = self._generate_backend_tests(project_analysis["backend"])
            generated_files.extend(self._save_tests(be_tests, "backend"))
            
        print(f"✅ テストコード生成完了。 {len(generated_files)} ファイル")
        return generated_files

    def _generate_frontend_tests(self, frontend_analysis):
        """フロントエンド用のテストを生成する"""
        tests = {}
        
        # 1. Playwright E2Eテスト (ログインページの基本操作)
        e2e_test_path = Path(frontend_analysis["path"]) / "tests" / "e2e" / "login.spec.ts"
        tests[str(e2e_test_path)] = self._get_playwright_template()
        
        # 2. Jest コンポーネントテスト (ダミー)
        component_test_path = Path(frontend_analysis["path"]) / "components" / "Button.test.tsx"
        tests[str(component_test_path)] = self._get_jest_component_template()
        
        return tests

    def _generate_backend_tests(self, backend_analysis):
        """バックエンド用のテストを生成する"""
        tests = {}
        
        # 1. Jest APIテスト (認証エンドポイント)
        api_test_path = Path(backend_analysis["path"]) / "tests" / "api" / "auth.test.js"
        tests[str(api_test_path)] = self._get_jest_api_template()
        
        return tests
        
    def _save_tests(self, tests, component_type):
        """生成されたテストをファイルに保存する"""
        saved_files = []
        for file_path, content in tests.items():
            try:
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   - 📄 {component_type} テスト保存: {file_path}")
                saved_files.append(file_path)
            except Exception as e:
                print(f"   - ❌ 保存失敗: {file_path} ({e})")
        return saved_files

    def run_qa_workflow(self, project_path):
        """指定されたプロジェクトに対してQAワークフロー全体を実行する"""
        print("\n" + "="*70)
        print(f"🏭 QA Agent ワークフロー開始: {Path(project_path).name}")
        print("="*70)
        
        # 1. プロジェクト分析
        analysis = self.analyze_project(project_path)
        
        # 2. テストコード生成
        generated_tests = self.generate_test_code(analysis)
        
        print("\n🎉 QAワークフロー完了!")
        print(f"   -  analyzation completed for {analysis['project_name']}")
        print(f"   - {len(generated_tests)} test files generated.")
        print("   - 次のステップ: `npm install` を実行し、`npm test` でテストを実行してください。")
        print("="*70 + "\n")
        
        return {"analysis": analysis, "generated_tests": generated_tests}

    # --- テストコードのテンプレート ---
    
    def _get_playwright_template(self):
        return """
import { test, expect } from '@playwright/test';

test('login page has a title and essential elements', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // ページのタイトルを確認
  await expect(page).toHaveTitle(/Login/);

  // Email入力フィールドが存在することを確認
  await expect(page.locator('input[type="email"]')).toBeVisible();

  // Password入力フィールドが存在することを確認
  await expect(page.locator('input[type="password"]')).toBeVisible();

  // ログインボタンが存在することを確認
  await expect(page.locator('button[type="submit"]')).toBeVisible();
});
"""

    def _get_jest_component_template(self):
        return """
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// ダミーのボタンコンポーネント
const Button = ({ children }) => <button>{children}</button>;

describe('Button Component', () => {
  test('renders children correctly', () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText('Click Me')).toBeInTheDocument();
  });
});
"""

    def _get_jest_api_template(self):
        return """
const request = require('supertest');
const express = require('express');

// ダミーのExpressアプリを作成
const app = express();
app.use(express.json());

app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  if (email === 'test@example.com' && password === 'password') {
    res.status(200).json({ token: 'dummy-token' });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

describe('Auth API', () => {
  it('should return a token for valid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'password',
      });
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty('token');
  });

  it('should return an error for invalid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'wrong@example.com',
        password: 'wrongpassword',
      });
    expect(res.statusCode).toEqual(401);
    expect(res.body).toHaveProperty('error');
  });
});
"""

def demo_qa_agent():
    """QA Engineer Agentのデモ実行"""
    qa_agent = QAEngineerAgent()
    
    # 実行対象のプロジェクトパス (FullStack_Project_2 を対象とする)
    target_project_path = "full_stack_projects/FullStack_Project_2"
    
    if not Path(target_project_path).exists():
        print(f"❌ テスト対象のプロジェクトが見つかりません: {target_project_path}")
        print("   先に `full_agent_orchestrator.py` を実行してプロジェクトを生成してください。")
        return
        
    qa_agent.run_qa_workflow(target_project_path)

if __name__ == "__main__":
    demo_qa_agent()
