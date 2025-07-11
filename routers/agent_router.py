from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import AIMessage, HumanMessage

from routers.dependencies import get_current_user, get_db
from database.models import User

# from database.session import AsyncSessionLocal
# from crud import crud_conversation
from schemas.agent import AgentRequest, AgentResponse
from agents.agent_firefly import agent_instance

router = APIRouter()

# # Dependency function to get DB session
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session

@router.post("/invoke", response_model=AgentResponse)
async def invoke_agent(
    request: AgentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Call the AI agent and manage conversation history."""
    try:
        # # 1. Retrieve previous conversation history from DB and convert to LangChain message format
        # db_history = await crud_conversation.get_history_by_session(db, session_id=request.session_id)
        # chat_history = []
        # for h in db_history:
        #     if h.role == "human":
        #         chat_history.append(HumanMessage(content=h.message))
        #     elif h.role == "ai":
        #         chat_history.append(AIMessage(content=h.message))

        # # 2. Save user request (prompt) to DB
        # await crud_conversation.create_history_entry(
        #     db=db, session_id=request.session_id, role="human", message=request.prompt
        # )
        
        # # 3. Call AI agent logic (pass session ID, prompt, and conversation history)
        # agent_result = await agent_instance.invoke(
        #     session_id=request.session_id,
        #     prompt=request.prompt,
        #     history=chat_history
        # )
        
        # # 4. Save AI response to DB
        # await crud_conversation.create_history_entry(
        #     db=db, session_id=request.session_id, role="ai", message=agent_result["response_text"]
        # )
        
        # # 5. Return final result to client (Unity)
        # return AgentResponse(
        #     session_id=request.session_id,
        #     action=agent_result["action"],
        #     response_text=agent_result["response_text"]
        # )

        agent_result = await agent_instance.invoke(
            session_id=request.session_id,
            prompt=request.prompt,
        )
        
        
        # # Return final result to client (Unity)
        # return AgentResponse(
        #     session_id=request.session_id,
        #     action=agent_result["action"],
        #     response_text=agent_result["response_text"]
        # )
        return AgentResponse(
            session_id=request.session_id,
            response_text=agent_result["response_text"]
        )
    except Exception as e:
        # More detailed logging is needed in production
        raise HTTPException(status_code=500, detail=f"Error occurred while processing agent: {str(e)}")