
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
