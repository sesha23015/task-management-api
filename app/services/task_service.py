from typing import List, Optional
from app.models.task import tasks_db, Task
from app.models.schemas import TaskCreate, TaskUpdate
from fastapi import HTTPException, status

class TaskService:
    @staticmethod
    def create_task(task_data: TaskCreate) -> Task:
        """Создание новой задачи"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority
        )
        tasks_db[task.id] = task
        return task
    
    @staticmethod
    def get_all_tasks() -> List[Task]:
        """Получение всех задач"""
        return list(tasks_db.values())
    
    @staticmethod
    def get_task(task_id: str) -> Task:
        """Получение задачи по ID"""
        task = tasks_db.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        return task
    
    @staticmethod
    def update_task(task_id: str, task_update: TaskUpdate) -> Task:
        """Обновление задачи"""
        task = TaskService.get_task(task_id)
        
        # Фильтруем None значения
        update_data = {k: v for k, v in task_update.model_dump().items() 
                      if v is not None}
        
        if update_data:
            task.update(**update_data)
        
        return task
    
    @staticmethod
    def delete_task(task_id: str) -> None:
        """Удаление задачи"""
        if task_id not in tasks_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        del tasks_db[task_id]
