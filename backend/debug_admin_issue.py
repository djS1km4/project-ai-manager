#!/usr/bin/env python3
"""
Script para diagnosticar el problema específico del usuario administrador
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

def debug_admin_issue():
    """Diagnosticar el problema del usuario administrador"""
    print("🔍 Diagnosticando problema del usuario administrador")
    print("=" * 60)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Buscar usuario administrador
        admin_user = db.query(User).filter(User.email == "test@example.com").first()
        
        if not admin_user:
            print("❌ Usuario administrador no encontrado")
            return
            
        print(f"✅ Usuario administrador encontrado:")
        print(f"   ID: {admin_user.id}")
        print(f"   Email: {admin_user.email}")
        print(f"   Username: {admin_user.username}")
        print(f"   Is Admin: {admin_user.is_admin}")
        print(f"   Is Active: {admin_user.is_active}")
        
        # Verificar proyectos del administrador
        print(f"\n📁 Proyectos del administrador:")
        admin_projects = db.query(Project).filter(Project.owner_id == admin_user.id).all()
        print(f"   Total proyectos: {len(admin_projects)}")
        
        if admin_projects:
            for i, project in enumerate(admin_projects[:5]):  # Mostrar primeros 5
                print(f"   {i+1}. {project.name} (ID: {project.id}) - Estado: {project.status}")
        
        # Verificar tareas del administrador
        print(f"\n📋 Tareas del administrador:")
        admin_tasks = db.query(Task).filter(Task.assignee_id == admin_user.id).all()
        print(f"   Total tareas asignadas: {len(admin_tasks)}")
        
        if admin_tasks:
            for i, task in enumerate(admin_tasks[:5]):  # Mostrar primeras 5
                print(f"   {i+1}. {task.title} (ID: {task.id}) - Estado: {task.status}")
        
        # Verificar todos los proyectos (para admin debería ver todos)
        print(f"\n🌐 Todos los proyectos en el sistema:")
        all_projects = db.query(Project).all()
        print(f"   Total proyectos en sistema: {len(all_projects)}")
        
        # Verificar todas las tareas
        print(f"\n🌐 Todas las tareas en el sistema:")
        all_tasks = db.query(Task).all()
        print(f"   Total tareas en sistema: {len(all_tasks)}")
        
        # Verificar si hay problemas con los enum values
        print(f"\n🔍 Verificando valores de enum:")
        
        # Verificar proyectos con problemas de enum
        problematic_projects = []
        for project in all_projects:
            try:
                # Intentar acceder a los atributos que podrían causar problemas
                status = project.status
                priority = project.priority
            except Exception as e:
                problematic_projects.append((project.id, str(e)))
        
        if problematic_projects:
            print(f"   ❌ Proyectos con problemas de enum: {len(problematic_projects)}")
            for project_id, error in problematic_projects[:3]:
                print(f"      Proyecto {project_id}: {error}")
        else:
            print(f"   ✅ No hay problemas de enum en proyectos")
        
        # Verificar tareas con problemas de enum
        problematic_tasks = []
        for task in all_tasks:
            try:
                # Intentar acceder a los atributos que podrían causar problemas
                status = task.status
                priority = task.priority
            except Exception as e:
                problematic_tasks.append((task.id, str(e)))
        
        if problematic_tasks:
            print(f"   ❌ Tareas con problemas de enum: {len(problematic_tasks)}")
            for task_id, error in problematic_tasks[:3]:
                print(f"      Tarea {task_id}: {error}")
        else:
            print(f"   ✅ No hay problemas de enum en tareas")
            
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("🏁 Diagnóstico completado")

if __name__ == "__main__":
    debug_admin_issue()