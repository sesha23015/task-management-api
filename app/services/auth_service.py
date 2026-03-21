from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.schemas import UserCreate, UserLogin, Token
from app.utils.security import create_access_token
import uuid

class AuthService:
    @staticmethod
    def register(db: Session, user_data: UserCreate) -> User:
        user_repo = UserRepository(db)
        
        # Проверка уникальности
        if user_repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if user_repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Создание пользователя
        user = user_repo.create({
            "id": str(uuid.uuid4()),
            "email": user_data.email,
            "username": user_data.username,
            "hashed_password": User.hash_password(user_data.password),
            "is_active": True
        })
        return user

    @staticmethod
    def login(db: Session, credentials: UserLogin) -> Token:
        user_repo = UserRepository(db)
        user = user_repo.get_by_email(credentials.email)
        
        if not user or not user.verify_password(credentials.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.id})
        return Token(access_token=access_token)