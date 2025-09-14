#!/usr/bin/env python3
"""
Backend Developer Agent - Phase 3実装
API設計とデータベーススキーマの自動生成
"""
import os
import json
from datetime import datetime
from pathlib import Path

class BackendDeveloperAgent:
    """バックエンド開発エージェント"""
    
    def __init__(self, project_config=None):
        self.project_config = project_config or {}
        self.agent_name = "Backend Developer Agent"
        self.version = "3.0"
        
    def generate_backend_api(self, project_name="MyApp", tech_stack=None, requirements=None):
        """バックエンドAPI・データベース設計を生成"""
        if tech_stack is None:
            tech_stack = ["Node.js", "Express", "MongoDB"]
        if requirements is None:
            requirements = ["ログイン機能"]
            
        print(f"⚙️  {self.agent_name} - バックエンド設計生成中...")
        print(f"📋 プロジェクト: {project_name}")
        print(f"🛠️  技術スタック: {', '.join(tech_stack)}")
        print(f"📝 要件: {', '.join(requirements)}")
        
        # 技術スタックに応じてコード生成
        if "Node.js" in tech_stack or "Express" in tech_stack:
            return self._generate_nodejs_api(project_name, requirements)
        elif "Python" in tech_stack or "Django" in tech_stack:
            return self._generate_django_api(project_name, requirements)
        elif "FastAPI" in tech_stack:
            return self._generate_fastapi_api(project_name, requirements)
        else:
            return self._generate_nodejs_api(project_name, requirements)  # デフォルト
    
    def _generate_nodejs_api(self, project_name, requirements):
        """Node.js + Express API生成"""
        
        # server.js - メインサーバーファイル
        server_js = '''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const authRoutes = require('./routes/auth');
const userRoutes = require('./routes/users');
const { errorHandler } = require('./middleware/errorHandler');
const { logger } = require('./utils/logger');

const app = express();

// セキュリティミドルウェア
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// レート制限
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// ボディパーサー
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// ログ出力
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.path} - ${req.ip}`);
  next();
});

// MongoDB接続
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/myapp', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => logger.info('MongoDB connected successfully'))
.catch(err => logger.error('MongoDB connection error:', err));

// ルート設定
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);

// ヘルスチェック
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// 404ハンドラー
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// エラーハンドラー
app.use(errorHandler);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

module.exports = app;'''

        # models/User.js - ユーザーモデル
        user_model = '''const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*(\\.\\w{2,3})+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters long'],
    select: false // デフォルトでパスワードは除外
  },
  firstName: {
    type: String,
    required: [true, 'First name is required'],
    trim: true,
    maxlength: [50, 'First name cannot exceed 50 characters']
  },
  lastName: {
    type: String,
    required: [true, 'Last name is required'],
    trim: true,
    maxlength: [50, 'Last name cannot exceed 50 characters']
  },
  role: {
    type: String,
    enum: ['user', 'admin', 'moderator'],
    default: 'user'
  },
  isActive: {
    type: Boolean,
    default: true
  },
  lastLogin: {
    type: Date
  },
  profile: {
    avatar: String,
    bio: {
      type: String,
      maxlength: [500, 'Bio cannot exceed 500 characters']
    },
    phone: {
      type: String,
      match: [/^[\\+]?[1-9][\\d]{0,15}$/, 'Please enter a valid phone number']
    },
    dateOfBirth: Date
  },
  preferences: {
    notifications: {
      email: { type: Boolean, default: true },
      push: { type: Boolean, default: true }
    },
    theme: {
      type: String,
      enum: ['light', 'dark', 'auto'],
      default: 'auto'
    }
  }
}, {
  timestamps: true,
  toJSON: { 
    transform: function(doc, ret) {
      delete ret.password;
      return ret;
    }
  }
});

// パスワードハッシュ化ミドルウェア
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// パスワード比較メソッド
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// フルネーム仮想フィールド
userSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`;
});

// インデックス作成
userSchema.index({ email: 1 });
userSchema.index({ createdAt: -1 });

module.exports = mongoose.model('User', userSchema);'''

        # routes/auth.js - 認証ルート
        auth_routes = '''const express = require('express');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const User = require('../models/User');
const { validateLogin, validateRegister } = require('../middleware/validation');
const { authenticateToken } = require('../middleware/auth');
const { logger } = require('../utils/logger');

const router = express.Router();

// ログイン用レート制限（より厳しく）
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // limit each IP to 5 login requests per windowMs
  message: { error: 'Too many login attempts, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

// JWT生成ユーティリティ
const generateTokens = (userId) => {
  const accessToken = jwt.sign(
    { userId, type: 'access' },
    process.env.JWT_SECRET || 'your-secret-key',
    { expiresIn: process.env.JWT_EXPIRES_IN || '15m' }
  );
  
  const refreshToken = jwt.sign(
    { userId, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET || 'your-refresh-secret',
    { expiresIn: '7d' }
  );
  
  return { accessToken, refreshToken };
};

// POST /api/auth/register - ユーザー登録
router.post('/register', validateRegister, async (req, res) => {
  try {
    const { email, password, firstName, lastName } = req.body;
    
    // 既存ユーザーチェック
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({ error: 'Email already registered' });
    }
    
    // 新規ユーザー作成
    const user = new User({
      email,
      password,
      firstName,
      lastName
    });
    
    await user.save();
    
    // トークン生成
    const { accessToken, refreshToken } = generateTokens(user._id);
    
    logger.info(`New user registered: ${email}`);
    
    res.status(201).json({
      message: 'User registered successfully',
      user: {
        id: user._id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role
      },
      tokens: {
        accessToken,
        refreshToken
      }
    });
    
  } catch (error) {
    logger.error('Registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /api/auth/login - ログイン
router.post('/login', loginLimiter, validateLogin, async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // ユーザー検索（パスワード含む）
    const user = await User.findOne({ email }).select('+password');
    if (!user || !user.isActive) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // パスワード検証
    const isPasswordValid = await user.comparePassword(password);
    if (!isPasswordValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // 最終ログイン時刻更新
    user.lastLogin = new Date();
    await user.save();
    
    // トークン生成
    const { accessToken, refreshToken } = generateTokens(user._id);
    
    logger.info(`User logged in: ${email}`);
    
    res.json({
      message: 'Login successful',
      user: {
        id: user._id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
        lastLogin: user.lastLogin
      },
      tokens: {
        accessToken,
        refreshToken
      }
    });
    
  } catch (error) {
    logger.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// POST /api/auth/refresh - トークンリフレッシュ
router.post('/refresh', async (req, res) => {
  try {
    const { refreshToken } = req.body;
    
    if (!refreshToken) {
      return res.status(401).json({ error: 'Refresh token required' });
    }
    
    // リフレッシュトークン検証
    const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET || 'your-refresh-secret');
    
    if (decoded.type !== 'refresh') {
      return res.status(401).json({ error: 'Invalid token type' });
    }
    
    // ユーザー存在確認
    const user = await User.findById(decoded.userId);
    if (!user || !user.isActive) {
      return res.status(401).json({ error: 'User not found or inactive' });
    }
    
    // 新しいアクセストークン生成
    const { accessToken } = generateTokens(user._id);
    
    res.json({
      accessToken
    });
    
  } catch (error) {
    logger.error('Token refresh error:', error);
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// POST /api/auth/logout - ログアウト
router.post('/logout', authenticateToken, (req, res) => {
  // 実際のアプリケーションでは、トークンブラックリストやRedisを使用
  logger.info(`User logged out: ${req.user.userId}`);
  res.json({ message: 'Logout successful' });
});

// GET /api/auth/me - 現在のユーザー情報
router.get('/me', authenticateToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({ user });
    
  } catch (error) {
    logger.error('Get user error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;'''

        # middleware/auth.js - 認証ミドルウェア
        auth_middleware = '''const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { logger } = require('../utils/logger');

// JWT認証ミドルウェア
const authenticateToken = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
    
    if (!token) {
      return res.status(401).json({ error: 'Access token required' });
    }
    
    // トークン検証
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key');
    
    if (decoded.type !== 'access') {
      return res.status(401).json({ error: 'Invalid token type' });
    }
    
    // ユーザー存在確認
    const user = await User.findById(decoded.userId);
    if (!user || !user.isActive) {
      return res.status(401).json({ error: 'User not found or inactive' });
    }
    
    req.user = { userId: user._id, role: user.role };
    next();
    
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    } else if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ error: 'Invalid token' });
    }
    
    logger.error('Authentication error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

// 役割ベース認証
const requireRole = (roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Authentication required' });
    }
    
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    
    next();
  };
};

// 管理者のみ
const requireAdmin = requireRole(['admin']);

// 管理者またはモデレーター
const requireModerator = requireRole(['admin', 'moderator']);

module.exports = {
  authenticateToken,
  requireRole,
  requireAdmin,
  requireModerator
};'''

        # package.json
        package_json = '''{
  "name": "backend-api",
  "version": "1.0.0",
  "description": "Auto-generated backend API with authentication",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix"
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.5.0",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "express-rate-limit": "^6.8.1",
    "express-validator": "^7.0.1",
    "dotenv": "^16.3.1",
    "winston": "^3.10.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.6.2",
    "supertest": "^6.3.3",
    "eslint": "^8.47.0"
  },
  "engines": {
    "node": ">=16.0.0"
  },
  "keywords": [
    "api",
    "authentication",
    "express",
    "mongodb",
    "jwt"
  ],
  "author": "Backend Developer Agent",
  "license": "MIT"
}'''

        # .env.example
        env_example = '''# Server Configuration
PORT=5000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/myapp

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_REFRESH_SECRET=your-super-secret-refresh-key-change-this-in-production
JWT_EXPIRES_IN=15m

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=info'''

        # README.md
        readme = '''# Backend API

Backend Developer Agent によって自動生成されたNode.js + Express APIサーバーです。

## 🚀 セットアップ

### 前提条件
- Node.js (v16以上)
- MongoDB
- npm または yarn

### インストール

```bash
# 依存関係インストール
npm install

# 環境変数設定
cp .env.example .env
# .envファイルを編集してください

# 開発サーバー起動
npm run dev
```

## 📋 API仕様

### 認証エンドポイント

#### POST /api/auth/register
ユーザー新規登録

```json
{
  "email": "user@example.com",
  "password": "password123",
  "firstName": "太郎",
  "lastName": "山田"
}
```

#### POST /api/auth/login
ログイン

```json
{
  "email": "user@example.com", 
  "password": "password123"
}
```

#### POST /api/auth/refresh
トークンリフレッシュ

```json
{
  "refreshToken": "refresh_token_here"
}
```

#### GET /api/auth/me
現在のユーザー情報取得（要認証）

### レスポンス例

```json
{
  "message": "Login successful",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "firstName": "太郎",
    "lastName": "山田",
    "role": "user"
  },
  "tokens": {
    "accessToken": "jwt_access_token",
    "refreshToken": "jwt_refresh_token"
  }
}
```

## 🗄️ データベース設計

### User Collection

```javascript
{
  _id: ObjectId,
  email: String (unique),
  password: String (hashed),
  firstName: String,
  lastName: String,
  role: String (enum: 'user', 'admin', 'moderator'),
  isActive: Boolean,
  lastLogin: Date,
  profile: {
    avatar: String,
    bio: String,
    phone: String,
    dateOfBirth: Date
  },
  preferences: {
    notifications: {
      email: Boolean,
      push: Boolean
    },
    theme: String (enum: 'light', 'dark', 'auto')
  },
  createdAt: Date,
  updatedAt: Date
}
```

## 🔒 セキュリティ機能

- ✅ JWT認証（アクセストークン + リフレッシュトークン）
- ✅ パスワードハッシュ化（bcrypt）
- ✅ レート制限
- ✅ CORS設定
- ✅ Helmet（セキュリティヘッダー）
- ✅ 入力バリデーション
- ✅ エラーハンドリング

## 🧪 テスト

```bash
# テスト実行
npm test

# テスト監視モード
npm run test:watch
```

## 📝 開発

```bash
# 開発サーバー（ホットリロード）
npm run dev

# コード整形
npm run lint:fix
```

## 🚀 デプロイ

### 環境変数

本番環境では以下の環境変数を設定してください：

- `NODE_ENV=production`
- `JWT_SECRET` - 強力なシークレットキー
- `JWT_REFRESH_SECRET` - リフレッシュトークン用
- `MONGODB_URI` - MongoDBの接続URL

### Docker

```bash
# Docker イメージビルド
docker build -t backend-api .

# Docker コンテナ実行
docker run -p 5000:5000 --env-file .env backend-api
```

---
*このAPIはBackend Developer Agentによって自動生成されました*
'''

        return {
            "files": {
                "server.js": server_js,
                "models/User.js": user_model,
                "routes/auth.js": auth_routes,
                "middleware/auth.js": auth_middleware,
                "package.json": package_json,
                ".env.example": env_example,
                "README.md": readme
            },
            "framework": "Node.js + Express + MongoDB",
            "features": [
                "JWT認証システム",
                "ユーザー登録・ログイン",
                "ロールベース認証",
                "セキュリティミドルウェア",
                "レート制限",
                "バリデーション",
                "エラーハンドリング",
                "ログ出力"
            ],
            "database_schema": {
                "User": {
                    "fields": ["email", "password", "firstName", "lastName", "role", "profile", "preferences"],
                    "indexes": ["email", "createdAt"],
                    "relations": []
                }
            },
            "endpoints": [
                "POST /api/auth/register",
                "POST /api/auth/login", 
                "POST /api/auth/refresh",
                "POST /api/auth/logout",
                "GET /api/auth/me"
            ]
        }
    
    def _generate_django_api(self, project_name, requirements):
        """Django REST API生成"""
        
        # settings.py
        settings_py = '''import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'accounts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'myapp'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Internationalization
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

        # models.py
        models_py = '''from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]
    
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    
    # Profile fields
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\\+?1?\\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='auto')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()'''

        return {
            "files": {
                "config/settings.py": settings_py,
                "accounts/models.py": models_py,
                "requirements.txt": "Django>=4.2.0\ndjango-cors-headers\ndjangorestframework\ndjangorestframework-simplejwt\npsycopg2-binary",
                "README.md": "# Django REST API\n\nDjango + PostgreSQL API"
            },
            "framework": "Django + PostgreSQL",
            "features": ["Django REST Framework", "JWT認証", "PostgreSQL"]
        }
    
    def _generate_fastapi_api(self, project_name, requirements):
        """FastAPI生成"""
        main_py = '''from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import get_db
from models import User
from auth import authenticate_user, create_access_token, get_current_user
from schemas import UserCreate, UserLogin, Token

app = FastAPI(title="Auto-generated API", version="1.0.0")

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # User registration logic
    pass

@app.post("/auth/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Login logic
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)'''
        
        return {
            "files": {
                "main.py": main_py,
                "requirements.txt": "fastapi\nuvicorn\nsqlalchemy\npsycopg2-binary",
                "README.md": "# FastAPI\n\nFastAPI + PostgreSQL API"
            },
            "framework": "FastAPI + PostgreSQL",
            "features": ["FastAPI", "自動ドキュメント", "高速API"]
        }
    
    def save_generated_backend(self, generated_code, project_name="BackendAPI", output_dir="generated_backend"):
        """生成されたバックエンドコードをファイルに保存"""
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
                "database_schema": generated_code.get("database_schema", {}),
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
    """Backend Developer Agentのデモ"""
    print("⚙️  Backend Developer Agent - Phase 3 デモ")
    print("=" * 50)
    
    agent = BackendDeveloperAgent()
    
    # テストケース
    test_cases = [
        {
            "project_name": "BlogAPI",
            "tech_stack": ["Node.js", "Express", "MongoDB"],
            "requirements": ["ログイン機能", "ユーザー登録", "認証"]
        },
        {
            "project_name": "MatchingAPI",
            "tech_stack": ["Python", "Django", "PostgreSQL"],
            "requirements": ["ユーザーマッチング", "プロファイル管理"]
        },
        {
            "project_name": "BookStoreAPI",
            "tech_stack": ["FastAPI", "PostgreSQL"],
            "requirements": ["商品管理", "注文処理", "決済"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. テストケース: {test_case['project_name']}")
        
        # API生成
        generated_code = agent.generate_backend_api(
            project_name=test_case["project_name"],
            tech_stack=test_case["tech_stack"],
            requirements=test_case["requirements"]
        )
        
        # ファイル保存
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
