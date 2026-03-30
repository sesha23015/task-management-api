from typing import List
from app.models.comment import comments_db, Comment
from app.models.task import tasks_db
from app.models.schemas import CommentCreate
from app.exceptions import TaskNotFound, CommentNotFound

class CommentService:
    @staticmethod
    def create_comment(task_id: str, comment_data: CommentCreate, user_id: str = "system") -> Comment:
        """Создание нового комментария"""
        
        if task_id not in tasks_db:
            raise TaskNotFound(task_id)
        
        comment = Comment(
            content=comment_data.content,
            task_id=task_id,
            user_id=user_id
        )
        comments_db[comment.id] = comment
        
        tasks_db[task_id].comments.append(comment.to_dict())
        
        return comment
    
    @staticmethod
    def get_comments_by_task(task_id: str) -> List[Comment]:
        """Получение всех комментариев задачи"""
        
        if task_id not in tasks_db:
            raise TaskNotFound(task_id)
        
        return [c for c in comments_db.values() if c.task_id == task_id]
    
    @staticmethod
    def get_comment(comment_id: str) -> Comment:
        """Получение комментария по ID"""
        comment = comments_db.get(comment_id)
        if not comment:
            raise CommentNotFound(comment_id)
        return comment