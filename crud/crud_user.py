import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from database.models import User
from schemas.user import UserCreate
from core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Retrieve a user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Retrieve a user by username."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_username_or_email(db: AsyncSession, identifier: str) -> User | None:
    """Retrieve a user by username or email (used for login)."""
    result = await db.execute(
        select(User).where(or_(User.username == identifier, User.email == identifier))
    )
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Create a new user (email/password registration)."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_or_create_social_user(db: AsyncSession, *, email: str, username: str) -> User:
    """
    Retrieve or create a social login user.
    If the user already exists, return the user information.
    """
    user = await get_user_by_email(db, email=email)
    if user:
        return user
    
    # Prevent possible username duplication.
    db_user_by_username = await get_user_by_username(db, username=username)
    if db_user_by_username:
        # If the name provided by Google, Apple, etc. is duplicated, add a random string.
        username = f"{username}_{secrets.token_hex(4)}"

    # Create a new social user without a password.
    new_user = User(email=email, username=username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
