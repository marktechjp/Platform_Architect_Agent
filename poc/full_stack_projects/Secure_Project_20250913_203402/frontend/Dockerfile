
# Stage 1: ビルド環境
FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係をコピーしてインストール
COPY package*.json ./
RUN npm install

# ソースコードをコピー
COPY . .

# アプリケーションをビルド
RUN npm run build

# Stage 2: 本番環境
FROM nginx:1.21-alpine

# ビルド成果物をNginxの公開ディレクトリにコピー
COPY --from=builder /app/build /usr/share/nginx/html

# Nginxの設定ファイルをコピー (オプション)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
