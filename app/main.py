from fastapi import FastAPI
import uvicorn
from app.views.user import router as user_router
from app.views.category import router as category_router
from app.views.transaction import router as transaction_router

app = FastAPI()
app.include_router(user_router)
app.include_router(category_router)
app.include_router(transaction_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        reload=True,
    )
