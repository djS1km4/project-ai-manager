#!/usr/bin/env python3
"""
Script to check user details and password
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.database import engine
from passlib.context import CryptContext

def check_user():
    """Check user details"""
    conn = engine.connect()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    try:
        # Get admin user details
        result = conn.execute(text("SELECT id, email, username, hashed_password, is_active FROM users WHERE email = 'admin@example.com'"))
        user = result.fetchone()
        
        if user:
            print(f"Admin user found:")
            print(f"  ID: {user[0]}")
            print(f"  Email: {user[1]}")
            print(f"  Username: {user[2]}")
            print(f"  Password hash: {user[3][:50]}...")
            print(f"  Active: {user[4]}")
            
            # Test password verification
            test_password = "adminpassword123"
            is_valid = pwd_context.verify(test_password, user[3])
            print(f"  Password 'adminpassword123' is valid: {is_valid}")
            
            # Try other common passwords
            for pwd in ["password", "test", "123456", "admin"]:
                is_valid = pwd_context.verify(pwd, user[3])
                if is_valid:
                    print(f"  Password '{pwd}' is valid: {is_valid}")
                    
        else:
            print("User not found")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_user()