from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os
from pathlib import Path

from config.settings import settings
from api.router import api_router
from utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

# Ensure storage directory exists at startup
Path("storage").mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Guruji backend starting — using JSON file store (no DB/Redis required).")
    yield
    logger.info("AI Guruji backend shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated audio/video/storage files directly as static files
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

# Include all API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "version": settings.VERSION, "store": "json"}
