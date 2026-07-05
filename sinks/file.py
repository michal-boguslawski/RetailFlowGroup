from infrastructure.minio.service import S3Service
from sinks.base import BaseSink


class FileSink(BaseSink):
    def __init__(self, s3_service: S3Service, naming: FileNamingConfig):
        self.s3_service = s3_service
        self.buffer: dict[str, list[dict]] = {}
        
        open("file.csv", "w", encoding="utf-8-sig")