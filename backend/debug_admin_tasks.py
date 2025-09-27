#!/usr/bin/env python3
"""
Script para debuggear el problema específico con las tareas de administradores
"""

import sqlite3
import os
from app.database import get_db
from app.services.task_service import TaskService
from app.models.user import User
from app.models.task import Task
from app.models.project import Project, ProjectMember
from sqlalchemy.orm import Session
from sqlalchemy import text

def debug_admin_tasks():
    """Debuggear el problema con las tareas de administradores"""
    print("🔍 Debuggeando problema con tareas de administradores...")
    
    # Obtener sesión de base de datos
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Obtener usuario administrador
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            print("❌ Usuario administrador no encontrado")
            return
        
        print(f"✅ Usuario admin encontrado: ID {admin_user.id}, is_admin: {admin_user.is_admin}")
        
        # Obtener usuario regular para comparar
        regular_user = db.query(User).filter(User.email == "test@example.com").first()
        if not regular_user:
            print("❌ Usuario regular no encontrado")
            return
        
        print(f"✅ Usuario regular encontrado: ID {regular_user.id}, is_admin: {regular_user.is_admin}")
        
        # Probar TaskService con usuario regular
        print("\n🔍 Probando TaskService con usuario regular...")
        task_service = TaskService()
        
        try:
            regular_tasks = task_service.get_tasks(db, regular_user.id)
            print(f"✅ Usuario regular: {len(regular_tasks)} tareas obtenidas")
        except Exception as e:
            print(f"❌ Error con usuario regular: {e}")
        
        # Probar TaskService con administrador
        print("\n🔍 Probando TaskService con administrador...")
        
        try:
            admin_tasks = task_service.get_tasks(db, admin_user.id)
            print(f"✅ Administrador: {len(admin_tasks)} tareas obtenidas")
        except Exception as e:
            print(f"❌ Error con administrador: {e}")
            print(f"   Tipo de error: {type(e)}")
            import traceback
            traceback.print_exc()
        
        # Verificar estructura de base de datos
        print("\n🔍 Verificando estructura de base de datos...")
        
        # Contar tareas totales
        total_tasks = db.query(Task).count()
        print(f"   Total de tareas en BD: {total_tasks}")
        
        # Contar proyectos totales
        total_projects = db.query(Project).count()
        print(f"   Total de proyectos en BD: {total_projects}")
        
        # Verificar ProjectMember
        total_members = db.query(ProjectMember).count()
        print(f"   Total de miembros de proyecto: {total_members}")
        
        # Verificar si admin está en ProjectMember
        admin_memberships = db.query(ProjectMember).filter(ProjectMember.user_id == admin_user.id).count()
        print(f"   Membresías del admin: {admin_memberships}")
        
        # Verificar si regular user está en ProjectMember
        regular_memberships = db.query(ProjectMember).filter(ProjectMember.user_id == regular_user.id).count()
        print(f"   Membresías del usuario regular: {regular_memberships}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_admin_tasks()