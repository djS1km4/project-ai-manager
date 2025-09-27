#!/usr/bin/env python3
"""
Script para verificar y crear usuarios administradores.
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import AuthService

def check_and_create_admin_users():
    """Verificar usuarios administradores existentes y crear uno si es necesario"""
    db = SessionLocal()
    
    try:
        # Verificar usuarios existentes
        all_users = db.query(User).all()
        print(f"👥 Total de usuarios: {len(all_users)}")
        print()
        
        # Mostrar usuarios con sus roles
        admin_users = []
        regular_users = []
        
        for user in all_users:
            print(f"👤 {user.username} ({user.email})")
            print(f"   ID: {user.id}")
            print(f"   Admin: {user.is_admin}")
            print(f"   Activo: {user.is_active}")
            print()
            
            if user.is_admin:
                admin_users.append(user)
            else:
                regular_users.append(user)
        
        print(f"📊 RESUMEN:")
        print(f"   Administradores: {len(admin_users)}")
        print(f"   Usuarios regulares: {len(regular_users)}")
        print()
        
        # Si no hay administradores, crear uno
        if not admin_users:
            print("🔧 No se encontraron administradores. Creando usuario admin...")
            
            # Crear usuario administrador
            admin_user = User(
                username="admin",
                email="admin@projectmanager.com",
                hashed_password=AuthService.get_password_hash("admin123"),
                is_admin=True,
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print(f"✅ Usuario administrador creado:")
            print(f"   Username: admin")
            print(f"   Email: admin@projectmanager.com")
            print(f"   Password: admin123")
            print(f"   ID: {admin_user.id}")
            
        else:
            print("✅ Administradores existentes:")
            for admin in admin_users:
                print(f"   - {admin.username} ({admin.email})")
        
        # Verificar si necesitamos hacer admin a algún usuario existente
        if len(admin_users) < 2:
            print(f"\n🔧 Convirtiendo usuario 'testuser' en administrador adicional...")
            testuser = db.query(User).filter(User.username == "testuser").first()
            if testuser:
                testuser.is_admin = True
                db.commit()
                print(f"✅ Usuario 'testuser' ahora es administrador")
            else:
                print(f"❌ Usuario 'testuser' no encontrado")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_create_admin_users()