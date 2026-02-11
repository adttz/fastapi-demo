const API = "http://127.0.0.1:8000";

document.getElementById("addBtn").addEventListener("click", createTodo);

async function loadTodos() {
  const res = await fetch(`${API}/todos`);
  const todos = await res.json();

  const list = document.getElementById("list");
  list.innerHTML = "";

  todos.forEach(t => {
    const li = document.createElement("li");

    const title = document.createElement("div");
    title.className = "todo-title" + (t.completed ? " completed" : "");
    title.textContent = `${t.id}: ${t.title}`;

    const desc = document.createElement("div");
    desc.className = "todo-desc";
    desc.textContent = t.description ?? "";

    const actions = document.createElement("div");
    actions.className = "actions";

    const toggleBtn = document.createElement("button");
    toggleBtn.textContent = t.completed ? "Undo" : "Complete";
    toggleBtn.onclick = () =>
      updateTodo(t.id, { completed: !t.completed });

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";
    editBtn.onclick = () => {
      const newTitle = prompt("New title", t.title);
      if (newTitle)
        updateTodo(t.id, { title: newTitle });
    };

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => deleteTodo(t.id);

    actions.appendChild(toggleBtn);
    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    li.appendChild(title);
    li.appendChild(desc);
    li.appendChild(actions);

    list.appendChild(li);
  });
}

async function createTodo() {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;
  if (!title) return;

  await fetch(`${API}/todos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description }),
  });

  document.getElementById("title").value = "";
  document.getElementById("description").value = "";
  loadTodos();
}

async function updateTodo(id, data) {
  await fetch(`${API}/todos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  loadTodos();
}

async function deleteTodo(id) {
  await fetch(`${API}/todos/${id}`, { method: "DELETE" });
  loadTodos();
}

loadTodos();
