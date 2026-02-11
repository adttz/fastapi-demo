from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .models import TodoCreate, TodoOut, TodoUpdate
from . import crud

app = FastAPI(title = "Todo Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo : TodoCreate):
    return crud.create_todo(todo)

@app.get("/todos", response_model=list[TodoOut])
def list_todos():
    return crud.get_all_todos()

@app.get("/todos/{todo_id}", response_model=TodoOut)
def get_todo(todo_id : int):
    todo = crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoOut)
def update_todo(todo_id : int, data : TodoUpdate):
    todo = crud.update_todo(todo_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id : int):
    if not crud.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo Not Found")
