from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Dict, Any

from ..database import get_db
from ..models.user import User
from ..models.project import Project, ProjectStatus
from ..models.task import Task, TaskStatus
from ..services.auth_service import AuthService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    return AuthService.get_current_user_from_token(db, token)

@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    try:
        # Get user's projects
        user_projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
        project_ids = [p.id for p in user_projects]
        
        # Total projects
        total_projects = len(user_projects)
        
        # Active projects (active status)
        active_projects = len([p for p in user_projects if p.status == ProjectStatus.ACTIVE])
        
        # Completed projects
        completed_projects = len([p for p in user_projects if p.status == ProjectStatus.COMPLETED])
        
        # Planning projects
        planning_projects = len([p for p in user_projects if p.status == ProjectStatus.PLANNING])
        
        # On hold projects
        on_hold_projects = len([p for p in user_projects if p.status == ProjectStatus.ON_HOLD])
        
        # Get user's tasks
        if project_ids:
            user_tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()
        else:
            user_tasks = []
        
        # Total tasks
        total_tasks = len(user_tasks)
        
        # Completed tasks
        completed_tasks = len([t for t in user_tasks if t.status == TaskStatus.DONE])
        
        # Pending tasks
        pending_tasks = len([t for t in user_tasks if t.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.IN_REVIEW]])
        
        # Overdue tasks
        today = datetime.utcnow()
        overdue_tasks = len([
            t for t in user_tasks 
            if t.due_date and t.due_date < today and t.status != TaskStatus.DONE
        ])
        
        # Budget calculations
        total_budget = sum([p.budget or 0 for p in user_projects])
        
        # Calculate used budget based on project progress
        used_budget = 0
        for project in user_projects:
            if project.budget:
                project_tasks = [t for t in user_tasks if t.project_id == project.id]
                if project_tasks:
                    completed_project_tasks = len([t for t in project_tasks if t.status == TaskStatus.DONE])
                    total_project_tasks = len(project_tasks)
                    progress_ratio = completed_project_tasks / total_project_tasks
                    used_budget += project.budget * progress_ratio
                elif project.status == ProjectStatus.COMPLETED:
                    used_budget += project.budget
                elif project.status == ProjectStatus.ACTIVE:
                    used_budget += project.budget * 0.3  # Assume 30% for active projects without tasks
        
        return {
            "totalProjects": total_projects,
            "activeProjects": active_projects,
            "completedProjects": completed_projects,
            "planningProjects": planning_projects,
            "onHoldProjects": on_hold_projects,
            "totalTasks": total_tasks,
            "completedTasks": completed_tasks,
            "pendingTasks": pending_tasks,
            "overdueTasks": overdue_tasks,
            "totalBudget": total_budget,
            "usedBudget": used_budget
        }
    except Exception as e:
        # Log the error and raise it instead of hiding it
        print(f"Dashboard stats error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting dashboard stats: {str(e)}"
        )