from infrastructure.config.settings import S3Settings
from infrastructure.minio.client import MinioClient
from infrastructure.minio.service import S3Service


def build_minio_service(
    minio_settings: S3Settings | None = None,
) -> S3Service:
    settings = minio_settings or S3Settings()
    client = MinioClient(
        minio_settings=settings
    )

    return S3Service(client.client)
