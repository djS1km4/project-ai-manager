from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..database import get_db
from ..models.task import (
    Task, TaskCreate, TaskUpdate, TaskResponse, TaskSummary,
    Comment, CommentCreate, CommentUpdate, CommentResponse,
    TaskStatus, TaskPriority
)
from ..services.auth_service import AuthService
from ..services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    return AuthService.get_current_user_from_token(db, token)

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    task_service = TaskService()
    try:
        db_task = task_service.create_task(db, task, current_user.id)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks with filtering options"""
    task_service = TaskService()
    tasks = task_service.get_tasks(
        db, current_user.id, project_id, assignee_id, status, priority,
        search, due_date_from, due_date_to, skip, limit
    )
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task"""
    task_service = TaskService()
    task = task_service.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    task_service = TaskService()
    updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task_service = TaskService()
    success = task_service.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

# Subtasks
@router.get("/{task_id}/subtasks", response_model=List[TaskResponse])
def get_subtasks(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all subtasks of a parent task"""
    task_service = TaskService()
    subtasks = task_service.get_subtasks(db, task_id, current_user.id)
    return subtasks

# Comments
@router.post("/{task_id}/comments", response_model=CommentResponse)
def add_comment(
    task_id: int,
    comment: CommentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a task"""
    task_service = TaskService()
    try:
        db_comment = task_service.add_comment(db, task_id, comment, current_user.id)
        return db_comment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding comment: {str(e)}"
        )

@router.get("/{task_id}/comments", response_model=List[CommentResponse])
def get_task_comments(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all comments for a task"""
    task_service = TaskService()
    comments = task_service.get_task_comments(db, task_id, current_user.id)
    return comments

@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    content: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a comment"""
    task_service = TaskService()
    updated_comment = task_service.update_comment(db, comment_id, content, current_user.id)
    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return updated_comment

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a comment"""
    task_service = TaskService()
    success = task_service.delete_comment(db, comment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return {"message": "Comment deleted successfully"}

# Task Status Management
@router.put("/{task_id}/status")
def update_task_status(
    task_id: int,
    new_status: TaskStatus,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update task status"""
    task_service = TaskService()
    
    # Create update object with just the status
    from ..models.task import TaskUpdate
    task_update = TaskUpdate(status=new_status)
    
    updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {
        "message": f"Task status updated to {new_status}",
        "task": updated_task
    }

@router.put("/{task_id}/assign")
def assign_task(
    task_id: int,
    assignee_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign task to a user"""
    task_service = TaskService()
    
    from ..models.task import TaskUpdate
    task_update = TaskUpdate(assignee_id=assignee_id)
    
    updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {
        "message": "Task assigned successfully",
        "task": updated_task
    }

@router.put("/{task_id}/unassign")
def unassign_task(
    task_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unassign task from current assignee"""
    task_service = TaskService()
    
    from ..models.task import TaskUpdate
    task_update = TaskUpdate(assignee_id=None)
    
    updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {
        "message": "Task unassigned successfully",
        "task": updated_task
    }

# Analytics and Reports
@router.get("/analytics/user-summary")
def get_user_tasks_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get summary of tasks assigned to current user"""
    task_service = TaskService()
    summary = task_service.get_user_tasks_summary(db, current_user.id)
    return summary

@router.get("/analytics/project/{project_id}")
def get_project_tasks_analytics(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics for tasks in a specific project"""
    task_service = TaskService()
    analytics = task_service.get_project_tasks_analytics(db, project_id, current_user.id)
    return analytics

# Quick Actions
@router.get("/my-tasks")
def get_my_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks assigned to current user"""
    task_service = TaskService()
    tasks = task_service.get_tasks(
        db, current_user.id, 
        assignee_id=current_user.id,
        status=status,
        priority=priority,
        skip=skip,
        limit=limit
    )
    return tasks

@router.get("/overdue")
def get_overdue_tasks(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overdue tasks for current user"""
    task_service = TaskService()
    
    # Get tasks due before now that are not completed
    now = datetime.utcnow()
    tasks = task_service.get_tasks(
        db, current_user.id,
        assignee_id=current_user.id,
        due_date_to=now,
        limit=1000
    )
    
    # Filter out completed tasks
    overdue_tasks = [
        task for task in tasks 
        if task.status != TaskStatus.DONE and task.due_date and task.due_date < now
    ]
    
    return {
        "overdue_tasks": overdue_tasks,
        "count": len(overdue_tasks)
    }

@router.get("/upcoming")
def get_upcoming_tasks(
    days: int = Query(7, ge=1, le=30),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get upcoming tasks for current user"""
    task_service = TaskService()
    
    from datetime import timedelta
    now = datetime.utcnow()
    future_date = now + timedelta(days=days)
    
    tasks = task_service.get_tasks(
        db, current_user.id,
        assignee_id=current_user.id,
        due_date_from=now,
        due_date_to=future_date,
        limit=1000
    )
    
    # Filter out completed tasks
    upcoming_tasks = [
        task for task in tasks 
        if task.status != TaskStatus.DONE
    ]
    
    return {
        "upcoming_tasks": upcoming_tasks,
        "count": len(upcoming_tasks),
        "period_days": days
    }

# Bulk Operations
@router.put("/bulk/status")
def bulk_update_status(
    task_ids: List[int],
    new_status: TaskStatus,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update status for multiple tasks"""
    task_service = TaskService()
    
    updated_tasks = []
    errors = []
    
    for task_id in task_ids:
        try:
            from ..models.task import TaskUpdate
            task_update = TaskUpdate(status=new_status)
            updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
            if updated_task:
                updated_tasks.append(updated_task)
            else:
                errors.append(f"Task {task_id} not found")
        except Exception as e:
            errors.append(f"Task {task_id}: {str(e)}")
    
    return {
        "updated_tasks": updated_tasks,
        "updated_count": len(updated_tasks),
        "errors": errors
    }

@router.put("/bulk/assign")
def bulk_assign_tasks(
    task_ids: List[int],
    assignee_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign multiple tasks to a user"""
    task_service = TaskService()
    
    updated_tasks = []
    errors = []
    
    for task_id in task_ids:
        try:
            from ..models.task import TaskUpdate
            task_update = TaskUpdate(assignee_id=assignee_id)
            updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
            if updated_task:
                updated_tasks.append(updated_task)
            else:
                errors.append(f"Task {task_id} not found")
        except Exception as e:
            errors.append(f"Task {task_id}: {str(e)}")
    
    return {
        "updated_tasks": updated_tasks,
        "updated_count": len(updated_tasks),
        "errors": errors
    }