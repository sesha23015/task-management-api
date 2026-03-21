from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import UserCreate, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService
from app.utils.security import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Создаёт нового пользователя и возвращает его данные"""
    return AuthService.register(db, user_data)

@router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему"
)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Аутентифицирует пользователя и возвращает JWT токен"""
    return AuthService.login(db, credentials)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Получить текущий профиль"
)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Возвращает данные текущего аутентифицированного пользователя"""
    return current_user