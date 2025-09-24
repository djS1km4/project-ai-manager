from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from ..models.project import Project, ProjectMember, ProjectCreate, ProjectUpdate, ProjectStatus, ProjectPriority
from ..models.task import Task, TaskStatus
from ..models.user import User
from ..models.ai_insight import AIInsight, ProjectAnalytics
from .ai_service import AIProjectAnalysisService
from fastapi import HTTPException, status

class ProjectService:
    def __init__(self):
        self.ai_service = AIProjectAnalysisService()
    
    def create_project(self, db: Session, project: ProjectCreate, owner_id: int) -> Project:
        """Create a new project"""
        db_project = Project(
            **project.dict(),
            owner_id=owner_id,
            status=ProjectStatus.PLANNING
        )
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Add owner as project member with admin role
        self.add_project_member(db, db_project.id, owner_id, "admin")
        
        return db_project
    
    def get_project(self, db: Session, project_id: int, user_id: int) -> Optional[Project]:
        """Get a project by ID if user has access"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        # Check if user has access to this project
        if not self.user_has_project_access(db, project_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )
        
        return project
    
    def get_projects(
        self, 
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[ProjectStatus] = None,
        priority: Optional[ProjectPriority] = None,
        search: Optional[str] = None
    ) -> List[Project]:
        """Get projects accessible to user with filtering"""
        # Get projects where user is owner or member
        query = db.query(Project).join(ProjectMember).filter(
            ProjectMember.user_id == user_id
        )
        
        # Apply filters
        if status:
            query = query.filter(Project.status == status)
        
        if priority:
            query = query.filter(Project.priority == priority)
        
        if search:
            query = query.filter(
                or_(
                    Project.name.ilike(f"%{search}%"),
                    Project.description.ilike(f"%{search}%")
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    def update_project(self, db: Session, project_id: int, project_update: ProjectUpdate, user_id: int) -> Optional[Project]:
        """Update a project"""
        project = self.get_project(db, project_id, user_id)
        if not project:
            return None
        
        # Check if user can edit this project
        if not self.user_can_edit_project(db, project_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to edit this project"
            )
        
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(project)
        return project
    
    def delete_project(self, db: Session, project_id: int, user_id: int) -> bool:
        """Delete a project"""
        project = self.get_project(db, project_id, user_id)
        if not project:
            return False
        
        # Only owner can delete project
        if project.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only project owner can delete the project"
            )
        
        db.delete(project)
        db.commit()
        return True
    
    def add_project_member(self, db: Session, project_id: int, user_id: int, role: str = "member") -> ProjectMember:
        """Add a member to a project"""
        # Check if user is already a member
        existing_member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this project"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        member = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role=role
        )
        
        db.add(member)
        db.commit()
        db.refresh(member)
        return member
    
    def remove_project_member(self, db: Session, project_id: int, user_id: int, requester_id: int) -> bool:
        """Remove a member from a project"""
        # Check if requester can manage members
        if not self.user_can_manage_members(db, project_id, requester_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to manage project members"
            )
        
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        
        if not member:
            return False
        
        # Cannot remove project owner
        project = db.query(Project).filter(Project.id == project_id).first()
        if project and project.owner_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove project owner from project"
            )
        
        db.delete(member)
        db.commit()
        return True
    
    def update_member_role(self, db: Session, project_id: int, user_id: int, new_role: str, requester_id: int) -> Optional[ProjectMember]:
        """Update a project member's role"""
        # Check if requester can manage members
        if not self.user_can_manage_members(db, project_id, requester_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to manage project members"
            )
        
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        
        if not member:
            return None
        
        member.role = new_role
        db.commit()
        db.refresh(member)
        return member
    
    def get_project_members(self, db: Session, project_id: int, user_id: int) -> List[ProjectMember]:
        """Get all members of a project"""
        # Check if user has access to this project
        if not self.user_has_project_access(db, project_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )
        
        return db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
    
    def get_project_analytics(self, db: Session, project_id: int, user_id: int) -> Dict[str, Any]:
        """Get comprehensive project analytics"""
        project = self.get_project(db, project_id, user_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Get basic project statistics
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        in_progress_tasks = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
        todo_tasks = len([t for t in tasks if t.status == TaskStatus.TODO])
        overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE])
        
        progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Get team statistics
        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
        team_size = len(members)
        
        # Calculate estimated vs actual hours
        total_estimated_hours = sum(t.estimated_hours or 0 for t in tasks)
        total_actual_hours = sum(t.actual_hours or 0 for t in tasks)
        
        # Get AI insights
        try:
            ai_insights = self.ai_service.generate_ai_insights(project_id, db)
        except Exception:
            ai_insights = []
        
        # Calculate budget utilization
        budget_utilization = 0.0
        if project.budget and project.budget > 0:
            hourly_rate = 75  # Default rate
            current_cost = total_actual_hours * hourly_rate
            budget_utilization = (current_cost / project.budget) * 100
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "status": project.status,
            "priority": project.priority,
            "progress_percentage": round(progress_percentage, 1),
            "task_statistics": {
                "total": total_tasks,
                "completed": completed_tasks,
                "in_progress": in_progress_tasks,
                "todo": todo_tasks,
                "overdue": overdue_tasks
            },
            "team_statistics": {
                "team_size": team_size,
                "members": [{"user_id": m.user_id, "role": m.role} for m in members]
            },
            "time_tracking": {
                "estimated_hours": total_estimated_hours,
                "actual_hours": total_actual_hours,
                "efficiency": round((total_estimated_hours / total_actual_hours * 100), 1) if total_actual_hours > 0 else 0
            },
            "budget": {
                "allocated": project.budget or 0,
                "utilization_percentage": round(budget_utilization, 1)
            },
            "timeline": {
                "start_date": project.start_date.isoformat() if project.start_date else None,
                "end_date": project.end_date.isoformat() if project.end_date else None,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat()
            },
            "ai_insights": ai_insights
        }
    
    def user_has_project_access(self, db: Session, project_id: int, user_id: int) -> bool:
        """Check if user has access to a project"""
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        return member is not None
    
    def user_can_edit_project(self, db: Session, project_id: int, user_id: int) -> bool:
        """Check if user can edit a project"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
        
        # Owner can always edit
        if project.owner_id == user_id:
            return True
        
        # Check if user is admin or manager
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        
        return member and member.role in ["admin", "manager"]
    
    def user_can_manage_members(self, db: Session, project_id: int, user_id: int) -> bool:
        """Check if user can manage project members"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
        
        # Owner can always manage members
        if project.owner_id == user_id:
            return True
        
        # Check if user is admin
        member = db.query(ProjectMember).filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        ).first()
        
        return member and member.role == "admin"
    
    def get_user_dashboard_data(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Get dashboard data for a user"""
        # Get user's projects
        user_projects = self.get_projects(db, user_id, limit=1000)
        
        # Calculate statistics
        total_projects = len(user_projects)
        active_projects = len([p for p in user_projects if p.status in [ProjectStatus.ACTIVE, ProjectStatus.IN_PROGRESS]])
        completed_projects = len([p for p in user_projects if p.status == ProjectStatus.COMPLETED])
        
        # Get tasks assigned to user across all projects
        user_tasks = db.query(Task).filter(Task.assignee_id == user_id).all()
        
        total_tasks = len(user_tasks)
        completed_tasks = len([t for t in user_tasks if t.status == TaskStatus.DONE])
        overdue_tasks = len([t for t in user_tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != TaskStatus.DONE])
        
        # Get recent activity (tasks updated in last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = [t for t in user_tasks if t.updated_at >= week_ago]
        
        # Get upcoming deadlines (next 7 days)
        next_week = datetime.utcnow() + timedelta(days=7)
        upcoming_deadlines = [
            t for t in user_tasks 
            if t.due_date and datetime.utcnow() <= t.due_date <= next_week and t.status != TaskStatus.DONE
        ]
        
        return {
            "user_id": user_id,
            "project_statistics": {
                "total": total_projects,
                "active": active_projects,
                "completed": completed_projects
            },
            "task_statistics": {
                "total": total_tasks,
                "completed": completed_tasks,
                "overdue": overdue_tasks,
                "completion_rate": round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
            },
            "recent_activity": {
                "tasks_updated_this_week": len(recent_tasks),
                "upcoming_deadlines": len(upcoming_deadlines)
            },
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "status": p.status,
                    "priority": p.priority,
                    "progress": self._calculate_project_progress(db, p.id)
                }
                for p in user_projects[:10]  # Limit to 10 most recent
            ]
        }
    
    def _calculate_project_progress(self, db: Session, project_id: int) -> float:
        """Calculate project progress percentage"""
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        if not tasks:
            return 0.0
        
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        return round((completed_tasks / len(tasks) * 100), 1)