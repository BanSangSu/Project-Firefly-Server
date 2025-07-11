from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.token import Token, RefreshTokenRequest
from schemas.user import UserCreate, UserPublic
from crud import crud_user, crud_token
from core import security
from core.config import settings
from .dependencies import get_db

router = APIRouter()

@router.post("/register", response_model=UserPublic)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if the username is already in use
    if await crud_user.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username is already in use.")
    # Check if the email is already registered
    if await crud_user.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email is already registered.")
    return await crud_user.create_user(db=db, user=user)

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Authenticate user by username or email and verify password
    user = await crud_user.get_user_by_username_or_email(db, identifier=form_data.username)
    if not user or not user.password_hash or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password.")
    
    access_token = security.create_access_token(data={"sub": user.email})
    refresh_token = await crud_token.create_refresh_token_for_user(db, user_id=user.id)
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token, "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    # Validate refresh token and check expiration
    db_token = await crud_token.get_refresh_token(db, token=refresh_data.refresh_token)
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is invalid or expired.")
    
    new_access_token = security.create_access_token(data={"sub": db_token.user.email})
    return {"access_token": new_access_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}
