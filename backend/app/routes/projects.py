from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from ..database import get_db
from ..models.project import (
    Project, ProjectCreate, ProjectUpdate, ProjectResponse, ProjectSummary,
    ProjectMember, ProjectMemberCreate, ProjectMemberResponse,
    ProjectStatus, ProjectPriority
)
from ..services.auth_service import AuthService
from ..services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    return AuthService.get_current_user_from_token(db, token)

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project"""
    project_service = ProjectService()
    try:
        db_project = project_service.create_project(db, project, current_user.id)
        return db_project
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating project: {str(e)}"
        )

@router.get("/", response_model=List[ProjectSummary])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[ProjectStatus] = None,
    priority: Optional[ProjectPriority] = None,
    search: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get projects accessible to current user"""
    project_service = ProjectService()
    projects = project_service.get_projects(
        db, current_user.id, skip, limit, status, priority, search
    )
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific project"""
    project_service = ProjectService()
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a project"""
    project_service = ProjectService()
    updated_project = project_service.update_project(db, project_id, project_update, current_user.id)
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return updated_project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project"""
    project_service = ProjectService()
    success = project_service.delete_project(db, project_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return {"message": "Project deleted successfully"}

# Project Members Management
@router.get("/{project_id}/members", response_model=List[ProjectMemberResponse])
def get_project_members(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all members of a project"""
    project_service = ProjectService()
    members = project_service.get_project_members(db, project_id, current_user.id)
    return members

@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
def add_project_member(
    project_id: int,
    member_data: ProjectMemberCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a member to a project"""
    project_service = ProjectService()
    try:
        member = project_service.add_project_member(
            db, project_id, member_data.user_id, member_data.role
        )
        return member
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding member: {str(e)}"
        )

@router.put("/{project_id}/members/{user_id}", response_model=ProjectMemberResponse)
def update_member_role(
    project_id: int,
    user_id: int,
    new_role: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a project member's role"""
    if new_role not in ["admin", "manager", "member", "viewer"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    project_service = ProjectService()
    updated_member = project_service.update_member_role(
        db, project_id, user_id, new_role, current_user.id
    )
    if not updated_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return updated_member

@router.delete("/{project_id}/members/{user_id}")
def remove_project_member(
    project_id: int,
    user_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a member from a project"""
    project_service = ProjectService()
    success = project_service.remove_project_member(db, project_id, user_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return {"message": "Member removed successfully"}

# Project Analytics
@router.get("/{project_id}/analytics")
def get_project_analytics(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive project analytics"""
    project_service = ProjectService()
    analytics = project_service.get_project_analytics(db, project_id, current_user.id)
    return analytics

@router.get("/{project_id}/dashboard")
def get_project_dashboard(
    project_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project dashboard data"""
    project_service = ProjectService()
    
    # Get basic project info
    project = project_service.get_project(db, project_id, current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get analytics
    analytics = project_service.get_project_analytics(db, project_id, current_user.id)
    
    # Get members
    members = project_service.get_project_members(db, project_id, current_user.id)
    
    return {
        "project": project,
        "analytics": analytics,
        "members": members,
        "user_role": next(
            (m.role for m in members if m.user_id == current_user.id),
            "viewer"
        )
    }

# User Dashboard
@router.get("/dashboard/overview")
def get_user_dashboard(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user dashboard overview"""
    project_service = ProjectService()
    dashboard_data = project_service.get_user_dashboard_data(db, current_user.id)
    return dashboard_data

# Project Status Management
@router.put("/{project_id}/status")
def update_project_status(
    project_id: int,
    new_status: ProjectStatus,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project status"""
    project_service = ProjectService()
    
    # Create update object with just the status
    from ..models.project import ProjectUpdate
    project_update = ProjectUpdate(status=new_status)
    
    updated_project = project_service.update_project(db, project_id, project_update, current_user.id)
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {
        "message": f"Project status updated to {new_status}",
        "project": updated_project
    }

# Search and Filter
@router.get("/search/advanced")
def advanced_project_search(
    query: Optional[str] = None,
    status: Optional[List[ProjectStatus]] = Query(None),
    priority: Optional[List[ProjectPriority]] = Query(None),
    owner_id: Optional[int] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced project search with multiple filters"""
    project_service = ProjectService()
    
    # For now, use the basic search functionality
    # This could be extended to support more advanced filtering
    projects = project_service.get_projects(
        db, current_user.id, skip, limit, 
        status[0] if status else None,
        priority[0] if priority else None,
        query
    )
    
    return {
        "projects": projects,
        "total": len(projects),
        "filters_applied": {
            "query": query,
            "status": status,
            "priority": priority,
            "owner_id": owner_id
        }
    }