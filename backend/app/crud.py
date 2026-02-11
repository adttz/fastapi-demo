from typing import Dict, Union
from .models import TodoCreate, TodoUpdate, TodoOut

_db: Dict[int, TodoOut] = {}
_id_counter = 1

def create_todo(todo: TodoCreate) -> TodoOut:
    global _id_counter
    todo_out = TodoOut(
            id = _id_counter,
            title = todo.title,
            description = todo.description,
            completed = False,
    )
    _db[_id_counter] = todo_out
    _id_counter += 1
    return todo_out

def get_all_todos() -> list[TodoOut]:
    return list(_db.values())

def get_todo(todo_id : int) -> Union[TodoOut, None]:
    return _db.get(todo_id)

def update_todo(todo_id : int, data : TodoUpdate) -> Union[TodoOut, None]:
    todo = _db.get(todo_id);
    if not todo:
        return None
    updated = todo.model_copy(update=data.model_dump(exclude_unset=True))
    _db[todo_id] =  updated
    return updated;

def delete_todo(todo_id : int) -> bool:
    return _db.pop(todo_id, None) is not None


