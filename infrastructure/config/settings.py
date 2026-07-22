from pydantic_settings import BaseSettings, SettingsConfigDict
from .paths import ENV_PATH


class SparkSettings(BaseSettings):
    master_url: str = ""

    model_config = SettingsConfigDict(
        env_prefix="SPARK_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
