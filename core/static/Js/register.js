document.addEventListener('DOMContentLoaded', function () {
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
      event.preventDefault();

      const email = registerForm.querySelector('input[name="email"]').value;
      const password1 = registerForm.querySelector('input[name="password1"]').value;
      const password2 = registerForm.querySelector('input[name="password2"]').value;

      try {
        const response = await fetch('/account/api/v1/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // 'X-CSRFToken': getCookie('csrftoken') 
          },
          body: JSON.stringify({
            email: email,
            password: password1,
            password_confirm: password2
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert('ثبت‌نام موفق! خوش آمدید');
          localStorage.setItem('access_token', data.access);
          localStorage.setItem('refresh_token', data.refresh);
          window.location.href = '/'; 
        } else {
          alert('خطا: ' + JSON.stringify(data));
        }
      } catch (error) {
        console.error(error);
        alert('خطای شبکه!');
      }
    });
  }
});