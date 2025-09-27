#!/usr/bin/env python3
"""
Script para agregar los registros de ProjectMember faltantes.
Cada propietario de proyecto debe ser miembro de su propio proyecto.
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.project import Project, ProjectMember

def fix_project_members():
    """Agregar registros de ProjectMember para todos los propietarios de proyectos"""
    db = SessionLocal()
    
    try:
        # Obtener todos los proyectos
        projects = db.query(Project).all()
        print(f"Encontrados {len(projects)} proyectos")
        
        members_added = 0
        
        for project in projects:
            # Verificar si el propietario ya es miembro
            existing_member = db.query(ProjectMember).filter(
                ProjectMember.project_id == project.id,
                ProjectMember.user_id == project.owner_id
            ).first()
            
            if not existing_member:
                # Crear registro de miembro para el propietario
                project_member = ProjectMember(
                    project_id=project.id,
                    user_id=project.owner_id,
                    role="admin"
                )
                db.add(project_member)
                members_added += 1
                print(f"Agregado propietario como miembro: Proyecto {project.id} - Usuario {project.owner_id}")
        
        # Confirmar cambios
        db.commit()
        print(f"\n✅ Se agregaron {members_added} registros de ProjectMember")
        
        # Verificar el resultado
        total_members = db.query(ProjectMember).count()
        print(f"Total de miembros de proyecto ahora: {total_members}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_project_members()