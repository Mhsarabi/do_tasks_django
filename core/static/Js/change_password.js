document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('change-password-form');

  if (form) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();

      const oldPassword = document.getElementById('old_password').value;
      const newPassword = document.getElementById('new_password').value;
      const confirmPassword = document.getElementById('confirm_new_password').value;

      const token = localStorage.getItem('access_token');

      if (!token) {
        alert("توکن یافت نشد. لطفاً دوباره وارد شوید.");
        return;
      }

      try {
        const response = await fetch('/account/api/v1/change-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword,
            confirm_new_password: confirmPassword
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert("رمز عبور با موفقیت تغییر کرد.");
          window.location.href = '/';  // یا صفحه دلخواه
        } else {
          alert("خطا: " + (data.details || data.old_password || JSON.stringify(data)));
        }
      } catch (err) {
        alert("خطای شبکه. لطفاً دوباره تلاش کنید.");
        console.error(err);
      }
    });
  }
});