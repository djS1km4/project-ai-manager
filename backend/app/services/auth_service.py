from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User, UserCreate, UserUpdate
import os
from dotenv import load_dotenv

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = AuthService.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = AuthService.get_password_hash(user.password)
        
        # Create user
        db_user = User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
            role=user.role,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        
        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = AuthService.get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        """Deactivate a user account"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        
        db_user.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def activate_user(db: Session, user_id: int) -> bool:
        """Activate a user account"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        
        db_user.is_active = True
        db.commit()
        return True
    
    @staticmethod
    def change_user_role(db: Session, user_id: int, new_role: str) -> Optional[User]:
        """Change user role"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        db_user.role = new_role
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_current_user_from_token(db: Session, token: str) -> User:
        """Get current user from JWT token"""
        try:
            payload = AuthService.verify_token(token)
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = AuthService.get_user_by_id(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        return user
    
    @staticmethod
    def check_user_permissions(user: User, required_role: str = None, required_permissions: list = None) -> bool:
        """Check if user has required permissions"""
        if not user.is_active:
            return False
        
        # Check role-based permissions
        if required_role:
            role_hierarchy = {
                "admin": 3,
                "manager": 2,
                "member": 1,
                "viewer": 0
            }
            
            user_level = role_hierarchy.get(user.role, 0)
            required_level = role_hierarchy.get(required_role, 0)
            
            if user_level < required_level:
                return False
        
        # Check specific permissions (if implemented)
        if required_permissions:
            # This could be extended to check specific permissions
            # For now, we'll assume admin has all permissions
            if user.role != "admin":
                return False
        
        return True
    
    @staticmethod
    def create_password_reset_token(user_id: int) -> str:
        """Create a password reset token"""
        expire = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        to_encode = {"sub": str(user_id), "exp": expire, "type": "password_reset"}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[int]:
        """Verify password reset token and return user ID"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "password_reset":
                return None
            user_id = int(payload.get("sub"))
            return user_id
        except (JWTError, ValueError):
            return None
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> bool:
        """Reset user password using reset token"""
        user_id = AuthService.verify_password_reset_token(token)
        if not user_id:
            return False
        
        user = AuthService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        user.hashed_password = AuthService.get_password_hash(new_password)
        db.commit()
        return True