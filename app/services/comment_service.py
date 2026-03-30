from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.comment import Comment
from app.models.task import Task
from app.models.schemas import CommentCreate
from app.exceptions import TaskNotFound, CommentNotFound

class CommentService:
    @staticmethod
    async def create_comment(db: AsyncSession, task_id: str, comment_ CommentCreate, user_id: str) -> Comment:
        result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
        task = result.scalar_one_or_none()
        if not task:
            raise TaskNotFound(task_id)
        
        comment = Comment(
            content=comment_data.content,
            task_id=task_id,
            user_id=user_id
        )
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment
    
    @staticmethod
    async def get_comments_by_task(db: AsyncSession, task_id: str, user_id: str) -> List[Comment]:
        result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
        task = result.scalar_one_or_none()
        if not task:
            raise TaskNotFound(task_id)
        
        result = await db.execute(select(Comment).where(Comment.task_id == task_id))
        return result.scalars().all()
    
    @staticmethod
    async def get_comment(db: AsyncSession, comment_id: str, user_id: str) -> Comment:
        result = await db.execute(select(Comment).where(Comment.id == comment_id))
        comment = result.scalar_one_or_none()
        if not comment:
            raise CommentNotFound(comment_id)
        
        result = await db.execute(select(Task).where(Task.id == comment.task_id, Task.user_id == user_id))
        task = result.scalar_one_or_none()
        if not task:
            raise TaskNotFound(comment.task_id)
        
        return comment