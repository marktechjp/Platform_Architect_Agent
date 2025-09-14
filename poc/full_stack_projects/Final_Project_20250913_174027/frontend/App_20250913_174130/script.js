// script.js
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
});