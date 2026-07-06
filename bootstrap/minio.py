from argparse import ArgumentParser

from config.loader import load_config
from domain.enums import StoreId
from infrastructure.minio.client import MinioClient
from infrastructure.minio.service import S3Service


def init_minio_buckets(store_id: StoreId):
    config = load_config(store_id)
    client = MinioClient()
    service = S3Service(client.client)

    bucket = config.minio_bucket_name
    if bucket and not service.bucket_exists(bucket):
        service.create_bucket(bucket)

def parse_args():
    parser = ArgumentParser(
        description="Reset Kafka topics for a store."
    )

    parser.add_argument(
        "--store-id",
        required=True,
        choices=[store.value for store in StoreId],
        help="Store identifier",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    init_minio_buckets(StoreId(args.store_id))
