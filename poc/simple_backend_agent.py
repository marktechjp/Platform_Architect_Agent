#!/usr/bin/env python3
"""
Backend Developer Agent - 簡易版（Phase 3）
"""
import os
import json
from datetime import datetime

class BackendDeveloperAgent:
    def __init__(self):
        self.agent_name = "Backend Developer Agent"
        self.version = "3.0"
        
    def generate_backend_api(self, project_name="MyApp", tech_stack=None, requirements=None):
        print(f"⚙️  {self.agent_name} - バックエンド設計生成中...")
        print(f"📋 プロジェクト: {project_name}")
        print(f"🛠️  技術スタック: {', '.join(tech_stack or ['Node.js', 'Express'])}")
        
        # Node.js + Express API生成
        return self._generate_nodejs_api(project_name)
    
    def _generate_nodejs_api(self, project_name):
        server_js = """const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();

app.use(cors());
app.use(express.json());

// ユーザーデータ（実際はデータベースを使用）
const users = [];

// ユーザー登録
app.post('/api/auth/register', async (req, res) => {
  try {
    const { email, password, firstName, lastName } = req.body;
    
    // 既存ユーザーチェック
    if (users.find(u => u.email === email)) {
      return res.status(409).json({ error: 'Email already exists' });
    }
    
    // パスワードハッシュ化
    const hashedPassword = await bcrypt.hash(password, 10);
    
    const user = {
      id: Date.now().toString(),
      email,
      password: hashedPassword,
      firstName,
      lastName,
      createdAt: new Date()
    };
    
    users.push(user);
    
    // JWTトークン生成
    const token = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: '24h' }
    );
    
    res.status(201).json({
      message: 'User registered successfully',
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName
      },
      token
    });
    
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ログイン
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    const user = users.find(u => u.email === email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const token = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: '24h' }
    );
    
    res.json({
      message: 'Login successful',
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName
      },
      token
    });
    
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 認証ミドルウェア
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET || 'secret', (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// ユーザー情報取得
app.get('/api/auth/me', authenticateToken, (req, res) => {
  const user = users.find(u => u.id === req.user.userId);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json({
    user: {
      id: user.id,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName
    }
  });
});

// ヘルスチェック
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date() });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;"""

        package_json = """{
  "name": "backend-api",
  "version": "1.0.0",
  "description": "Auto-generated backend API",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}"""

        readme = """# Backend API

Backend Developer Agent によって自動生成されたAPIサーバーです。

## セットアップ

```bash
npm install
npm start
```

## API エンドポイント

- POST /api/auth/register - ユーザー登録
- POST /api/auth/login - ログイン
- GET /api/auth/me - ユーザー情報取得
- GET /health - ヘルスチェック

## 使用例

### ユーザー登録
```bash
curl -X POST http://localhost:5000/api/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "firstName": "太郎",
    "lastName": "山田"
  }'
```

### ログイン
```bash
curl -X POST http://localhost:5000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```
"""

        return {
            "files": {
                "server.js": server_js,
                "package.json": package_json,
                "README.md": readme,
                ".env.example": "JWT_SECRET=your-secret-key\\nPORT=5000"
            },
            "framework": "Node.js + Express",
            "features": [
                "JWT認証",
                "ユーザー登録・ログイン",
                "CORS対応",
                "エラーハンドリング"
            ],
            "endpoints": [
                "POST /api/auth/register",
                "POST /api/auth/login",
                "GET /api/auth/me",
                "GET /health"
            ]
        }
    
    def save_generated_backend(self, generated_code, project_name="BackendAPI", output_dir="generated_backend"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = f"{output_dir}/{project_name}_{timestamp}"
        
        try:
            os.makedirs(project_dir, exist_ok=True)
            
            saved_files = []
            for file_path, content in generated_code["files"].items():
                full_path = os.path.join(project_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(file_path)
            
            metadata = {
                "agent": self.agent_name,
                "version": self.version,
                "timestamp": timestamp,
                "framework": generated_code["framework"],
                "features": generated_code["features"],
                "endpoints": generated_code.get("endpoints", []),
                "files": saved_files
            }
            
            with open(f"{project_dir}/metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"💾 バックエンドコードが保存されました: {project_dir}/")
            return project_dir
            
        except Exception as e:
            print(f"❌ コード保存エラー: {e}")
            return None

def demo_backend_agent():
    print("⚙️  Backend Developer Agent - 簡易版デモ")
    print("=" * 50)
    
    agent = BackendDeveloperAgent()
    
    test_cases = [
        {
            "project_name": "BlogAPI",
            "tech_stack": ["Node.js", "Express"],
            "requirements": ["ログイン機能", "ユーザー登録"]
        },
        {
            "project_name": "MatchingAPI", 
            "tech_stack": ["Node.js", "Express"],
            "requirements": ["ユーザー認証", "プロファイル管理"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\\n{i}. テストケース: {test_case['project_name']}")
        
        generated_code = agent.generate_backend_api(
            project_name=test_case["project_name"],
            tech_stack=test_case["tech_stack"],
            requirements=test_case["requirements"]
        )
        
        project_dir = agent.save_generated_backend(generated_code, test_case["project_name"])
        
        if project_dir:
            print(f"✅ 生成完了: {generated_code['framework']}")
            print(f"📁 保存先: {project_dir}")
            print(f"🛠️  機能: {', '.join(generated_code['features'])}")
            print(f"🔗 エンドポイント数: {len(generated_code.get('endpoints', []))}")
        
        print("-" * 50)
    
    print("🎉 Backend Developer Agent デモ完了!")

if __name__ == "__main__":
    demo_backend_agent()
