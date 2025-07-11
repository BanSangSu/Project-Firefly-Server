from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import settings
from core.security import create_refresh_token
from database.models import RefreshToken

async def create_refresh_token_for_user(db: AsyncSession, user_id: int) -> str:
    """
    Create a new refresh token for the user and save it to the DB.
    """
    # Generate a token as a secure random string
    token_str = create_refresh_token()
    
    # Calculate expiration period from settings
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Create RefreshToken object to save in DB
    db_token = RefreshToken(token=token_str, user_id=user_id, expires_at=expires_at)
    
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    
    return token_str

async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
    """
    Retrieve a RefreshToken object from the DB using the token string.
    """
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    return result.scalars().first()
