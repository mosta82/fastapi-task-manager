# from sqlalchemy import Column, Integer, String, Boolean
# from database import Base

# # Define the Task table in the database
# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, nullable=True)
#     is_completed = Column(Boolean, default=False)

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Define the relationship to the Task model
    tasks = relationship("Task", back_populates="owner")


# Define the Task model with a foreign key relationship to the User model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    priority = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")