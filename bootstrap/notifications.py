# bootstrap/notifications.py
from infrastructure.config.settings import S3Settings
from infrastructure.minio.client import MinioClient
from config.loader import load_lake_config


def initialize_landing_notifications() -> None:
    settings = S3Settings()
    lake_config = load_lake_config()
    minio_client = MinioClient(settings)

    minio_client.set_bucket_kafka_notification(
        bucket=lake_config.landing.bucket,
        queue_arn="arn:minio:sqs::LANDING_EVENTS:kafka",  # must match target registered in docker-compose
        events=["s3:ObjectCreated:*"],
    )


if __name__ == "__main__":
    initialize_landing_notifications()
