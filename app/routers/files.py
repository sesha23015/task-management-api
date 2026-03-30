from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.security import get_current_active_user
from app.models.user import User
from app.services.minio_service import minio_service
import uuid

router = APIRouter(prefix="/v1/tasks", tags=["Files"], dependencies=[Depends(get_current_active_user)])

@router.post("/{task_id}/upload-avatar")
async def upload_avatar(
    task_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "INVALID_FILE_TYPE", "message": f"File type must be one of: {allowed_types}"}}
        )
    
    file_data = await file.read()
    
    if len(file_data) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail={"error": {"code": "FILE_TOO_LARGE", "message": "File size must be less than 5MB"}}
        )
    
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    object_name = f"{task_id}/{uuid.uuid4()}.{file_extension}"
    
    file_url = minio_service.upload_file(file_data, object_name)
    
    return {"url": file_url, "filename": object_name}