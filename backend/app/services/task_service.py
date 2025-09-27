from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from ..models.task import Task, Comment, TaskCreate, TaskUpdate, CommentCreate, TaskStatus, TaskPriority
from ..models.project import Project, ProjectMember
from ..models.user import User
from fastapi import HTTPException, status

class TaskService:
    def create_task(self, db: Session, task: TaskCreate, creator_id: int) -> Task:
        """Create a new task"""
        # Verify project exists and user has access
        project = db.query(Project).filter(Project.id == task.project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Check if user has access to the project
        if not self._user_has_project_access(db, task.project_id, creator_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )
        
        # Verify assignee exists and has access to project if specified
        if task.assignee_id:
            if not self._user_has_project_access(db, task.project_id, task.assignee_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assignee does not have access to this project"
                )
        
        # Verify parent task exists and belongs to same project if specified
        if task.parent_task_id:
            parent_task = db.query(Task).filter(Task.id == task.parent_task_id).first()
            if not parent_task or parent_task.project_id != task.project_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Parent task not found or belongs to different project"
                )
        
        task_data = task.dict()
        db_task = Task(
            **task_data,
            creator_id=creator_id
        )
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    def get_task(self, db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """Get a task by ID if user has access"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        
        # Check if user has access to the project
        if not self._user_has_project_access(db, task.project_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this task"
            )
        
        return task
    
    def get_tasks(
        self,
        db: Session,
        user_id: int,
        project_id: Optional[int] = None,
        assignee_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        search: Optional[str] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Get tasks with filtering options"""
        # Check if user is admin
        user = db.query(User).filter(User.id == user_id).first()
        is_admin = user and user.is_admin
        
        if is_admin:
            # Admins can see all tasks
            query = db.query(Task).join(Project)
        else:
            # Base query - only tasks from projects user has access to
            query = db.query(Task).join(Project).join(ProjectMember).filter(
                ProjectMember.user_id == user_id
            )
        
        # Apply filters
        if project_id:
            # Verify user has access to specific project
            if not self._user_has_project_access(db, project_id, user_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this project"
                )
            query = query.filter(Task.project_id == project_id)
        
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if search:
            query = query.filter(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%")
                )
            )
        
        if due_date_from:
            query = query.filter(Task.due_date >= due_date_from)
        
        if due_date_to:
            query = query.filter(Task.due_date <= due_date_to)
        
        return query.offset(skip).limit(limit).all()
    
    def update_task(self, db: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
        """Update a task"""
        task = self.get_task(db, task_id, user_id)
        if not task:
            return None
        
        # Check if user can edit this task
        if not self._user_can_edit_task(db, task_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to edit this task"
            )
        
        update_data = task_update.dict(exclude_unset=True)
        
        # Verify assignee has access to project if being changed
        if "assignee_id" in update_data and update_data["assignee_id"]:
            if not self._user_has_project_access(db, task.project_id, update_data["assignee_id"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New assignee does not have access to this project"
                )
        
        # Handle status changes
        if "status" in update_data:
            new_status = update_data["status"]
            if new_status == TaskStatus.DONE and task.status != TaskStatus.DONE:
                update_data["completed_at"] = datetime.utcnow()
            elif new_status != TaskStatus.DONE and task.status == TaskStatus.DONE:
                update_data["completed_at"] = None
        
        for field, value in update_data.items():
            setattr(task, field, value)
        
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
        return task
    
    def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """Delete a task"""
        task = self.get_task(db, task_id, user_id)
        if not task:
            return False
        
        # Check if user can delete this task
        if not self._user_can_delete_task(db, task_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to delete this task"
            )
        
        # Check if task has subtasks
        subtasks = db.query(Task).filter(Task.parent_task_id == task_id).all()
        if subtasks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete task with subtasks. Delete subtasks first."
            )
        
        db.delete(task)
        db.commit()
        return True
    
    def get_subtasks(self, db: Session, parent_task_id: int, user_id: int) -> List[Task]:
        """Get all subtasks of a parent task"""
        # Verify parent task exists and user has access
        parent_task = self.get_task(db, parent_task_id, user_id)
        if not parent_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent task not found"
            )
        
        return db.query(Task).filter(Task.parent_task_id == parent_task_id).all()
    
    def add_comment(self, db: Session, task_id: int, comment: CommentCreate, user_id: int) -> Comment:
        """Add a comment to a task"""
        # Verify task exists and user has access
        task = self.get_task(db, task_id, user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        db_comment = Comment(
            **comment.dict(),
            task_id=task_id,
            author_id=user_id
        )
        
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    def get_task_comments(self, db: Session, task_id: int, user_id: int) -> List[Comment]:
        """Get all comments for a task"""
        # Verify task exists and user has access
        task = self.get_task(db, task_id, user_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()
    
    def update_comment(self, db: Session, comment_id: int, content: str, user_id: int) -> Optional[Comment]:
        """Update a comment"""
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return None
        
        # Only author can edit their comment
        if comment.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only edit your own comments"
            )
        
        comment.content = content
        comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(comment)
        return comment
    
    def delete_comment(self, db: Session, comment_id: int, user_id: int) -> bool:
        """Delete a comment"""
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return False
        
        # Only author can delete their comment, or project admin
        if comment.author_id != user_id:
            # Check if user is project admin
            task = db.query(Task).filter(Task.id == comment.task_id).first()
            if not task or not self._user_can_manage_project(db, task.project_id, user_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions to delete this comment"
                )
        
        db.delete(comment)
        db.commit()
        return True
    
    def get_user_tasks_summary(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get summary of tasks assigned to user"""
        # Get all tasks assigned to user
        user_tasks = db.query(Task).filter(Task.assignee_id == user_id).all()
        
        # Calculate statistics
        total_tasks = len(user_tasks)
        completed_tasks = len([t for t in user_tasks if t.status == TaskStatus.DONE])
        in_progress_tasks = len([t for t in user_tasks if t.status == TaskStatus.IN_PROGRESS])
        todo_tasks = len([t for t in user_tasks if t.status == TaskStatus.TODO])
        
        # Get overdue tasks
        overdue_tasks = [
            t for t in user_tasks 
            if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE
        ]
        
        # Get upcoming tasks (due in next 7 days)
        next_week = datetime.utcnow() + timedelta(days=7)
        upcoming_tasks = [
            t for t in user_tasks
            if t.due_date and datetime.utcnow() <= t.due_date <= next_week and t.status != TaskStatus.DONE
        ]
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Get tasks by priority
        high_priority_tasks = len([t for t in user_tasks if t.priority == TaskPriority.HIGH and t.status != TaskStatus.DONE])
        medium_priority_tasks = len([t for t in user_tasks if t.priority == TaskPriority.MEDIUM and t.status != TaskStatus.DONE])
        low_priority_tasks = len([t for t in user_tasks if t.priority == TaskPriority.LOW and t.status != TaskStatus.DONE])
        
        return {
            "user_id": user_id,
            "total_tasks": total_tasks,
            "task_status_breakdown": {
                "completed": completed_tasks,
                "in_progress": in_progress_tasks,
                "todo": todo_tasks
            },
            "completion_rate": round(completion_rate, 1),
            "overdue_tasks": len(overdue_tasks),
            "upcoming_tasks": len(upcoming_tasks),
            "priority_breakdown": {
                "high": high_priority_tasks,
                "medium": medium_priority_tasks,
                "low": low_priority_tasks
            },
            "recent_overdue": [
                {
                    "id": t.id,
                    "title": t.title,
                    "due_date": t.due_date.isoformat(),
                    "project_id": t.project_id
                }
                for t in overdue_tasks[:5]  # Limit to 5 most recent
            ],
            "upcoming_deadlines": [
                {
                    "id": t.id,
                    "title": t.title,
                    "due_date": t.due_date.isoformat(),
                    "project_id": t.project_id
                }
                for t in upcoming_tasks[:5]  # Limit to 5 most urgent
            ]
        }
    
    def get_project_tasks_analytics(self, db: Session, project_id: int, user_id: int) -> Dict[str, Any]:
        """Get analytics for tasks in a specific project"""
        # Verify user has access to project
        if not self._user_has_project_access(db, project_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )
        
        # Get all tasks for the project
        project_tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        if not project_tasks:
            return {
                "project_id": project_id,
                "total_tasks": 0,
                "message": "No tasks found for this project"
            }
        
        # Calculate basic statistics
        total_tasks = len(project_tasks)
        completed_tasks = len([t for t in project_tasks if t.status == TaskStatus.DONE])
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate time statistics
        total_estimated_hours = sum(t.estimated_hours or 0 for t in project_tasks)
        total_actual_hours = sum(t.actual_hours or 0 for t in project_tasks)
        
        # Get team workload distribution
        assignee_workload = {}
        for task in project_tasks:
            if task.assignee_id:
                if task.assignee_id not in assignee_workload:
                    assignee_workload[task.assignee_id] = {
                        "total_tasks": 0,
                        "completed_tasks": 0,
                        "estimated_hours": 0,
                        "actual_hours": 0
                    }
                
                assignee_workload[task.assignee_id]["total_tasks"] += 1
                if task.status == TaskStatus.DONE:
                    assignee_workload[task.assignee_id]["completed_tasks"] += 1
                assignee_workload[task.assignee_id]["estimated_hours"] += task.estimated_hours or 0
                assignee_workload[task.assignee_id]["actual_hours"] += task.actual_hours or 0
        
        # Calculate velocity (tasks completed per week)
        completed_with_dates = [t for t in project_tasks if t.status == TaskStatus.DONE and t.completed_at]
        if completed_with_dates:
            # Get tasks completed in last 4 weeks
            four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
            recent_completions = [t for t in completed_with_dates if t.completed_at >= four_weeks_ago]
            velocity = len(recent_completions) / 4  # tasks per week
        else:
            velocity = 0.0
        
        return {
            "project_id": project_id,
            "total_tasks": total_tasks,
            "progress_percentage": round(progress_percentage, 1),
            "task_status_breakdown": {
                "completed": len([t for t in project_tasks if t.status == TaskStatus.DONE]),
                "in_progress": len([t for t in project_tasks if t.status == TaskStatus.IN_PROGRESS]),
                "todo": len([t for t in project_tasks if t.status == TaskStatus.TODO]),
                "cancelled": len([t for t in project_tasks if t.status == TaskStatus.CANCELLED])
            },
            "time_tracking": {
                "total_estimated_hours": total_estimated_hours,
                "total_actual_hours": total_actual_hours,
                "efficiency_percentage": round((total_estimated_hours / total_actual_hours * 100), 1) if total_actual_hours > 0 else 0
            },
            "team_workload": assignee_workload,
            "velocity": round(velocity, 1),
            "overdue_tasks": len([
                t for t in project_tasks 
                if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE
            ])
        }
    
    def _user_has_project_access(self, db: Session, project_id: int, user_id: int) -> bool:
        """Check if user has access to a project"""
        # Check if user is admin (admins have access to all projects)
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.is_admin:
            return True
        
        # Check if user is project owner
        project = db.query(Project).filter(Project.id == project_id).first()
        if project and project.owner_id == user_id:
            return True
        
        # Check if user is project member
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        return member is not None
    
    def _user_can_edit_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """Check if user can edit a task"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        # Task creator can edit
        if task.creator_id == user_id:
            return True
        
        # Task assignee can edit
        if task.assignee_id == user_id:
            return True
        
        # Project admin/manager can edit
        return self._user_can_manage_project(db, task.project_id, user_id)
    
    def _user_can_delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """Check if user can delete a task"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        # Task creator can delete
        if task.creator_id == user_id:
            return True
        
        # Project admin/manager can delete
        return self._user_can_manage_project(db, task.project_id, user_id)
    
    def _user_can_manage_project(self, db: Session, project_id: int, user_id: int) -> bool:
        """Check if user can manage a project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
        
        # Project owner can manage
        if project.owner_id == user_id:
            return True
        
        # Check if user is admin or manager
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        
        return member and member.role in ["admin", "manager"]