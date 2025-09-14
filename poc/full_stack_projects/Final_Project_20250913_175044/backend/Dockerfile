
FROM node:18-alpine

WORKDIR /app

# AIが生成したアプリケーションが含まれるサブディレクトリからpackage.jsonをコピー
COPY API_20250913_175146/package*.json ./
RUN npm install --production

# AIが生成したアプリケーションが含まれるサブディレクトリからソースコードを全てコピー
COPY API_20250913_175146/. .

EXPOSE 8080

CMD ["node", "server.js"]
