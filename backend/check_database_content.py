#!/usr/bin/env python3
"""
Script para verificar el contenido de la base de datos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

def check_database_content():
    """Verificar el contenido actual de la base de datos"""
    db = SessionLocal()
    try:
        # Contar usuarios
        user_count = db.query(User).count()
        print(f"👥 Total de usuarios: {user_count}")
        
        # Listar usuarios
        users = db.query(User).all()
        for user in users:
            print(f"  - {user.username} ({user.email}) - Admin: {user.is_admin}")
        
        # Contar proyectos
        project_count = db.query(Project).count()
        print(f"\n📁 Total de proyectos: {project_count}")
        
        # Listar algunos proyectos
        projects = db.query(Project).limit(10).all()
        for project in projects:
            print(f"  - {project.name} (Estado: {project.status}) - Owner: {project.owner_id}")
        
        # Contar tareas
        task_count = db.query(Task).count()
        print(f"\n✅ Total de tareas: {task_count}")
        
        # Listar algunas tareas
        tasks = db.query(Task).limit(10).all()
        for task in tasks:
            print(f"  - {task.title} (Estado: {task.status}) - Proyecto: {task.project_id}")
        
        print(f"\n📊 Resumen:")
        print(f"  - Usuarios: {user_count}")
        print(f"  - Proyectos: {project_count}")
        print(f"  - Tareas: {task_count}")
        
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database_content()