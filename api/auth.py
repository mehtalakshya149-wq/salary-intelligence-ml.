import uuid
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.schemas import UserCreate, UserResponse, Token
from api.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from api.models import User, ModelLog
from api.deps import get_current_user, get_current_admin
from api.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role if user.role == "admin" else "user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Log Registration
    reg_log = ModelLog(user_id=new_user.id, action="User Registered", endpoint="/auth/register")
    db.add(reg_log)
    db.commit()
    
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    # Log Successful Login
    login_log = ModelLog(user_id=user.id, action=f"Login Successful (Role: {user.role})", endpoint="/auth/login")
    db.add(login_log)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # JWT is stateless. We just return success and the client discards the token.
    return {"message": "Successfully logged out. Client should discard the token."}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
def read_admin_data(current_admin: User = Depends(get_current_admin)):
    return {"message": "Welcome Admin!", "secret_data": "Admin level statistics unlocked."}
