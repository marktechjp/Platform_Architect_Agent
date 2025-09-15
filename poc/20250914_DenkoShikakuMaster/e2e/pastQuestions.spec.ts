import { device, element, by, expect, waitFor } from 'detox';

describe('電工資格マスター - 過去問題学習フロー', () => {
  // テストスイートの開始前に、アプリをクリーンな状態で起動する
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('ユーザーはログイン後、過去問題を選択して学習を開始できるべき', async () => {
    // --- ログイン処理 ---
    // ログイン画面が表示されていることを確認
    await expect(element(by.id('login-screen'))).toBeVisible();

    // テスト用の認証情報を入力
    // NOTE: 本来は環境変数やセキュアな方法で管理します
    await element(by.id('email-input')).typeText('qa-tester@example.com');
    await element(by.id('password-input')).typeText('SecurePassword123!');
    
    // ログインボタンをタップ
    await element(by.id('login-button')).tap();

    // --- ホーム画面 ---
    // ホーム画面（ダッシュボード）への遷移を待機し、表示を確認
    await waitFor(element(by.id('home-screen'))).toBeVisible().withTimeout(10000); // ネットワーク状況を考慮して長めのタイムアウト
    await expect(element(by.id('welcome-message'))).toBeVisible();

    // 「過去問題」へのナビゲーションボタンをタップ
    await element(by.id('navigate-past-questions-button')).tap();

    // --- 過去問題一覧画面 ---
    // 過去問題一覧画面への遷移を待機し、表示を確認
    await waitFor(element(by.id('past-questions-list-screen'))).toBeVisible().withTimeout(5000);
    
    // 特定の年度・期の試験項目が表示されていることを確認
    const targetTestItem = element(by.id('test-item-2nd-class-2024-first-half'));
    await expect(targetTestItem).toBeVisible();

    // 対象の試験項目をタップ
    await targetTestItem.tap();

    // --- 問題詳細画面 ---
    // 問題詳細画面への遷移を待機し、表示を確認
    await waitFor(element(by.id('question-screen'))).toBeVisible().withTimeout(5000);

    // 最初の問題（問1）が表示されていることを確認
    await expect(element(by.id('question-number-text'))).toHaveText('問1');
    await expect(element(by.id('question-body-text'))).toBeVisible();
    
    // 選択肢が表示されていることを確認
    await expect(element(by.id('choice-button-a'))).toBeVisible();
    await expect(element(by.id('choice-button-b'))).toBeVisible();
    await expect(element(by.id('choice-button-c'))).toBeVisible();
    await expect(element(by.id('choice-button-d'))).toBeVisible();

    // 選択肢の一つをタップ（例：選択肢 'a'）
    await element(by.id('choice-button-a')).tap();

    // 解答後のフィードバック（例：解説表示ボタン）が表示されることを確認
    await expect(element(by.id('show-explanation-button'))).toBeVisible();
  });
});
