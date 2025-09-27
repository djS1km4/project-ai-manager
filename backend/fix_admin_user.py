#!/usr/bin/env python3
"""
Script para recrear el usuario administrador con la contraseña correcta
"""

import sqlite3
from passlib.context import CryptContext

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_admin_user():
    """Recrear el usuario administrador con la contraseña correcta"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('project_manager.db')
    cursor = conn.cursor()
    
    # Eliminar el usuario administrador existente
    cursor.execute("DELETE FROM users WHERE email = 'admin@example.com'")
    print("Usuario administrador anterior eliminado")
    
    # Crear nuevo usuario administrador
    admin_password = "adminpassword123"
    hashed_password = pwd_context.hash(admin_password)
    
    cursor.execute("""
        INSERT INTO users (email, username, full_name, hashed_password, is_active, is_admin)
        VALUES (?, ?, ?, ?, 1, 1)
    """, ('admin@example.com', 'admin', 'Administrator', hashed_password))
    
    print(f"✅ Usuario administrador recreado con contraseña: {admin_password}")
    
    # Confirmar cambios
    conn.commit()
    conn.close()
    
    print("🎉 Usuario administrador corregido exitosamente!")

if __name__ == "__main__":
    fix_admin_user()