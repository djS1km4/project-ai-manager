#!/usr/bin/env python3
"""
Script para debuggear el servicio de proyectos directamente.
"""

import traceback
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.project_service import ProjectService

def debug_project_service():
    """Debuggear el servicio de proyectos"""
    db = SessionLocal()
    project_service = ProjectService()
    
    try:
        print("🔍 Probando ProjectService.get_projects()...")
        
        # Probar con el usuario testuser (ID 12)
        user_id = 12
        print(f"Usuario ID: {user_id}")
        
        projects = project_service.get_projects(db, user_id)
        print(f"✅ Proyectos obtenidos: {len(projects)}")
        
        for i, project in enumerate(projects[:3]):  # Solo mostrar los primeros 3
            print(f"  {i+1}. {project['name']} - Status: {project['status']}")
        
    except Exception as e:
        print(f"❌ Error en get_projects: {e}")
        print("Stack trace:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_project_service()