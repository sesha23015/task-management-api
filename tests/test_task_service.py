import pytest
from unittest.mock import patch
from app.services.task_service import TaskService
from app.models.schemas import TaskCreate
from app.models.task import Task

class TestTaskService:
    
    @patch('app.services.task_service.tasks_db')
    def test_create_task(self, mock_tasks_db):
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            priority="high"
        )
        
        result = TaskService.create_task(task_data)
        
        assert isinstance(result, Task)
        assert result.title == "Test Task"
        assert result.description == "Test Description"
        assert result.priority == "high"
        assert result.completed == False
        assert mock_tasks_db.__setitem__.called