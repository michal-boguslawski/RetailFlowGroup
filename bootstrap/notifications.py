# bootstrap/notifications.py
from infrastructure.minio.config import S3Config
from infrastructure.minio.client import MinioClient
from infrastructure.lake.config import lake_config


def initialize_landing_notifications() -> None:
    settings = S3Config()
    minio_client = MinioClient(settings)

    minio_client.set_bucket_kafka_notification(
        bucket=lake_config.landing.bucket,
        queue_arn="arn:minio:sqs::LANDING_EVENTS:kafka",  # must match target registered in docker-compose
        events=["s3:ObjectCreated:*"],
    )


if __name__ == "__main__":
    initialize_landing_notifications()
