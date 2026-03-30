from fastapi import APIRouter, Depends, status, Query
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.utils.security import get_current_active_user
from app.models.user import User
from app.models.task import Task

router = APIRouter(prefix="/v1/tasks", tags=["tasks"], dependencies=[Depends(get_current_active_user)])

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу"
)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> TaskResponse:
    new_task = TaskService.create_task(db, task, current_user.id)
    return TaskResponse.model_validate(new_task)

@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Получить все задачи пользователя"
)
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[TaskResponse]:
    tasks = TaskService.get_all_tasks(db, current_user.id, skip, limit)
    return [TaskResponse.model_validate(task) for task in tasks]

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить задачу по ID"
)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> TaskResponse:
    task = TaskService.get_task(db, task_id, current_user.id)
    return TaskResponse.model_validate(task)

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновить задачу"
)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> TaskResponse:
    updated_task = TaskService.update_task(db, task_id, task_update, current_user.id)
    return TaskResponse.model_validate(updated_task)

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу"
)
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    TaskService.delete_task(db, task_id, current_user.id)