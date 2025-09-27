#!/usr/bin/env python3
"""
Script para asignar proyectos huérfanos a usuarios existentes de forma aleatoria.
"""

import random
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.project import Project
from app.models.user import User
from app.services.project_service import ProjectService

def assign_orphan_projects():
    """Asignar proyectos huérfanos a usuarios existentes aleatoriamente"""
    db = SessionLocal()
    project_service = ProjectService()
    
    try:
        # Obtener todos los usuarios válidos
        valid_users = db.query(User).all()
        valid_user_ids = [user.id for user in valid_users]
        
        print(f"👥 Usuarios válidos encontrados: {len(valid_users)}")
        for user in valid_users:
            print(f"   - {user.username} (ID: {user.id})")
        print()
        
        # Obtener proyectos huérfanos (con owner_id inválido)
        all_projects = db.query(Project).all()
        orphan_projects = [p for p in all_projects if p.owner_id not in valid_user_ids]
        
        print(f"🚫 Proyectos huérfanos encontrados: {len(orphan_projects)}")
        
        if not orphan_projects:
            print("✅ No hay proyectos huérfanos para asignar.")
            return
        
        # Asignar proyectos aleatoriamente
        assigned_count = 0
        for project in orphan_projects:
            # Seleccionar un usuario aleatorio
            new_owner = random.choice(valid_users)
            old_owner_id = project.owner_id
            
            # Actualizar el propietario del proyecto
            project.owner_id = new_owner.id
            
            # Agregar al nuevo propietario como miembro admin del proyecto
            try:
                project_service.add_project_member(db, project.id, new_owner.id, "admin")
                print(f"📁 '{project.name}' asignado a {new_owner.username} (ID: {old_owner_id} → {new_owner.id})")
                assigned_count += 1
            except Exception as e:
                # Si ya es miembro, solo actualizar el propietario
                if "already a member" in str(e).lower():
                    print(f"📁 '{project.name}' asignado a {new_owner.username} (ya era miembro)")
                    assigned_count += 1
                else:
                    print(f"❌ Error asignando '{project.name}': {e}")
        
        # Confirmar cambios
        db.commit()
        
        print(f"\n✅ RESUMEN:")
        print(f"   Proyectos asignados: {assigned_count}")
        print(f"   Total de proyectos: {len(all_projects)}")
        
        # Verificar distribución final
        print(f"\n📊 DISTRIBUCIÓN FINAL:")
        for user in valid_users:
            project_count = db.query(Project).filter(Project.owner_id == user.id).count()
            print(f"   {user.username}: {project_count} proyectos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    assign_orphan_projects()