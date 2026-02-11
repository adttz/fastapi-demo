import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchTodos();
  }, []);

  async function fetchTodos() {
    const res = await fetch(`${API}/todos`);
    setTodos(await res.json());
  }

  async function addTodo() {
    if (!title) return;

    await fetch(`${API}/todos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });

    setTitle("");
    fetchTodos();
  }

  async function toggleTodo(todo) {
    await fetch(`${API}/todos/${todo.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: !todo.completed }),
    });
    fetchTodos();
  }

  async function updateTitle(todo, newTitle) {
    if (!newTitle) return;

    await fetch(`${API}/todos/${todo.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle }),
    });
    fetchTodos();
  }

  async function deleteTodo(id) {
    await fetch(`${API}/todos/${id}`, {
      method: "DELETE",
    });
    fetchTodos();
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Todo Demo</h2>

      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New todo"
      />
      <button onClick={addTodo}>Add</button>

      <ul>
        {todos.map((t) => (
          <li key={t.id}>
            <input
              defaultValue={t.title}
              onBlur={(e) => updateTitle(t, e.target.value)}
            />
            [{t.completed ? "done" : "pending"}]

            <button onClick={() => toggleTodo(t)}>Toggle</button>
            <button onClick={() => deleteTodo(t.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
