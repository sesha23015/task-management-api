from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository
from app.models.schemas import TaskCreate, TaskUpdate
from app.config.settings import settings

class TaskService:
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate, user_id: str):
        task_repo = TaskRepository(db)
        
        # Проверка лимита задач
        if task_repo.count_by_user(user_id) >= settings.MAX_TASKS_PER_USER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum {settings.MAX_TASKS_PER_USER} tasks per user reached"
            )
        
        return task_repo.create({
            "title": task_data.title,
            "description": task_data.description,
            "priority": task_data.priority,
            "user_id": user_id
        })

    @staticmethod
    def get_all_tasks(db: Session, user_id: str, skip: int = 0, limit: int = 100):
        task_repo = TaskRepository(db)
        return task_repo.get_by_user(user_id, skip, limit)

    @staticmethod
    def get_task(db: Session, task_id: str, user_id: str):
        task_repo = TaskRepository(db)
        task = task_repo.get(task_id)
        
        if not task or task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    @staticmethod
    def update_task(db: Session, task_id: str, task_update: TaskUpdate, user_id: str):
        task = TaskService.get_task(db, task_id, user_id)  # Проверка прав
        
        update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
        if update_data:
            task = TaskRepository(db).update(task_id, update_data)
        
        return task

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str):
        task = TaskService.get_task(db, task_id, user_id)  # Проверка прав
        TaskRepository(db).delete(task_id)