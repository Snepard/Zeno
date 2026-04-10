from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config.settings import settings
from api.router import api_router
from utils.exceptions import global_exception_handler
from utils.logger import setup_logging
# For dev migrations
# from db.database import engine
# from models.base import Base

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Zeno Backend...")
    # Optional DB Sync (if alembic is not configured yet):
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting down Zeno Backend...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for React + Three.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handler
app.add_exception_handler(Exception, global_exception_handler)

# Include main router
app.include_router(api_router)

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint useful for monitoring/k8s probes."""
    return {"status": "healthy", "version": settings.VERSION}

