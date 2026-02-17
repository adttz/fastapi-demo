from fastapi import APIRouter
from . import todos

router = APIRouter()

router.include_router(
    todos.router,
    prefix="/todos",
    tags=["todos"],
)
