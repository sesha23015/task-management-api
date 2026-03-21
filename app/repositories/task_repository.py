# app/repositories/task_repository.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)
    
    def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> list[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()
    
    def count_by_user(self, user_id: str) -> int:
        return self.db.query(Task).filter(Task.user_id == user_id).count()