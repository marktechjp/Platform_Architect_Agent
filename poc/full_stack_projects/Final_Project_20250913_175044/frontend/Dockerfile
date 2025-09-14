# Stage 1: 本番環境
# シンプルな静的コンテンツ配信用のNginxイメージを使用
FROM nginx:1.21-alpine

# AIが生成したアプリケーションの静的ファイルをNginxの公開ディレクトリにコピー
# 'App_20250913_175145'の部分は実際のフォルダ名に合わせてください
COPY ./App_20250913_175145/ /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
