#!/usr/bin/env python3
"""
Script para crear un usuario regular con credenciales específicas
"""

import sqlite3
import os
from passlib.context import CryptContext

# Configurar el contexto de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def create_regular_user():
    """Crear un usuario regular"""
    
    # Datos del usuario regular
    email = "usuario@example.com"
    username = "usuario"
    password = "usuario123"
    full_name = "Usuario Regular"
    
    db_path = "project_manager.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id, email, username, is_admin FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            user_id, user_email, user_username, is_admin = existing_user
            print(f"✅ Usuario {user_email} ya existe")
            print(f"   Username: {user_username}")
            print(f"   Admin: {bool(is_admin)}")
            print(f"   Password: {password}")
            return True
        
        # Crear hash de contraseña
        hashed_password = get_password_hash(password)
        
        # Insertar nuevo usuario
        cursor.execute("""
            INSERT INTO users (email, username, hashed_password, full_name, is_admin, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (email, username, hashed_password, full_name, False, True))
        
        conn.commit()
        
        # Verificar creación
        cursor.execute("SELECT id, email, username, is_admin, is_active FROM users WHERE email = ?", (email,))
        new_user = cursor.fetchone()
        
        if new_user:
            user_id, user_email, user_username, is_admin, is_active = new_user
            print("✅ Usuario regular creado exitosamente:")
            print(f"   ID: {user_id}")
            print(f"   Email: {user_email}")
            print(f"   Username: {user_username}")
            print(f"   Password: {password}")
            print(f"   Full Name: {full_name}")
            print(f"   Admin: {bool(is_admin)}")
            print(f"   Active: {bool(is_active)}")
            return True
        else:
            print("❌ Error al verificar la creación del usuario")
            return False
            
    except Exception as e:
        print(f"❌ Error al crear usuario: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    create_regular_user()