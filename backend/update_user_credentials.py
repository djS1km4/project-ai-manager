#!/usr/bin/env python3
"""
Script para actualizar las credenciales de los usuarios existentes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import AuthService

def update_user_credentials():
    """Actualizar las credenciales de los usuarios existentes"""
    db = SessionLocal()
    try:
        # Actualizar usuario administrador test@example.com
        admin_user = db.query(User).filter(User.email == "test@example.com").first()
        if admin_user:
            admin_user.hashed_password = AuthService.get_password_hash("testpassword123")
            admin_user.is_admin = True
            print("✅ Usuario test@example.com actualizado")
        
        # Crear usuario regular usuario@example.com si no existe
        regular_user = db.query(User).filter(User.email == "usuario@example.com").first()
        if not regular_user:
            regular_user = User(
                email="usuario@example.com",
                username="usuario",
                hashed_password=AuthService.get_password_hash("usuario123"),
                full_name="Usuario Regular",
                is_active=True,
                is_admin=False
            )
            db.add(regular_user)
            print("✅ Usuario usuario@example.com creado")
        else:
            regular_user.hashed_password = AuthService.get_password_hash("usuario123")
            regular_user.is_admin = False
            print("✅ Usuario usuario@example.com actualizado")
        
        db.commit()
        print("\n📋 Credenciales actualizadas:")
        print("  - test@example.com / testpassword123 (Admin)")
        print("  - usuario@example.com / usuario123 (Usuario regular)")
        
    except Exception as e:
        print(f"❌ Error al actualizar credenciales: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_user_credentials()