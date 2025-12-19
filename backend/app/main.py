from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
# Import routers will be added later
# from app.api import api

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Backend API for MarketWay Navigator"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for images
app.mount("/images", StaticFiles(directory=settings.IMAGES_DIR), name="images")

@app.get("/")
async def root():
    return {
        "message": "Welcome to MarketWay Navigator API",
        "docs": "/docs",
        "version": settings.PROJECT_VERSION
    }

# Include routers
from app.api.api import api
app.include_router(api.router)
