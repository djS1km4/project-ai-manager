#!/usr/bin/env python3
"""
Script para verificar campos NULL en la base de datos que podrían causar problemas de serialización
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.task import Task
from app.models.project import Project, ProjectMember
from sqlalchemy import text

def check_null_fields():
    """Verificar campos NULL que podrían causar problemas"""
    db = next(get_db())
    
    print("🔍 Verificando campos NULL en la base de datos...")
    print("=" * 60)
    
    # Verificar tareas con creator_id NULL
    tasks_null_creator = db.query(Task).filter(Task.creator_id.is_(None)).count()
    print(f"📋 Tareas con creator_id NULL: {tasks_null_creator}")
    
    # Verificar tareas con assignee_id NULL
    tasks_null_assignee = db.query(Task).filter(Task.assignee_id.is_(None)).count()
    print(f"📋 Tareas con assignee_id NULL: {tasks_null_assignee}")
    
    # Verificar proyectos con owner_id NULL
    projects_null_owner = db.query(Project).filter(Project.owner_id.is_(None)).count()
    print(f"📁 Proyectos con owner_id NULL: {projects_null_owner}")
    
    # Verificar miembros de proyecto con user_id NULL
    members_null_user = db.query(ProjectMember).filter(ProjectMember.user_id.is_(None)).count()
    print(f"👥 Miembros de proyecto con user_id NULL: {members_null_user}")
    
    print("=" * 60)
    
    # Si hay proyectos con owner_id NULL, mostrar algunos ejemplos
    if projects_null_owner > 0:
        print("⚠️  Proyectos con owner_id NULL encontrados:")
        null_projects = db.query(Project).filter(Project.owner_id.is_(None)).limit(5).all()
        for project in null_projects:
            print(f"   - ID: {project.id}, Nombre: {project.name}")
    
    db.close()

if __name__ == "__main__":
    check_null_fields()