from fastapi import APIRouter, Depends

from app.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.auth.dependencies import get_current_user

from langgraph.checkpoint.memory import InMemorySaver
from agents.schemas import AgentContext
from agents.client import agent

router = APIRouter(tags=["AgentAI"])


@router.post("/chat")
async def chat(
    message: str,
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    request_context = AgentContext(user_db=user_db, session=session)
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        context=request_context,
    )
    # print(response)
    return {"message": response["messages"][-1].content}
