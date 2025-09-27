#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.project import Project, ProjectStatus
from app.models.user import User
from app.models.task import Task, TaskStatus

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def debug_dashboard_logic():
    """Debug the dashboard logic step by step"""
    
    print("🔍 Debugging dashboard logic...")
    
    # Get admin user
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        print("❌ Admin user not found!")
        return
    
    print(f"✅ Admin user found: ID {admin_user.id}")
    
    # Get user's projects (same logic as dashboard)
    user_projects = db.query(Project).filter(Project.owner_id == admin_user.id).all()
    print(f"📁 User projects found: {len(user_projects)}")
    
    for project in user_projects:
        print(f"  - Project: {project.name}")
        print(f"    Status: {project.status} (type: {type(project.status)})")
        print(f"    Budget: {project.budget}")
        
        # Check status comparisons
        print(f"    Status == ProjectStatus.ACTIVE: {project.status == ProjectStatus.ACTIVE}")
        print(f"    Status == ProjectStatus.COMPLETED: {project.status == ProjectStatus.COMPLETED}")
        print(f"    Status == ProjectStatus.PLANNING: {project.status == ProjectStatus.PLANNING}")
        print(f"    Status == ProjectStatus.ON_HOLD: {project.status == ProjectStatus.ON_HOLD}")
        print(f"    Status == ProjectStatus.CANCELLED: {project.status == ProjectStatus.CANCELLED}")
    
    # Calculate statistics manually
    total_projects = len(user_projects)
    active_projects = len([p for p in user_projects if p.status == ProjectStatus.ACTIVE])
    completed_projects = len([p for p in user_projects if p.status == ProjectStatus.COMPLETED])
    planning_projects = len([p for p in user_projects if p.status == ProjectStatus.PLANNING])
    on_hold_projects = len([p for p in user_projects if p.status == ProjectStatus.ON_HOLD])
    cancelled_projects = len([p for p in user_projects if p.status == ProjectStatus.CANCELLED])
    
    print(f"\n📊 Manual Statistics:")
    print(f"  Total Projects: {total_projects}")
    print(f"  Active Projects: {active_projects}")
    print(f"  Completed Projects: {completed_projects}")
    print(f"  Planning Projects: {planning_projects}")
    print(f"  On Hold Projects: {on_hold_projects}")
    print(f"  Cancelled Projects: {cancelled_projects}")
    
    # Get tasks
    project_ids = [p.id for p in user_projects]
    if project_ids:
        user_tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()
    else:
        user_tasks = []
    
    print(f"\n📋 Tasks found: {len(user_tasks)}")
    
    for task in user_tasks[:5]:  # Show first 5 tasks
        print(f"  - Task: {task.title}")
        print(f"    Status: {task.status} (type: {type(task.status)})")
        print(f"    Project ID: {task.project_id}")
    
    # Calculate task statistics
    total_tasks = len(user_tasks)
    completed_tasks = len([t for t in user_tasks if t.status == TaskStatus.DONE])
    pending_tasks = len([t for t in user_tasks if t.status in [TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.IN_REVIEW]])
    
    print(f"\n📈 Task Statistics:")
    print(f"  Total Tasks: {total_tasks}")
    print(f"  Completed Tasks: {completed_tasks}")
    print(f"  Pending Tasks: {pending_tasks}")
    
    # Budget calculations
    total_budget = sum([p.budget or 0 for p in user_projects])
    print(f"\n💰 Budget:")
    print(f"  Total Budget: ${total_budget}")
    
    db.close()

if __name__ == "__main__":
    debug_dashboard_logic()