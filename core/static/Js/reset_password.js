document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reset-password-form');
  const msgElem = document.getElementById('message');

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    msgElem.style.color = 'red';
    msgElem.textContent = '';

    const newPassword = document.getElementById('new_password').value;
    const confirmPassword = document.getElementById('confirm_new_password').value;

    if (newPassword !== confirmPassword) {
      msgElem.textContent = 'رمزهای عبور یکسان نیستند.';
      return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (!token) {
      msgElem.textContent = 'توکن معتبر وجود ندارد.';
      return;
    }

    try {
      const response = await fetch('/account/api/v1/password-reset-confirm?token=' + encodeURIComponent(token), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          new_password: newPassword,
          confirm_new_password: confirmPassword
        })
      });

      const data = await response.json();

      if (response.ok) {
        msgElem.style.color = 'green';
        msgElem.textContent = 'رمز عبور با موفقیت تغییر کرد. در حال انتقال...';

        setTimeout(() => {
          window.location.href = '/account/login/';
        }, 2000);

      } else {
        msgElem.textContent = data.detail || 'خطا در تغییر رمز عبور.';
      }

    } catch (error) {
      msgElem.textContent = 'خطا در ارتباط با سرور.';
    }
  });
});