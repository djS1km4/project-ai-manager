#!/usr/bin/env python3
"""
Script to create test tasks for AI insights generation
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.user import User
from datetime import datetime, timedelta
import random

def create_test_tasks():
    print("🔧 Creating test tasks for AI insights...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        # Get some users to assign tasks
        users = db.query(User).limit(5).all()
        if not users:
            print("❌ No users found")
            return
            
        project_id = 3
        
        # Create various tasks with different statuses
        tasks_data = [
            {
                "title": "Diseñar interfaz de usuario",
                "description": "Crear mockups y diseños para la interfaz principal",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "due_date": datetime.now() - timedelta(days=5),
                "estimated_hours": 16
            },
            {
                "title": "Implementar autenticación",
                "description": "Desarrollar sistema de login y registro",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "due_date": datetime.now() - timedelta(days=3),
                "estimated_hours": 24
            },
            {
                "title": "Crear dashboard principal",
                "description": "Implementar dashboard con métricas y gráficos",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.MEDIUM,
                "due_date": datetime.now() + timedelta(days=7),
                "estimated_hours": 32
            },
            {
                "title": "Integrar API de pagos",
                "description": "Conectar con pasarela de pagos externa",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "due_date": datetime.now() + timedelta(days=10),
                "estimated_hours": 20
            },
            {
                "title": "Optimizar rendimiento",
                "description": "Mejorar velocidad de carga y respuesta",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "due_date": datetime.now() + timedelta(days=14),
                "estimated_hours": 16
            },
            {
                "title": "Implementar notificaciones",
                "description": "Sistema de notificaciones push y email",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "due_date": datetime.now() + timedelta(days=21),
                "estimated_hours": 12
            },
            {
                "title": "Configurar CI/CD",
                "description": "Pipeline de integración y despliegue continuo",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.HIGH,
                "due_date": datetime.now() - timedelta(days=2),
                "estimated_hours": 8
            },
            {
                "title": "Escribir documentación",
                "description": "Documentación técnica y de usuario",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "due_date": datetime.now() + timedelta(days=30),
                "estimated_hours": 20
            }
        ]
        
        created_tasks = []
        for i, task_data in enumerate(tasks_data):
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                status=task_data["status"],
                priority=task_data["priority"],
                project_id=project_id,
                assignee_id=users[i % len(users)].id,
                creator_id=users[0].id,  # Use first user as creator
                due_date=task_data["due_date"],
                estimated_hours=task_data["estimated_hours"],
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            
            # Set completion date for completed tasks
            if task.status == TaskStatus.DONE:
                task.completed_at = task.due_date + timedelta(days=random.randint(-2, 1))
            
            db.add(task)
            created_tasks.append(task)
        
        db.commit()
        
        print(f"✅ Created {len(created_tasks)} test tasks")
        for task in created_tasks:
            print(f"   - {task.title} ({task.status.value})")
            
    except Exception as e:
        print(f"❌ Error creating tasks: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_tasks()