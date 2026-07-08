from config.loader import load_lake_config
from infrastructure.minio.client import MinioClient
from infrastructure.minio.service import S3Service


def init_minio_buckets():
    client = MinioClient()
    service = S3Service(client.client)

    lake_config = load_lake_config()

    for _, layer in lake_config:
        bucket = layer.bucket
        if bucket and not service.bucket_exists(bucket):
            service.create_bucket(bucket)
            print(f"Created bucket: {bucket}")


if __name__ == "__main__":
    init_minio_buckets()
