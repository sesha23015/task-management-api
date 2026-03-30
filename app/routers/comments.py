from fastapi import APIRouter, HTTPException, status
from typing import List
from app.services.comment_service import CommentService
from app.models.schemas import CommentCreate, CommentResponse
from app.exceptions import TaskNotFound, CommentNotFound

router = APIRouter(prefix="/v1/tasks", tags=["Comments"])

@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(task_id: str, comment_data: CommentCreate):
    comment = CommentService.create_comment(task_id, comment_data)
    return comment

@router.get("/{task_id}/comments", response_model=List[CommentResponse])
async def get_comments(task_id: str):
    comments = CommentService.get_comments_by_task(task_id)
    return comments