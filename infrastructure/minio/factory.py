from infrastructure.config.settings import S3Settings
from infrastructure.minio.client import MinioClient
from infrastructure.minio.service import S3Service


def build_minio_service(
    minio_settings: S3Settings | None = None,
) -> S3Service:
    settings = minio_settings or S3Settings()
    client = MinioClient(
        endpoint_url=settings.endpoint_url,
        access_key=settings.access_key,
        secret_key=settings.secret_key,
        region_name=settings.region_name,
        secure=settings.secure,
    )

    return S3Service(client.client)
