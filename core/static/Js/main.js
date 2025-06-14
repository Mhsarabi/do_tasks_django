const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function addTodo() {
  const text = input.value.trim();
  if (text === '') return;

  fetch('/task/api/v1/task', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
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
  if (noTaskMsg) {
  noTaskMsg.remove();
  }

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

  fetch(`/task/api/v1/task/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
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

  fetch(`/task/api/v1/task/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
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
  fetch(`/task/api/v1/task/${id}`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
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
  list.innerHTML = '<li>⏳ در حال بارگذاری...</li>';

  fetch('/task/api/v1/task')
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

