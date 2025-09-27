#!/usr/bin/env python3
"""
Script to check project data for AI insights generation
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.models.project import Project
from app.models.task import Task
from app.models.user import User

def check_project_data():
    print("🔍 Checking project data for AI insights...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        # Get project 3
        project = db.query(Project).filter(Project.id == 3).first()
        if not project:
            print("❌ Project 3 not found")
            return
            
        print(f"📋 Project: {project.name}")
        print(f"   Status: {project.status}")
        print(f"   Start Date: {project.start_date}")
        print(f"   End Date: {project.end_date}")
        print(f"   Budget: {project.budget}")
        print(f"   Description: {project.description}")
        
        # Get tasks for this project
        tasks = db.query(Task).filter(Task.project_id == 3).all()
        print(f"\n📝 Tasks: {len(tasks)} found")
        
        if tasks:
            completed_tasks = [t for t in tasks if t.status == 'completed']
            in_progress_tasks = [t for t in tasks if t.status == 'in_progress']
            pending_tasks = [t for t in tasks if t.status == 'pending']
            overdue_tasks = [t for t in tasks if t.due_date and t.due_date < datetime.now() and t.status != 'completed']
            
            print(f"   ✅ Completed: {len(completed_tasks)}")
            print(f"   🔄 In Progress: {len(in_progress_tasks)}")
            print(f"   ⏳ Pending: {len(pending_tasks)}")
            print(f"   ⚠️ Overdue: {len(overdue_tasks)}")
            
            print("\n📋 Task details:")
            for task in tasks[:5]:  # Show first 5 tasks
                print(f"   - {task.title} ({task.status})")
                if task.assigned_to:
                    user = db.query(User).filter(User.id == task.assigned_to).first()
                    print(f"     Assigned to: {user.username if user else 'Unknown'}")
                print(f"     Due: {task.due_date}")
                print(f"     Priority: {task.priority}")
        else:
            print("   ⚠️ No tasks found for this project")
            
        # Check users
        users = db.query(User).all()
        print(f"\n👥 Users: {len(users)} found")
        for user in users:
            print(f"   - {user.username} ({user.email})")
            
    except Exception as e:
        print(f"❌ Error checking project data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    from datetime import datetime
    check_project_data()