from fastapi import APIRouter, Depends, Request

from app.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.auth.dependencies import get_current_user

from agents.schemas import AgentContext

router = APIRouter(tags=["AgentAI"])


@router.post("/chat")
async def chat(
    message: str,
    request: Request,
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    thread_id = str(user_db.id)
    request_context = AgentContext(user_db=user_db, session=session)
    response = await request.app.state.agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        {
            "configurable": {
                "thread_id": thread_id,
            }
        },
        context=request_context,
    )
    # print(response)
    return {"message": response["messages"][-1].content}
