document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('/account/api/v1/jwt/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: email,
            password: password
          })
        });

        const data = await response.json();

        console.log("Response status:", response.status);
        console.log("Response data:", data);

        if (response.ok) {
          // تشخیص نوع توکن
          if (data.access && data.refresh) {
            // JWT
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            console.log("Login success (JWT)");
          } else if (data.token) {
            // TokenAuthentication
            localStorage.setItem('token', data.token);
            console.log("Login success (TokenAuth)");
          } else {
            console.warn("No token found in response!");
          }

          alert('ورود موفق!');
          window.location.href = '/';
        } else {
          alert('ورود ناموفق: ' + (data.detail || JSON.stringify(data)));
        }
      } catch (error) {
        console.error("Login error:", error);
        alert('خطای شبکه! لطفاً دوباره تلاش کنید.');
      }
    });
  }
});