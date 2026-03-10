from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks
from app.config.settings import settings

# Создание экземпляра приложения
app = FastAPI(
    title=settings.APP_NAME,
    description="API для управления задачами",
    version=settings.APP_VERSION
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(tasks.router)

@app.get("/", tags=["Root"])
async def root():
    """Корневой endpoint с информацией об API"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "python_version": "3.12",
        "app_version": settings.APP_VERSION
    }
