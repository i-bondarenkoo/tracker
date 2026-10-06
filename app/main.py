from fastapi import FastAPI
import uvicorn
from app.views.user import router as user_router
from app.views.category import router as category_router
from app.views.transaction import router as transaction_router
from app.auth.views import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.views.agent import router as agent_router
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from app.core.config import settings
from langchain.agents import create_agent
from agents.client import system_prompt, llm_model
from agents.tools import list_tools
from contextlib import asynccontextmanager
from agents.schemas import AgentContext


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncPostgresSaver.from_conn_string(
        settings.checkpointer_db_url
    ) as checkpointer:
        # автоматически создаст в базе необходмые таблицы
        # для сохранения истории диалога
        await checkpointer.setup()
        app.state.agent = create_agent(
            llm_model,
            tools=list_tools,
            system_prompt=system_prompt,
            context_schema=AgentContext,
            checkpointer=checkpointer,
        )
        yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)
app.include_router(auth_router)
app.include_router(agent_router)
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        reload=True,
    )
