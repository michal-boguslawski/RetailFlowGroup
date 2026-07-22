from boto3 import client
from botocore.client import BaseClient

from infrastructure.minio.config import S3Config


class MinioClient:
    def __init__(
        self,
        minio_settings: S3Config | None = None,
    ):
        settings = minio_settings or S3Config()

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

    def set_bucket_kafka_notification(
        self,
        *,
        bucket: str,
        queue_arn: str,
        events: list[str],
        config_id: str = "landing-events",
    ) -> None:
        """Attach a Kafka notification target to a bucket.

        `queue_arn` must already be registered server-side (e.g. via
        docker-compose MINIO_NOTIFY_KAFKA_* env vars) — this call only
        wires the bucket to an existing target, it does not create one.
        """
        print(f"Setting bucket {bucket} notification config to ARN {queue_arn}")
        print(self._client.put_bucket_notification_configuration(
            Bucket=bucket,
            NotificationConfiguration={
                "QueueConfigurations": [
                    {
                        "Id": config_id,
                        "QueueArn": queue_arn,
                        "Events": events,
                    }
                ]
            },
        ))
