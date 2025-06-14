const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');

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

function addTodo() {
  console.log("addTodo called ✅");
  const text = input.value.trim();
  if (text === '') return;

  fetch(addTaskUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ task: text })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        addTaskToDOM(text, data.task_id);
        input.value = '';
      } else {
        alert('خطا در ذخیره‌سازی: ' + (data.error || 'نامشخص'));
      }
    });
}

function addTaskToDOM(text, id) {
  if (list.children.length === 1 && list.children[0].textContent.trim() === '.هیچ کاری اضافه نشده است') {
    list.children[0].remove();
  }
  const li = document.createElement('li');
  li.setAttribute('data-id', id);

  const span = document.createElement('span');
  span.textContent = text;
  li.appendChild(span);

  const actions = document.createElement('div');
  actions.classList.add('actions');

  const doneBtn = document.createElement('button');
  doneBtn.textContent = '✔';
  doneBtn.onclick = () => toggleDone(id, li);

  const deleteBtn = document.createElement('button');
  deleteBtn.textContent = '🗑';
  deleteBtn.onclick = () => deleteTask(id, li);
  
  const editBtn = document.createElement('button');
  editBtn.textContent = '✏️';
  editBtn.onclick = () => editTask(id, span, li);

  actions.appendChild(doneBtn);
  actions.appendChild(editBtn);
  actions.appendChild(deleteBtn);

  li.appendChild(actions);
  list.appendChild(li);
}

function toggleDone(id, liElement) {
   fetch(`/task/toggle_done/${id}`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      if (data.done) {
        liElement.classList.add('completed');
      } else {
        liElement.classList.remove('completed');
      }
    } else {
      alert('خطا در تغییر وضعیت تسک: ' + (data.error || 'نامشخص'));
    }
  })
  .catch(() => alert('خطا در اتصال به سرور'));
}

function editTask(id, spanElement, liElement) {
  const span = liElement.querySelector('span');
  const oldText = span.textContent;

  const input = document.createElement('input');
  input.type = 'text';
  input.value = oldText;

  liElement.replaceChild(input, span);

  const actionsDiv = liElement.querySelector('.actions');


  actionsDiv.innerHTML = '';


  const saveBtn = document.createElement('button');
  saveBtn.textContent = '💾';
  saveBtn.onclick = () => saveEdit(id, input, liElement);


  const cancelBtn = document.createElement('button');
  cancelBtn.textContent = '❌';
  cancelBtn.onclick = () => {
    liElement.replaceChild(span, input); 
    actionsDiv.innerHTML = ''; 
    createDefaultButtons(id, liElement);
  };

  actionsDiv.appendChild(saveBtn);
  actionsDiv.appendChild(cancelBtn);
}

function saveEdit(id, inputElement, liElement) {
  const newText = inputElement.value.trim();
  if (newText === '') return;

  fetch(`/task/edit/${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ task: newText }),
  })
    .then(res => res.json())
    .then(data => {
  if (data.success) {
    const newSpan = document.createElement('span');
    newSpan.textContent = newText;
    inputElement.replaceWith(newSpan);
    createDefaultButtons(id, liElement);
  } else {
    alert('خطا در ویرایش تسک: ' + (data.error || 'نامشخص'));
  }
})
    .catch(() => alert('خطا در اتصال به سرور'));
}

function deleteTask(id, liElement) {
  fetch(`/task/delete/${id}`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        liElement.remove();
      } else {
        alert('خطا در حذف تسک: ' + (data.error || 'نامشخص'));
      }
    })
    .catch(err => alert('خطا در اتصال به سرور'));
}

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') addTodo();
});

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
document.querySelectorAll('#todo-list li').forEach(li => {
  const id = li.getAttribute('data-id');
  if (!id) return;
  if (!li.querySelector('.actions')) {
    const actions = document.createElement('div');
    actions.classList.add('actions');
    li.appendChild(actions);
  }
  createDefaultButtons(id, li);
});