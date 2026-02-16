const API = "http://127.0.0.1:8000";

document.getElementById("addBtn").addEventListener("click", createTodo);

async function loadTodos() {
  const filter = document.getElementById("filter").value;

  let url = `${API}/todos`;

  if (filter !== "") {
    url += `?completed=${filter}`;
  }
  
  const res = await fetch(url);
  const todos = await res.json();
  
  const list = document.getElementById("list");
  list.innerHTML = "";

  todos.forEach(t => {
    const li = document.createElement("li");

    const title = document.createElement("div");
    title.className = "title";

    const todo = document.createElement("div");
todo.className = "todo" + (t.completed ? " completed" : "");
    todo.textContent = `${t.title}`;
    
    const todo_id = document.createElement("div");
    todo_id.className = "todo_id";
    todo_id.textContent = `#ID: ${t.id}`;
    
    title.appendChild(todo);
    title.appendChild(todo_id);

    const desc = document.createElement("div");
    desc.className = "todo-desc" + (t.completed ? " completed" : "");
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

    const created = document.createElement("div");
    created.className = "todo-meta";

    const dateObj = new Date(t.created_at);

    const time = document.createElement("div");
    time.textContent = dateObj.toLocaleTimeString();

    const date = document.createElement("div");
    date.textContent = dateObj.toLocaleDateString();

    created.appendChild(time);
    created.appendChild(date);

    actions.appendChild(toggleBtn);
    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);
    actions.appendChild(created)

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

document.getElementById("filter").addEventListener("change", loadTodos);

loadTodos();
