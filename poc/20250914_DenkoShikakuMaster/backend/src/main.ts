import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // CORSのオプションを明示的に設定
  app.enableCors({
    origin: 'http://localhost:5173', // フロントエンドのURLを許可
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
  });

  await app.listen(3010);
}
bootstrap();
