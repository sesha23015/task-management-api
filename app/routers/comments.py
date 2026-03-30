from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.comment_service import CommentService
from app.models.schemas import CommentCreate, CommentResponse
from app.utils.security import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/v1/tasks", tags=["Comments"], dependencies=[Depends(get_current_active_user)])

@router.post(
    "/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
    task_id: str,
    comment_ CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> CommentResponse:
    comment = await CommentService.create_comment(db, task_id, comment_data, current_user.id)
    return CommentResponse.model_validate(comment)

@router.get(
    "/{task_id}/comments",
    response_model=List[CommentResponse]
)
async def get_comments(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[CommentResponse]:
    comments = await CommentService.get_comments_by_task(db, task_id, current_user.id)
    return [CommentResponse.model_validate(c) for c in comments]