from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class S3Config(BaseSettings):
    endpoint_url: str = ""
    access_key: str = ""
    secret_key: str = ""
    region_name: str = "us-east-1"
    secure: bool = True
    endpoint_docker: str = ""

    model_config = SettingsConfigDict(
        env_prefix="S3_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
