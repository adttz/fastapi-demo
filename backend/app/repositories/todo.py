from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from typing import Union

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=False,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_all_todos(db: Session, completed: Union[bool, None] = None):
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    return query.order_by(
        Todo.completed.asc(),
        Todo.id.asc(),
    ).all()


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, data: TodoUpdate):
    todo = get_todo(db, todo_id)
    if not todo:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)
    if not todo:
        return False

    db.delete(todo)
    db.commit()
    return True
