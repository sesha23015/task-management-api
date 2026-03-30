# app/models/comment.py
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class Comment:
    def __init__(self, content: str, task_id: str, user_id: str = "system"):
        self.id = str(uuid.uuid4())
        self.content = content
        self.task_id = task_id
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update(self, content: str):
        self.content = content
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# In-memory storage
comments_db: Dict[str, Comment] = {}