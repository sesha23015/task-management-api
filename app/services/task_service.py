from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.models.schemas import TaskCreate, TaskUpdate
from app.exceptions import TaskNotFound
from fastapi import status

class TaskService:
    @staticmethod
    async def create_task(db: AsyncSession, task_ TaskCreate, user_id: str) -> Task:
        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            user_id=user_id
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task
    
    @staticmethod
    async def get_all_tasks(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await db.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_task(db: AsyncSession, task_id: str, user_id: str) -> Task:
        result = await db.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise TaskNotFound(task_id)
        return task
    
    @staticmethod
    async def update_task(db: AsyncSession, task_id: str, task_update: TaskUpdate, user_id: str) -> Task:
        task = await TaskService.get_task(db, task_id, user_id)
        
        update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
        
        for key, value in update_data.items():
            setattr(task, key, value)
        
        await db.commit()
        await db.refresh(task)
        return task
    
    @staticmethod
    async def delete_task(db: AsyncSession, task_id: str, user_id: str) -> None:
        task = await TaskService.get_task(db, task_id, user_id)
        await db.delete(task)
        await db.commit()