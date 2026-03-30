from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, init_db
from app.routers import tasks, auth, comments, files
from app.config.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="API для управления задачами с аутентификацией",
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(comments.router)
app.include_router(files.router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    from app.services.minio_service import minio_service
    minio_service.init_bucket()

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    from app.database import engine
    from app.services.minio_service import minio_service
    
    db_status = "connected"
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
    except Exception:
        db_status = "disconnected"
    
    minio_status = "connected" if minio_service.check_connection() else "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" and minio_status == "connected" else "degraded",
        "database": db_status,
        "minio": minio_status,
        "python_version": "3.12",
        "app_version": settings.APP_VERSION
    }

@app.get("/info", tags=["Info"])
async def get_info():
    import os
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": os.getenv("DEBUG", "false").lower() == "true"
    }