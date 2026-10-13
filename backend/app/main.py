from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth as auth_router
from app.routers import users as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the schema on startup using the SQLAlchemy metadata."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Cross-Language Messaging API",
    description="Backend foundation for the AI-powered cross-language messaging system.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(users_router.public_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the backend health status."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    """Return a welcome message with documentation hints."""
    return {"message": "Welcome to the Cross-Language Messaging API. View the docs at /docs."}
