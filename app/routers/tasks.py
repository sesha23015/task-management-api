from fastapi import APIRouter, status
from typing import List
from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post(
    "/", 
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу"
)
async def create_task(task: TaskCreate) -> TaskResponse:
    """Создание новой задачи"""
    new_task = TaskService.create_task(task)
    return TaskResponse.model_validate(new_task.to_dict())

@router.get(
    "/", 
    response_model=List[TaskResponse],
    summary="Получить все задачи"
)
async def get_tasks() -> List[TaskResponse]:
    """Возвращает список всех задач"""
    tasks = TaskService.get_all_tasks()
    return [TaskResponse.model_validate(task.to_dict()) for task in tasks]

@router.get(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="Получить задачу по ID"
)
async def get_task(task_id: str) -> TaskResponse:
    """Возвращает конкретную задачу по её ID"""
    task = TaskService.get_task(task_id)
    return TaskResponse.model_validate(task.to_dict())

@router.put(
    "/{task_id}", 
    response_model=TaskResponse,
    summary="Обновить задачу"
)
async def update_task(task_id: str, task_update: TaskUpdate) -> TaskResponse:
    """Обновляет существующую задачу"""
    updated_task = TaskService.update_task(task_id, task_update)
    return TaskResponse.model_validate(updated_task.to_dict())

@router.delete(
    "/{task_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу"
)
async def delete_task(task_id: str) -> None:
    """Удаляет задачу по ID"""
    TaskService.delete_task(task_id)
