from fastapi import APIRouter, Depends
from langchain.agents import create_agent
from agents.tools import create_tools
from app.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.auth.dependencies import get_current_user
from agents.client import llm_model, system_prompt

router = APIRouter(tags=["AgentAI"])


@router.post("/chat")
async def chat(
    message: str,
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    tools = create_tools(
        user_db=user_db,
        session=session,
    )
    agent = create_agent(
        llm_model,
        tools=tools,
        system_prompt=system_prompt,
    )
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        }
    )
    # print(response)
    return {"message": response["messages"][-1].content}
