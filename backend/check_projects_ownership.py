#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.project import Project
from app.models.user import User
from app.models.task import Task

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def check_projects_ownership():
    """Check projects and their ownership"""
    
    print("🔍 Checking projects and ownership...")
    
    # Get all users
    users = db.query(User).all()
    print(f"\n👥 Users in database:")
    for user in users:
        print(f"  ID: {user.id}, Email: {user.email}, Name: {user.full_name}")
    
    # Get all projects
    projects = db.query(Project).all()
    print(f"\n📁 Projects in database:")
    for project in projects:
        owner = db.query(User).filter(User.id == project.owner_id).first()
        owner_name = owner.full_name if owner else "Unknown"
        print(f"  ID: {project.id}, Name: {project.name}, Owner: {owner_name} (ID: {project.owner_id}), Status: {project.status}")
        
        # Get tasks for this project
        tasks = db.query(Task).filter(Task.project_id == project.id).all()
        print(f"    Tasks: {len(tasks)} total")
        if tasks:
            completed_tasks = len([t for t in tasks if t.status == 'done'])
            print(f"    Completed: {completed_tasks}")
            for task in tasks[:3]:  # Show first 3 tasks
                print(f"      - {task.title} (Status: {task.status})")
    
    # Check admin user specifically
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if admin_user:
        print(f"\n🔑 Admin user found: ID {admin_user.id}")
        admin_projects = db.query(Project).filter(Project.owner_id == admin_user.id).all()
        print(f"Admin owns {len(admin_projects)} projects:")
        for project in admin_projects:
            print(f"  - {project.name} (Status: {project.status})")
    else:
        print("\n❌ Admin user not found!")
    
    db.close()

if __name__ == "__main__":
    check_projects_ownership()