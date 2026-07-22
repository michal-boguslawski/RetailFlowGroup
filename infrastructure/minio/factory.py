from infrastructure.minio.config import S3Config
from infrastructure.minio.client import MinioClient
from infrastructure.minio.service import S3Service


def build_minio_service(
    minio_settings: S3Config | None = None,
) -> S3Service:
    settings = minio_settings or S3Config()
    client = MinioClient(
        minio_settings=settings
    )

    return S3Service(client.client)
