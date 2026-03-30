from minio import Minio
from minio.error import S3Error
from app.config.settings import settings
import io

class MinIOService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
    
    def init_bucket(self):
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET):
                self.client.make_bucket(settings.MINIO_BUCKET)
        except S3Error as e:
            print(f"Error creating bucket: {e}")
    
    def upload_file(self, file_data: bytes, object_name: str) -> str:
        try:
            self.client.put_object(
                settings.MINIO_BUCKET,
                object_name,
                io.BytesIO(file_data),
                len(file_data)
            )
            return f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{object_name}"
        except S3Error as e:
            raise Exception(f"Error uploading file: {e}")
    
    def check_connection(self) -> bool:
        try:
            self.client.list_buckets()
            return True
        except S3Error:
            return False

minio_service = MinIOService()