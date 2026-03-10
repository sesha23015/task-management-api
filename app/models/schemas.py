from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class TaskBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="Название задачи"
    )
    description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Описание задачи"
    )
    priority: str = Field(
        "medium", 
        description="Приоритет задачи"
    )
    completed: bool = False

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: str) -> str:
        allowed_priorities = ['low', 'medium', 'high', 'critical']
        if v not in allowed_priorities:
            raise ValueError(f'Priority must be one of: {allowed_priorities}')
        return v
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        if re.search(r'[<>{}[\]\\]', v):
            raise ValueError('Title contains invalid characters')
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        return v.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[str] = None
    completed: Optional[bool] = None
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed_priorities = ['low', 'medium', 'high', 'critical']
            if v not in allowed_priorities:
                raise ValueError(f'Priority must be one of: {allowed_priorities}')
        return v

class TaskResponse(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
