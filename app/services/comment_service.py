from typing import List
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.task import Task
from app.models.schemas import CommentCreate
from app.exceptions import TaskNotFound, CommentNotFound

class CommentService:
    @staticmethod
    def create_comment(db: Session, task_id: str, comment_data: CommentCreate, user_id: str) -> Comment:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            raise TaskNotFound(task_id)
        
        comment = Comment(
            content=comment_data.content,
            task_id=task_id,
            user_id=user_id
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    
    @staticmethod
    def get_comments_by_task(db: Session, task_id: str, user_id: str) -> List[Comment]:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            raise TaskNotFound(task_id)
        
        return db.query(Comment).filter(Comment.task_id == task_id).all()
    
    @staticmethod
    def get_comment(db: Session, comment_id: str, user_id: str) -> Comment:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise CommentNotFound(comment_id)
        
        task = db.query(Task).filter(Task.id == comment.task_id, Task.user_id == user_id).first()
        if not task:
            raise TaskNotFound(comment.task_id)
        
        return comment