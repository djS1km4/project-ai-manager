#!/usr/bin/env python3
"""
Script to completely reset the database and recreate it with fresh data
"""
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.database import get_db, engine, Base
from app.models.user import User
from app.models.project import Project, ProjectMember, ProjectStatus, ProjectPriority
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.ai_insight import AIInsight
from app.services.auth_service import AuthService
from sqlalchemy.orm import sessionmaker

def reset_database():
    """Reset the entire database"""
    print("🗑️  Resetting database...")
    
    try:
        # Drop all tables
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        
        # Recreate all tables
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database reset successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False

def create_test_users():
    """Create test users"""
    print("👥 Creating test users...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Test user 1
        test_user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password=AuthService.get_password_hash("testpassword123"),
            is_active=True,
            is_admin=True
        )
        db.add(test_user)
        
        # Test user 2
        admin_user = User(
            email="admin@example.com",
            username="admin",
            full_name="Administrator",
            hashed_password=AuthService.get_password_hash("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        
        # Regular user
        regular_user = User(
            email="user@example.com",
            username="user",
            full_name="Regular User",
            hashed_password=AuthService.get_password_hash("user123"),
            is_active=True,
            is_admin=False
        )
        db.add(regular_user)
        
        db.commit()
        print("✅ Test users created successfully!")
        
        # Show created users
        users = db.query(User).all()
        for user in users:
            print(f"  - {user.email} (ID: {user.id}, Admin: {user.is_admin})")
            
    except Exception as e:
        print(f"❌ Error creating test users: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_data():
    """Create some sample projects and tasks"""
    print("📊 Creating sample data...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get the first user
        user = db.query(User).first()
        if not user:
            print("❌ No users found to create sample data")
            return
        
        # Create sample project
        sample_project = Project(
            name="Proyecto de Ejemplo",
            description="Este es un proyecto de ejemplo para probar la funcionalidad",
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.MEDIUM,
            owner_id=user.id
        )
        db.add(sample_project)
        db.commit()
        
        # Create sample task
        sample_task = Task(
            title="Tarea de Ejemplo",
            description="Esta es una tarea de ejemplo",
            status=TaskStatus.TODO,
            priority=TaskPriority.MEDIUM,
            project_id=sample_project.id,
            assignee_id=user.id,
            creator_id=user.id
        )
        db.add(sample_task)
        db.commit()
        
        print("✅ Sample data created successfully!")
        print(f"  - Project: {sample_project.name} (ID: {sample_project.id})")
        print(f"  - Task: {sample_task.title} (ID: {sample_task.id})")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function"""
    print("🔄 Starting database reset process...")
    print("=" * 50)
    
    # Reset database
    if not reset_database():
        print("❌ Failed to reset database. Exiting.")
        return
    
    # Create test users
    create_test_users()
    
    # Create sample data
    create_sample_data()
    
    print("=" * 50)
    print("✅ Database reset completed successfully!")
    print("\n📋 Available test accounts:")
    print("  1. test@example.com / testpassword123 (Admin)")
    print("  2. admin@example.com / admin123 (Admin)")
    print("  3. user@example.com / user123 (Regular user)")

if __name__ == "__main__":
    main()