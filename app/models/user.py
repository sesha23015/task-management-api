from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship  # ← ИМПОРТИРУЙТЕ ЭТО!
from sqlalchemy.sql import func
from app.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с учётом ограничения bcrypt (макс. 72 байта).
        """
        # Кодируем в UTF-8 и обрезаем до 72 БАЙТ (не символов!)
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Обрезаем и декодируем обратно, игнорируя неполные символы
            password_bytes = password_bytes[:72]
            password = password_bytes.decode('utf-8', errors='ignore')
        
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str) -> bool:
        # При проверке тоже обрезаем, если нужно
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            plain_password = password_bytes.decode('utf-8', errors='ignore')
        
        return pwd_context.verify(plain_password, self.hashed_password)