# from pydantic import BaseModel

# # Base schema with shared attributes
# class TaskBase(BaseModel):
#     title: str
#     description: str | None = None
#     is_completed: bool = False

# # Schema for creating a task (Input)
# class TaskCreate(TaskBase):
#     pass

# # Schema for reading/returning a task (Output)
# class TaskResponse(TaskBase):
#     id: int

#     class Config:
#         from_attributes = True  # Allows mapping from SQLAlchemy models to Pydantic
from typing import Optional

from pydantic import BaseModel

# --- Task Schemas  ---
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner_id: Optional[int] = None # which user created this task

    class Config:
        from_attributes = True

# --- User Schemas ( ) ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    tasks: list[TaskResponse] = []

    class Config:
        from_attributes = True