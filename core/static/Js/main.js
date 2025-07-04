const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');

function getToken() {
  const token = localStorage.getItem('access_token');
  if (!token) {
    alert("لطفاً ابتدا وارد شوید.");
    window.location.href = "/account/login/";
  }
  return token;
}

function authFetch(url, options = {}) {
  const token = getToken();
  if (!options.headers) options.headers = {};
  options.headers['Authorization'] = 'Bearer ' + token;

  return fetch(url, options).then(response => {
    if (response.status === 401) {
      alert("دسترسی غیرمجاز. لطفاً دوباره وارد شوید.");
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = "/account/login/";
      throw new Error("Unauthorized");
    }
    return response;
  });
}

function addTodo() {
  const text = input.value.trim();
  if (text === '') return;

  authFetch('/task/api/v1/task', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ task: text })
  })
    .then(res => res.json())
    .then(data => {
      addTaskToDOM(data.task, data.id, data.done);
      input.value = '';
    })
    .catch(() => alert('خطا در افزودن تسک'));
}

function addTaskToDOM(text, id, done = false) {
  const noTaskMsg = document.getElementById('no-task-msg');
  if (noTaskMsg) noTaskMsg.remove();

  const li = document.createElement('li');
  li.setAttribute('data-id', id);
  if (done) li.classList.add('completed');

  const span = document.createElement('span');
  span.textContent = text;
  li.appendChild(span);

  const actions = document.createElement('div');
  actions.classList.add('actions');

  const doneBtn = document.createElement('button');
  doneBtn.textContent = '✔';
  doneBtn.onclick = () => toggleDone(id, li);

  const editBtn = document.createElement('button');
  editBtn.textContent = '✏️';
  editBtn.onclick = () => editTask(id, span, li);

  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = '🗑';
  deleteBtn.onclick = () => deleteTask(id, li);

  actions.appendChild(doneBtn);
  actions.appendChild(editBtn);
  actions.appendChild(deleteBtn);

  li.appendChild(actions);
  list.appendChild(li);
}

function toggleDone(id, liElement) {
  const newDoneStatus = !liElement.classList.contains('completed');

  authFetch(`/task/api/v1/task/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ done: newDoneStatus })
  })
    .then(res => res.json())
    .then(data => {
      liElement.classList.toggle('completed', data.done);
    })
    .catch(() => alert('خطا در تغییر وضعیت تسک'));
}

function editTask(id, spanElement, liElement) {
  const oldText = spanElement.textContent;
  const input = document.createElement('input');
  input.type = 'text';
  input.value = oldText;

  liElement.replaceChild(input, spanElement);

  const actionsDiv = liElement.querySelector('.actions');
  actionsDiv.innerHTML = '';

  const saveBtn = document.createElement('button');
  saveBtn.textContent = '💾';
  saveBtn.onclick = () => saveEdit(id, input, liElement);

  const cancelBtn = document.createElement('button');
  cancelBtn.textContent = '❌';
  cancelBtn.onclick = () => {
    liElement.replaceChild(spanElement, input);
    createDefaultButtons(id, liElement);
  };

  actionsDiv.appendChild(saveBtn);
  actionsDiv.appendChild(cancelBtn);
}

function saveEdit(id, inputElement, liElement) {
  const newText = inputElement.value.trim();
  if (newText === '') return;

  authFetch(`/task/api/v1/task/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ task: newText })
  })
    .then(res => res.json())
    .then(data => {
      const newSpan = document.createElement('span');
      newSpan.textContent = data.task;
      liElement.replaceChild(newSpan, inputElement);
      createDefaultButtons(id, liElement);
    })
    .catch(() => alert('خطا در ویرایش تسک'));
}

function deleteTask(id, liElement) {
  authFetch(`/task/api/v1/task/${id}`, {
    method: 'DELETE'
  })
    .then(res => {
      if (res.status === 204) {
        liElement.remove();
      } else {
        alert('خطا در حذف تسک');
      }
    })
    .catch(() => alert('خطا در حذف تسک'));
}

function createDefaultButtons(id, liElement) {
  const actions = liElement.querySelector('.actions');
  actions.innerHTML = '';

  const doneBtn = document.createElement('button');
  doneBtn.textContent = '✔';
  doneBtn.onclick = () => toggleDone(id, liElement);

  const editBtn = document.createElement('button');
  editBtn.textContent = '✏️';
  const span = liElement.querySelector('span');
  editBtn.onclick = () => editTask(id, span, liElement);

  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = '🗑';
  deleteBtn.onclick = () => deleteTask(id, liElement);

  actions.appendChild(doneBtn);
  actions.appendChild(editBtn);
  actions.appendChild(deleteBtn);
}

window.addEventListener('DOMContentLoaded', () => {
  // بررسی اولیه توکن و هدایت به login در صورت نیاز
  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('برای مشاهده تسک‌ها ابتدا وارد شوید.');
    window.location.href = '/account/login/';
    return;
  }

  list.innerHTML = '<li>⏳ در حال بارگذاری...</li>';

  authFetch('/task/api/v1/task')
    .then(res => res.json())
    .then(data => {
      list.innerHTML = '';
      if (data.length === 0) {
        const msg = document.createElement('li');
        msg.id = 'no-task-msg';
        msg.textContent = 'هیچ تسکی موجود نیست';
        list.appendChild(msg);
        return;
      }
      data.forEach(task => {
        addTaskToDOM(task.task, task.id, task.done);
      });
    })
    .catch(() => {
      list.innerHTML = '<li>❌ خطا در دریافت لیست تسک‌ها</li>';
    });
});

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') addTodo();
});

function logout() {
  const token = localStorage.getItem('token'); // توکن rest_framework TokenAuthentication

  if (token) {
    fetch('/account/api/v1/logout', {
      method: 'POST',
      headers: {
        'Authorization': 'Token ' + token,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        console.warn('خطا در حذف توکن از سرور');
      }
    })
    .catch(() => console.warn('خطا در حذف توکن از سرور'));
  }

  // پاک کردن توکن‌های localStorage
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('token');

  window.location.href = "/account/login/";
}
