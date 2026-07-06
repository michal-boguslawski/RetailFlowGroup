from boto3 import client
from botocore.client import BaseClient

from infrastructure.config.settings import S3Settings


class MinioClient:
    def __init__(
        self,
        minio_settings: S3Settings | None = None,
    ):
        settings = minio_settings or S3Settings()

        protocol = "https" if settings.secure else "http"

        if settings.endpoint_url.startswith("http"):
            url = settings.endpoint_url
        else:
            url = f"{protocol}://{settings.endpoint_url}"

        self._client: BaseClient = client(
            "s3",
            endpoint_url=url,
            aws_access_key_id=settings.access_key,
            aws_secret_access_key=settings.secret_key,
            region_name=settings.region_name,
        )

    @property
    def client(self) -> BaseClient:
        return self._client
