# app/exceptions.py
from fastapi import HTTPException, status
from typing import Any, Dict

class AppException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(
            status_code=status_code,
            detail={"error": {"code": code, "message": message}}
        )

class TaskNotFound(AppException):
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="TASK_NOT_FOUND",
            message=f"Task with id {task_id} not found"
        )

class CommentNotFound(AppException):
    def __init__(self, comment_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="COMMENT_NOT_FOUND",
            message=f"Comment with id {comment_id} not found"
        )