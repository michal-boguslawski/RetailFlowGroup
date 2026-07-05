from boto3 import client
from botocore.client import BaseClient


class MinioClient:
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        region_name: str = "us-east-1",
        secure: bool = True,
    ):
        protocol = "https" if secure else "http"

        if endpoint_url.startswith("http"):
            url = endpoint_url
        else:
            url = f"{protocol}://{endpoint_url}"

        self._client: BaseClient = client(
            "s3",
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region_name,
        )

    @property
    def client(self) -> BaseClient:
        return self._client
