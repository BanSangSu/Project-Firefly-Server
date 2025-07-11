from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings
from routers import agent_router, login #, social_login

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up {settings.APP_TITLE} v{settings.APP_VERSION}...")
    yield
    print("Shutting down AI Agent Server.")

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG_MODE
)

# Add SessionMiddleware for Authlib social login
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include routers
app.include_router(login.router, prefix="/auth", tags=["Authentication"])
# app.include_router(social_login.router, prefix="/auth", tags=["Social Login"])
app.include_router(agent_router.router, prefix="/api/v1/agent", tags=["AI Agent"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to {settings.APP_TITLE}!"}