document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('reset-request-form');
  const msgElem = document.getElementById('message');

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    msgElem.style.color = 'red';
    msgElem.textContent = '';

    const email = document.getElementById('email').value;

    try {
      const response = await fetch('/account/api/v1/password-reset', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (response.ok) {
        msgElem.style.color = 'green';
        msgElem.textContent =  'لینک بازیابی به ایمیل شما ارسال شد.';
      } else {
        msgElem.textContent =  'ارسال ناموفق بود.';
      }
    } catch (error) {
      msgElem.textContent = 'خطا در ارتباط با سرور.';
    }
  });
});