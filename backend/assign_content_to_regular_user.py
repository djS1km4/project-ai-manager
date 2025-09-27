#!/usr/bin/env python3
"""
Script para asignar contenido al usuario regular
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

def assign_content_to_regular_user():
    """Asignar algunos proyectos y tareas al usuario regular"""
    print("👤 Asignando contenido al usuario regular")
    print("=" * 50)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Buscar usuario regular
        regular_user = db.query(User).filter(User.email == "usuario@example.com").first()
        
        if not regular_user:
            print("❌ Usuario regular no encontrado")
            return
            
        print(f"✅ Usuario regular encontrado: {regular_user.email} (ID: {regular_user.id})")
        
        # Obtener algunos proyectos existentes para asignar
        available_projects = db.query(Project).limit(5).all()
        
        if not available_projects:
            print("❌ No hay proyectos disponibles para asignar")
            return
        
        print(f"\n📁 Asignando proyectos al usuario regular...")
        
        # Asignar los primeros 3 proyectos al usuario regular
        assigned_projects = 0
        for project in available_projects[:3]:
            # Cambiar el propietario del proyecto
            project.owner_id = regular_user.id
            assigned_projects += 1
            print(f"   ✅ Asignado proyecto: {project.name} (ID: {project.id})")
        
        # Obtener algunas tareas para asignar
        available_tasks = db.query(Task).limit(10).all()
        
        print(f"\n📋 Asignando tareas al usuario regular...")
        
        # Asignar las primeras 5 tareas al usuario regular
        assigned_tasks = 0
        for task in available_tasks[:5]:
            task.assignee_id = regular_user.id
            assigned_tasks += 1
            print(f"   ✅ Asignada tarea: {task.title} (ID: {task.id})")
        
        # Confirmar cambios
        db.commit()
        
        print(f"\n✅ Asignación completada:")
        print(f"   📁 Proyectos asignados: {assigned_projects}")
        print(f"   📋 Tareas asignadas: {assigned_tasks}")
        
        # Verificar la asignación
        print(f"\n🔍 Verificando asignación...")
        
        user_projects = db.query(Project).filter(Project.owner_id == regular_user.id).count()
        user_tasks = db.query(Task).filter(Task.assignee_id == regular_user.id).count()
        
        print(f"   📁 Total proyectos del usuario: {user_projects}")
        print(f"   📋 Total tareas del usuario: {user_tasks}")
        
    except Exception as e:
        print(f"❌ Error durante la asignación: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
    
    print("\n" + "=" * 50)
    print("🏁 Asignación de contenido completada")

if __name__ == "__main__":
    assign_content_to_regular_user()