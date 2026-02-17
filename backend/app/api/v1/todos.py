from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut
from app.repositories import todo as todo_repo

router = APIRouter()


@router.post("", response_model=TodoOut)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return todo_repo.create_todo(db, todo)


@router.get("", response_model=list[TodoOut])
def list_todos(
    completed: Union[bool, None] = Query(default=None),
    db: Session = Depends(get_db),
):
    return todo_repo.get_all_todos(db, completed)


@router.get("/{todo_id}", response_model=TodoOut)
def get(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_repo.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@router.put("/{todo_id}", response_model=TodoOut)
def update(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    todo = todo_repo.update_todo(db, todo_id, data)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    if not todo_repo.delete_todo(db, todo_id):
        raise HTTPException(status_code=404)
    return {"message": "deleted"}
