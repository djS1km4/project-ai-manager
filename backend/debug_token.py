#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.auth_service import AuthService
from app.database import get_db

def test_token():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU4NzI5NTI2fQ.c25cNMhZfBzO5wSB69Mg7tABwi28DCNtadAXSBsGmn0"
    
    try:
        print("Testing token verification...")
        payload = AuthService.verify_token(token)
        print(f"Payload: {payload}")
        
        user_id_str = payload.get("sub")
        print(f"User ID string: {user_id_str}")
        print(f"Type: {type(user_id_str)}")
        
        user_id = int(user_id_str)
        print(f"User ID int: {user_id}")
        
        # Test with database
        db = next(get_db())
        user = AuthService.get_current_user_from_token(db, token)
        print(f"User found: {user.email}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_token()