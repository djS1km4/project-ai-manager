from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum
from ..database import Base

class TaskStatus(PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys=[assignee_id])
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[creator_id])
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")

# Pydantic models for API
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    assignee_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    estimated_hours: Optional[int] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    estimated_hours: Optional[int] = None
    actual_hours: Optional[int] = None
    due_date: Optional[datetime] = None

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(CommentBase):
    id: int
    task_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: "UserResponse"
    
    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    id: int
    project_id: int
    creator_id: int
    actual_hours: Optional[int] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    assignee: Optional["UserResponse"] = None
    creator: "UserResponse"
    comments: Optional[List[CommentResponse]] = []
    subtasks: Optional[List["TaskResponse"]] = []
    
    class Config:
        from_attributes = True

class TaskSummary(BaseModel):
    id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    assignee_name: Optional[str] = None
    due_date: Optional[datetime] = None
    progress_percentage: Optional[float] = None
    
    class Config:
        from_attributes = True

# Import UserResponse to avoid circular imports
from .user import UserResponse
CommentResponse.model_rebuild()
TaskResponse.model_rebuild()