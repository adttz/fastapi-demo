from typing import Union
from .models import TodoCreate, TodoUpdate
from sqlalchemy.orm import Session
from . import orm_models

def create_todo(db: Session, todo: TodoCreate):
    db_todo = orm_models.Todo(
        title=todo.title,
        description=todo.description,
        completed=False
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_all_todos(db: Session, completed: Union[bool, None]= None):
    query = db.query(orm_models.Todo)

    if completed is not None:
        query = query.filter(
            orm_models.Todo.completed == completed
        )

    return query.order_by(
        orm_models.Todo.completed.asc(),
        orm_models.Todo.id.asc()
    ).all()

def get_todo(db: Session, todo_id: int):
    return db.query(orm_models.Todo).filter(
        orm_models.Todo.id == todo_id
    ).first()

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
