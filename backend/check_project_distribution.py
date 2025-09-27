#!/usr/bin/env python3
"""
Script para verificar la distribución de proyectos entre usuarios.
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.project import Project
from app.models.user import User

def check_project_distribution():
    """Verificar cómo están distribuidos los proyectos entre usuarios"""
    db = SessionLocal()
    
    try:
        # Obtener todos los usuarios
        users = db.query(User).all()
        print(f"📊 Total de usuarios: {len(users)}")
        print("=" * 60)
        
        # Contar proyectos por usuario
        project_counts = {}
        total_projects = 0
        
        for user in users:
            project_count = db.query(Project).filter(Project.owner_id == user.id).count()
            project_counts[user.id] = {
                'username': user.username,
                'email': user.email,
                'project_count': project_count
            }
            total_projects += project_count
        
        # Mostrar distribución ordenada por cantidad de proyectos
        print("📁 DISTRIBUCIÓN DE PROYECTOS POR USUARIO:")
        print("-" * 60)
        
        sorted_users = sorted(project_counts.items(), key=lambda x: x[1]['project_count'], reverse=True)
        
        for user_id, data in sorted_users:
            if data['project_count'] > 0:
                print(f"👤 {data['username']} ({data['email']})")
                print(f"   📁 Proyectos: {data['project_count']}")
                print()
        
        print("=" * 60)
        print(f"📊 RESUMEN:")
        print(f"   Total proyectos verificados: {total_projects}")
        print(f"   Usuarios con proyectos: {len([u for u in project_counts.values() if u['project_count'] > 0])}")
        print(f"   Usuarios sin proyectos: {len([u for u in project_counts.values() if u['project_count'] == 0])}")
        
        # Verificar el total en la base de datos
        db_total = db.query(Project).count()
        print(f"   Total en BD: {db_total}")
        
        if total_projects != db_total:
            print(f"⚠️  ADVERTENCIA: Discrepancia en el conteo!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_project_distribution()