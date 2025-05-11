// 登录页面逻辑
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.form-signin form');
    const errorMessage = document.querySelector('.error-message');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = document.querySelector('input[name="name"]').value;
            const password = document.querySelector('input[name="password"]').value;
            
            try {
                const response = await fetch('/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        name: name,
                        password: password
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (data.redirect_url) {
                        window.location.href = data.redirect_url;
                    } else {
                        window.location.href = '/';
                    }
                } else {
                    showError(data.message || '登录失败，请检查用户名和密码');
                }
            } catch (error) {
                showError('登录失败，请稍后重试');
            }
        });
    }
    
    function showError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
        }
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 