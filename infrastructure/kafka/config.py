from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class KafkaConfig(BaseSettings):
    bootstrap_servers: str = ""
    schema_registry_url: str = ""
    bootstrap_servers_docker: str = ""

    model_config = SettingsConfigDict(
        env_prefix="KAFKA_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
