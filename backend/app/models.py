from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Union

class TodoBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Union[str, None] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    completed: Union[bool, None] = None

class TodoOut(TodoBase):
    id: int
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
