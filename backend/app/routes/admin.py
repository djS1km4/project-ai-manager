from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import UserListResponse, UserAdminUpdate
from ..models.project import Project, ProjectMember
from ..models.task import Task
from ..services.auth_service import AuthService
from ..services.project_service import ProjectService
from ..services.task_service import TaskService
from ..dependencies import get_current_admin_user, get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserListResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Get all users (admin only)"""
    users = AuthService.get_all_users(db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}", response_model=UserListResponse)
async def update_user(
    user_id: int,
    user_update: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Update user information (admin only)"""
    
    # Prevent admin from deactivating themselves
    if user_id == current_user.id and user_update.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    updated_user = AuthService.admin_update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user

@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Activate a user account (admin only)"""
    
    success = AuthService.activate_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User activated successfully"}

@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Deactivate a user account (admin only)"""
    
    # Prevent admin from deactivating themselves
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    success = AuthService.deactivate_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}

@router.post("/users/{user_id}/make-admin")
async def make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Grant admin privileges to a user (admin only)"""
    
    updated_user = AuthService.change_user_role(db, user_id, "admin")
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User {updated_user.full_name} is now an admin"}

@router.post("/users/{user_id}/remove-admin")
async def remove_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Remove admin privileges from a user (admin only)"""
    
    # Prevent admin from removing their own admin privileges
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove admin privileges from your own account"
        )
    
    updated_user = AuthService.change_user_role(db, user_id, "user")
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"Admin privileges removed from {updated_user.full_name}"}

# Project Management Endpoints
@router.get("/projects")
async def get_all_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Get all projects (admin only)"""
    project_service = ProjectService()
    projects = project_service.get_projects(db, current_user.id, skip=skip, limit=limit)
    return projects

@router.post("/projects/{project_id}/assign-user/{user_id}")
async def assign_project_to_user(
    project_id: int,
    user_id: int,
    role: str = "member",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Assign a project to a user (admin only)"""
    
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Verify user exists
    from ..models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        project_service = ProjectService()
        project_service.add_project_member(db, project_id, user_id, role)
        return {"message": f"User assigned to project successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/projects/{project_id}/unassign-user/{user_id}")
async def unassign_project_from_user(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Unassign a project from a user (admin only)"""
    
    # Find and remove project member
    project_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    
    if not project_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not assigned to this project"
        )
    
    db.delete(project_member)
    db.commit()
    
    return {"message": "User unassigned from project successfully"}

@router.post("/projects/{project_id}/change-owner/{new_owner_id}")
async def change_project_owner(
    project_id: int,
    new_owner_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Change project owner (admin only)"""
    
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Verify new owner exists
    from ..models.user import User
    new_owner = db.query(User).filter(User.id == new_owner_id).first()
    if not new_owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="New owner not found"
        )
    
    # Update project owner
    project.owner_id = new_owner_id
    db.commit()
    
    # Ensure new owner is a project member with admin role
    project_service = ProjectService()
    try:
        project_service.add_project_member(db, project_id, new_owner_id, "admin")
    except:
        # User might already be a member, update their role
        member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == new_owner_id
        ).first()
        if member:
            member.role = "admin"
            db.commit()
    
    return {"message": f"Project ownership transferred to {new_owner.full_name}"}

# Task Management Endpoints
@router.get("/tasks")
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Get all tasks (admin only)"""
    task_service = TaskService()
    tasks = task_service.get_tasks(db, current_user.id, skip=skip, limit=limit)
    return tasks

@router.post("/tasks/{task_id}/assign-user/{user_id}")
async def assign_task_to_user(
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Assign a task to a user (admin only)"""
    
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify user exists
    from ..models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update task assignee
    task.assignee_id = user_id
    db.commit()
    
    return {"message": f"Task assigned to {user.full_name} successfully"}

@router.delete("/tasks/{task_id}/unassign")
async def unassign_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """Unassign a task (admin only)"""
    
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Remove assignee
    task.assignee_id = None
    db.commit()
    
    return {"message": "Task unassigned successfully"}