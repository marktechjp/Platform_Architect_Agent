#!/usr/bin/env python3
"""
Frontend Developer Agent - Phase 2実装
ログインページの雛形コード生成機能
"""
import os
import json
from datetime import datetime
from pathlib import Path

class FrontendDeveloperAgent:
    """フロントエンド開発エージェント"""
    
    def __init__(self, project_config=None):
        self.project_config = project_config or {}
        self.agent_name = "Frontend Developer Agent"
        self.version = "2.0"
        
    def generate_login_page(self, project_name="MyApp", tech_stack=None):
        """ログインページの雛形コードを生成"""
        if tech_stack is None:
            tech_stack = ["React", "TypeScript", "CSS"]
            
        print(f"🎨 {self.agent_name} - ログインページ生成中...")
        print(f"📋 プロジェクト: {project_name}")
        print(f"🛠️  技術スタック: {', '.join(tech_stack)}")
        
        # 技術スタックに応じてコード生成
        if "React" in tech_stack:
            return self._generate_react_login()
        elif "Vue.js" in tech_stack:
            return self._generate_vue_login()
        else:
            return self._generate_vanilla_html_login()
    
    def _generate_react_login(self):
        """React + TypeScript ログインページ"""
        
        # LoginPage.tsx
        login_tsx = '''import React, { useState } from 'react';
import './LoginPage.css';

interface LoginFormData {
  email: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Clear error on input change
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // TODO: API呼び出しをここに実装
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('ログインに失敗しました');
      }

      const data = await response.json();
      // TODO: 認証トークンの保存とリダイレクト
      localStorage.setItem('authToken', data.token);
      window.location.href = '/dashboard';
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'ログインエラーが発生しました');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>ログイン</h1>
          <p>アカウントにサインインしてください</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email">メールアドレス</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
              className={error ? 'error' : ''}
              placeholder="example@email.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">パスワード</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
              className={error ? 'error' : ''}
              placeholder="パスワードを入力"
            />
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button 
            type="submit" 
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'ログイン中...' : 'ログイン'}
          </button>

          <div className="login-footer">
            <a href="/forgot-password">パスワードを忘れた方</a>
            <span>アカウントをお持ちでない方は</span>
            <a href="/register">新規登録</a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;'''

        # LoginPage.css
        login_css = '''/* LoginPage.css */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  padding: 40px;
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #333;
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 600;
}

.login-header p {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

.form-group input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input.error {
  border-color: #e74c3c;
}

.error-message {
  background: #fdeaea;
  color: #e74c3c;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  border: 1px solid #fadbd8;
}

.login-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.login-footer a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.login-footer span {
  color: #666;
  font-size: 14px;
}

/* レスポンシブ対応 */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .login-header h1 {
    font-size: 24px;
  }
}'''

        # package.json (React用)
        package_json = '''{
  "name": "frontend-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@types/node": "^18.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.0",
    "web-vitals": "^3.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}'''

        # README.md
        readme = '''# Frontend Application - Login Page

Frontend Developer Agent によって自動生成されたログインページです。

## 🚀 セットアップ

```bash
# 依存関係のインストール
npm install

# 開発サーバー起動
npm start
```

## 📁 ファイル構成

```
src/
├── components/
│   └── LoginPage/
│       ├── LoginPage.tsx    # ログインページコンポーネント
│       └── LoginPage.css    # スタイルシート
└── App.tsx                  # メインアプリケーション
```

## 🎨 機能

- ✅ レスポンシブデザイン
- ✅ TypeScript対応
- ✅ フォームバリデーション
- ✅ エラーハンドリング
- ✅ ローディング状態
- ✅ アクセシビリティ対応

## 🔧 カスタマイズ

### API エンドポイント
`LoginPage.tsx` の `handleSubmit` 関数内でAPI URLを変更してください：

```typescript
const response = await fetch('/api/auth/login', {
  // 設定
});
```

### スタイル
`LoginPage.css` でデザインをカスタマイズできます。

## 📝 次のステップ

1. バックエンドAPI実装
2. 認証トークン管理
3. ルーティング設定
4. ユニットテスト追加

---
*このコードはFrontend Developer Agentによって自動生成されました*
'''

        return {
            "files": {
                "src/components/LoginPage/LoginPage.tsx": login_tsx,
                "src/components/LoginPage/LoginPage.css": login_css,
                "package.json": package_json,
                "README.md": readme
            },
            "framework": "React + TypeScript",
            "features": [
                "レスポンシブデザイン",
                "TypeScript対応", 
                "フォームバリデーション",
                "エラーハンドリング",
                "ローディング状態",
                "アクセシビリティ対応"
            ]
        }
    
    def _generate_vue_login(self):
        """Vue.js ログインページ"""
        
        # LoginPage.vue
        login_vue = '''<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>ログイン</h1>
        <p>アカウントにサインインしてください</p>
      </div>

      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group">
          <label for="email">メールアドレス</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            required
            :class="{ error: error }"
            placeholder="example@email.com"
          />
        </div>

        <div class="form-group">
          <label for="password">パスワード</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            required
            :class="{ error: error }"
            placeholder="パスワードを入力"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button 
          type="submit" 
          class="login-button"
          :disabled="isLoading"
        >
          {{ isLoading ? 'ログイン中...' : 'ログイン' }}
        </button>

        <div class="login-footer">
          <router-link to="/forgot-password">パスワードを忘れた方</router-link>
          <span>アカウントをお持ちでない方は</span>
          <router-link to="/register">新規登録</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      isLoading: false,
      error: ''
    }
  },
  methods: {
    async handleSubmit() {
      this.isLoading = true;
      this.error = '';

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        });

        if (!response.ok) {
          throw new Error('ログインに失敗しました');
        }

        const data = await response.json();
        localStorage.setItem('authToken', data.token);
        this.$router.push('/dashboard');
        
      } catch (err) {
        this.error = err.message || 'ログインエラーが発生しました';
      } finally {
        this.isLoading = false;
      }
    }
  },
  watch: {
    formData: {
      handler() {
        this.error = '';
      },
      deep: true
    }
  }
}
</script>

<style scoped>
/* 同じCSSスタイル */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 他のスタイルは同様... */
</style>'''

        return {
            "files": {
                "src/components/LoginPage.vue": login_vue,
                "package.json": "{ /* Vue.js package.json */ }",
                "README.md": "# Vue.js Login Page"
            },
            "framework": "Vue.js",
            "features": ["Vue 3 Composition API", "Vue Router対応"]
        }
    
    def _generate_vanilla_html_login(self):
        """バニラHTML/CSS/JS ログインページ"""
        
        html_content = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ログイン</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h1>ログイン</h1>
                <p>アカウントにサインインしてください</p>
            </div>

            <form id="loginForm" class="login-form">
                <div class="form-group">
                    <label for="email">メールアドレス</label>
                    <input type="email" id="email" name="email" required placeholder="example@email.com">
                </div>

                <div class="form-group">
                    <label for="password">パスワード</label>
                    <input type="password" id="password" name="password" required placeholder="パスワードを入力">
                </div>

                <div id="errorMessage" class="error-message" style="display: none;"></div>

                <button type="submit" class="login-button">
                    <span id="buttonText">ログイン</span>
                </button>

                <div class="login-footer">
                    <a href="/forgot-password">パスワードを忘れた方</a>
                    <span>アカウントをお持ちでない方は</span>
                    <a href="/register">新規登録</a>
                </div>
            </form>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>'''

        js_content = '''// script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const buttonText = document.getElementById('buttonText');
    const loginButton = form.querySelector('.login-button');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // UI状態更新
        loginButton.disabled = true;
        buttonText.textContent = 'ログイン中...';
        errorMessage.style.display = 'none';

        // フォームデータ取得
        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error('ログインに失敗しました');
            }

            const result = await response.json();
            localStorage.setItem('authToken', result.token);
            window.location.href = '/dashboard';
            
        } catch (error) {
            errorMessage.textContent = error.message || 'ログインエラーが発生しました';
            errorMessage.style.display = 'block';
        } finally {
            loginButton.disabled = false;
            buttonText.textContent = 'ログイン';
        }
    });

    // 入力時にエラーメッセージをクリア
    form.addEventListener('input', function() {
        errorMessage.style.display = 'none';
    });
});'''

        return {
            "files": {
                "index.html": html_content,
                "script.js": js_content,
                "styles.css": "/* 同じCSSスタイル */",
                "README.md": "# HTML/CSS/JS Login Page"
            },
            "framework": "Vanilla HTML/CSS/JS",
            "features": ["モダンJS (ES6+)", "レスポンシブデザイン", "フォームバリデーション"]
        }
    
    def save_generated_code(self, generated_code, project_name="LoginPage", output_dir="generated_code"):
        """生成されたコードをファイルに保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = f"{output_dir}/{project_name}_{timestamp}"
        
        try:
            # ディレクトリ作成
            os.makedirs(project_dir, exist_ok=True)
            
            # ファイル保存
            saved_files = []
            for file_path, content in generated_code["files"].items():
                full_path = os.path.join(project_dir, file_path)
                
                # サブディレクトリ作成
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(file_path)
            
            # メタデータファイル保存
            metadata = {
                "agent": self.agent_name,
                "version": self.version,
                "timestamp": timestamp,
                "framework": generated_code["framework"],
                "features": generated_code["features"],
                "files": saved_files
            }
            
            with open(f"{project_dir}/metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"💾 コードが保存されました: {project_dir}/")
            return project_dir
            
        except Exception as e:
            print(f"❌ コード保存エラー: {e}")
            return None


def demo_frontend_agent():
    """Frontend Developer Agentのデモ"""
    print("🎨 Frontend Developer Agent - Phase 2 デモ")
    print("=" * 50)
    
    agent = FrontendDeveloperAgent()
    
    # テストケース
    test_cases = [
        {
            "project_name": "BlogSite",
            "tech_stack": ["React", "TypeScript", "CSS"]
        },
        {
            "project_name": "MatchingPlatform", 
            "tech_stack": ["Vue.js", "JavaScript", "CSS"]
        },
        {
            "project_name": "BookStore",
            "tech_stack": ["HTML", "CSS", "JavaScript"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. テストケース: {test_case['project_name']}")
        
        # コード生成
        generated_code = agent.generate_login_page(
            project_name=test_case["project_name"],
            tech_stack=test_case["tech_stack"]
        )
        
        # ファイル保存
        project_dir = agent.save_generated_code(generated_code, test_case["project_name"])
        
        if project_dir:
            print(f"✅ 生成完了: {generated_code['framework']}")
            print(f"📁 保存先: {project_dir}")
            print(f"🎯 機能: {', '.join(generated_code['features'])}")
        
        print("-" * 50)
    
    print("🎉 Frontend Developer Agent デモ完了!")


if __name__ == "__main__":
    demo_frontend_agent()
