from io import BytesIO
from botocore.client import BaseClient
from botocore.exceptions import ClientError


class S3Service:
    def __init__(self, s3_client: BaseClient):
        self._client = s3_client

    def upload_bytes(
        self,
        bucket: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        self._client.put_object(
            Bucket=bucket,
            Key=object_name,
            Body=data,
            ContentType=content_type,
        )

    def upload_file(
        self,
        bucket: str,
        object_name: str,
        filename: str,
    ) -> None:
        self._client.upload_file(
            Filename=filename,
            Bucket=bucket,
            Key=object_name,
        )

    def upload_stream(
        self,
        bucket: str,
        object_name: str,
        stream: BytesIO,
        content_type: str = "application/octet-stream",
    ) -> None:
        self._client.upload_fileobj(
            Fileobj=stream,
            Bucket=bucket,
            Key=object_name,
            ExtraArgs={"ContentType": content_type},
        )

    def download_bytes(
        self,
        bucket: str,
        object_name: str,
    ) -> bytes:
        response = self._client.get_object(
            Bucket=bucket,
            Key=object_name,
        )

        return response["Body"].read()

    def delete_object(
        self,
        bucket: str,
        object_name: str,
    ) -> None:
        self._client.delete_object(
            Bucket=bucket,
            Key=object_name,
        )

    def object_exists(
        self,
        bucket: str,
        object_name: str,
    ) -> bool:
        try:
            self._client.head_object(
                Bucket=bucket,
                Key=object_name,
            )
            return True
        except self._client.exceptions.ClientError:
            return False

    def bucket_exists(self, bucket: str) -> bool:
        try:
            self._client.head_bucket(Bucket=bucket)
            return True
        except ClientError:
            return False

    def create_bucket(self, bucket: str) -> None:
        if not self.bucket_exists(bucket):
            self._client.create_bucket(Bucket=bucket)
