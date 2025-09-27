#!/usr/bin/env python3
"""
Script para agregar al usuario regular como miembro de los proyectos
donde tiene tareas asignadas.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.task import Task
from sqlalchemy.orm import Session

def fix_project_membership():
    print("🔧 Corrigiendo membresías de proyecto para usuario regular...")
    
    db = next(get_db())
    
    try:
        # Obtener usuario regular
        regular_user = db.query(User).filter(User.email == "usuario@example.com").first()
        if not regular_user:
            print("❌ Usuario regular no encontrado")
            return
        
        print(f"✅ Usuario regular encontrado: ID {regular_user.id}")
        
        # Obtener proyectos donde el usuario tiene tareas asignadas
        projects_with_tasks = db.query(Project).join(Task).filter(
            Task.assignee_id == regular_user.id
        ).distinct().all()
        
        print(f"📋 Proyectos donde el usuario tiene tareas: {len(projects_with_tasks)}")
        
        # Verificar membresías existentes
        existing_memberships = db.query(ProjectMember).filter(
            ProjectMember.user_id == regular_user.id
        ).all()
        
        existing_project_ids = {m.project_id for m in existing_memberships}
        print(f"🔗 Membresías existentes: {len(existing_memberships)} proyectos")
        
        # Agregar membresías faltantes
        added_count = 0
        for project in projects_with_tasks:
            if project.id not in existing_project_ids:
                # Agregar como miembro del proyecto
                membership = ProjectMember(
                    user_id=regular_user.id,
                    project_id=project.id,
                    role="member"  # Rol básico de miembro
                )
                db.add(membership)
                added_count += 1
                print(f"   ➕ Agregado como miembro del proyecto: {project.name}")
        
        if added_count > 0:
            db.commit()
            print(f"✅ Se agregaron {added_count} nuevas membresías")
        else:
            print("ℹ️ No se necesitaron nuevas membresías")
        
        # Verificar también proyectos donde es owner
        owned_projects = db.query(Project).filter(
            Project.owner_id == regular_user.id
        ).all()
        
        print(f"👑 Proyectos donde es owner: {len(owned_projects)}")
        
        # Agregar membresías para proyectos propios si no existen
        for project in owned_projects:
            if project.id not in existing_project_ids:
                membership = ProjectMember(
                    user_id=regular_user.id,
                    project_id=project.id,
                    role="owner"
                )
                db.add(membership)
                added_count += 1
                print(f"   👑 Agregado como owner del proyecto: {project.name}")
        
        if added_count > 0:
            db.commit()
            print(f"✅ Total de membresías agregadas: {added_count}")
        
        # Verificación final
        print("\n🔍 Verificación final:")
        final_memberships = db.query(ProjectMember).filter(
            ProjectMember.user_id == regular_user.id
        ).all()
        
        print(f"   Total membresías: {len(final_memberships)}")
        
        # Verificar tareas accesibles
        accessible_tasks = db.query(Task).join(Project).join(ProjectMember).filter(
            ProjectMember.user_id == regular_user.id
        ).all()
        
        print(f"   Tareas accesibles: {len(accessible_tasks)}")
        
        # Verificar tareas asignadas específicamente al usuario
        assigned_tasks = db.query(Task).filter(
            Task.assignee_id == regular_user.id
        ).all()
        
        print(f"   Tareas asignadas: {len(assigned_tasks)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_project_membership()