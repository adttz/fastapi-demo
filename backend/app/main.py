from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import orm_models, crud, models

orm_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Todo List")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos", response_model=models.TodoOut)
def create(todo: models.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.get("/todos", response_model=list[models.TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return crud.get_all_todos(db)


@app.get("/todos/{todo_id}", response_model=models.TodoOut)
def get(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@app.put("/todos/{todo_id}", response_model=models.TodoOut)
def update(todo_id: int, data: models.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, todo_id, data)
    if not todo:
        raise HTTPException(status_code=404)
    return todo


@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    if not crud.delete_todo(db, todo_id):
        raise HTTPException(status_code=404)
    return {"message": "deleted"}
