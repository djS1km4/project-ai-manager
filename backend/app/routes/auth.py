from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict, Any

from ..database import get_db
from ..models.user import User, UserCreate, UserLogin, UserResponse, Token, UserUpdate
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = AuthService.create_user(db, user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    user = AuthService.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": AuthService.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""
    token = credentials.credentials
    user = AuthService.get_current_user_from_token(db, token)
    return user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update current user's information"""
    token = credentials.credentials
    current_user = AuthService.get_current_user_from_token(db, token)
    
    updated_user = AuthService.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user

@router.post("/refresh", response_model=Token)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    token = credentials.credentials
    user = AuthService.get_current_user_from_token(db, token)
    
    access_token_expires = timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": AuthService.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user
    }

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    """Request password reset"""
    user = AuthService.get_user_by_email(db, email)
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If the email exists, a password reset link has been sent"}
    
    reset_token = AuthService.create_password_reset_token(user.id)
    
    # In a real application, you would send this token via email
    # For demo purposes, we'll return it (don't do this in production!)
    return {
        "message": "Password reset token generated",
        "reset_token": reset_token  # Remove this in production
    }

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """Reset password using reset token"""
    success = AuthService.reset_password(db, token, new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    return {"message": "Password reset successfully"}

@router.post("/logout")
def logout():
    """Logout user (client should discard token)"""
    return {"message": "Successfully logged out"}

# Admin routes
@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    token = credentials.credentials
    current_user = AuthService.get_current_user_from_token(db, token)
    
    if not AuthService.check_user_permissions(current_user, required_role="admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    new_role: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Change user role (admin only)"""
    token = credentials.credentials
    current_user = AuthService.get_current_user_from_token(db, token)
    
    if not AuthService.check_user_permissions(current_user, required_role="admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    if new_role not in ["admin", "manager", "member", "viewer"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    updated_user = AuthService.change_user_role(db, user_id, new_role)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User role changed to {new_role}", "user": updated_user}

@router.put("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Activate user account (admin only)"""
    token = credentials.credentials
    current_user = AuthService.get_current_user_from_token(db, token)
    
    if not AuthService.check_user_permissions(current_user, required_role="admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    success = AuthService.activate_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User activated successfully"}

@router.put("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Deactivate user account (admin only)"""
    token = credentials.credentials
    current_user = AuthService.get_current_user_from_token(db, token)
    
    if not AuthService.check_user_permissions(current_user, required_role="admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Prevent self-deactivation
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    success = AuthService.deactivate_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}