#!/usr/bin/env python3
"""
Script para verificar proyectos huérfanos (sin propietario válido).
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models.project import Project
from app.models.user import User

def check_orphan_projects():
    """Verificar proyectos sin propietario válido"""
    db = SessionLocal()
    
    try:
        # Obtener todos los proyectos
        all_projects = db.query(Project).all()
        print(f"📊 Total de proyectos en BD: {len(all_projects)}")
        
        # Obtener todos los IDs de usuarios válidos
        valid_user_ids = [user.id for user in db.query(User).all()]
        print(f"👥 IDs de usuarios válidos: {valid_user_ids}")
        print()
        
        # Verificar proyectos huérfanos
        orphan_projects = []
        valid_projects = []
        
        for project in all_projects:
            if project.owner_id not in valid_user_ids:
                orphan_projects.append(project)
            else:
                valid_projects.append(project)
        
        print(f"📁 PROYECTOS VÁLIDOS: {len(valid_projects)}")
        print(f"🚫 PROYECTOS HUÉRFANOS: {len(orphan_projects)}")
        print()
        
        if orphan_projects:
            print("🚫 PROYECTOS HUÉRFANOS (sin propietario válido):")
            print("-" * 60)
            
            # Agrupar por owner_id inválido
            invalid_owners = {}
            for project in orphan_projects:
                if project.owner_id not in invalid_owners:
                    invalid_owners[project.owner_id] = []
                invalid_owners[project.owner_id].append(project)
            
            for owner_id, projects in invalid_owners.items():
                print(f"👤 Owner ID inválido: {owner_id} ({len(projects)} proyectos)")
                for project in projects[:3]:  # Mostrar solo los primeros 3
                    print(f"   📁 {project.name}")
                if len(projects) > 3:
                    print(f"   ... y {len(projects) - 3} más")
                print()
        
        # Verificar si hay proyectos con owner_id NULL
        null_owner_count = db.execute(text("SELECT COUNT(*) FROM projects WHERE owner_id IS NULL")).scalar()
        print(f"🔍 Proyectos con owner_id NULL: {null_owner_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_orphan_projects()