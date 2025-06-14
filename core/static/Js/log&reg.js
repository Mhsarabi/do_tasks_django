document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('login-form');
  form.addEventListener('submit', function (event) {
    alert('در حال ورود...');
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('register-form');
  form.addEventListener('submit', function (event) {
    alert('در حال ثبت نام...');
  });
});