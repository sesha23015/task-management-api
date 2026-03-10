from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Task Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    MAX_TASKS_PER_USER: int = 1000
    
    class Config:
        env_file = ".env"

settings = Settings()
