from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import ConversationHistory

async def create_history_entry(db: AsyncSession, *, session_id: str, role: str, message: str) -> ConversationHistory:
    """
    Create a new conversation history entry (user or AI) and save it to the DB.
    
    :param db: SQLAlchemy async session
    :param session_id: Unique ID to distinguish the conversation
    :param role: The sender of the message ('human' or 'ai')
    :param message: The actual message content
    """
    db_entry = ConversationHistory(session_id=session_id, role=role, message=message)
    
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    
    return db_entry

async def get_history_by_session(db: AsyncSession, session_id: str) -> list[ConversationHistory]:
    """
    Retrieve all conversation history for a specific session ID in chronological order.
    
    :param db: SQLAlchemy async session
    :param session_id: Unique ID of the conversation to retrieve
    """
    result = await db.execute(
        select(ConversationHistory)
        .where(ConversationHistory.session_id == session_id)
        .order_by(ConversationHistory.id)  # id order is chronological
    )
    return result.scalars().all()
