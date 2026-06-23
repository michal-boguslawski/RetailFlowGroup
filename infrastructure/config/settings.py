from pydantic_settings import BaseSettings, SettingsConfigDict
from .paths import ENV_PATH


class PostgresSettings(BaseSettings):
    host: str = ""
    port: int = 5432
    user: str = ""
    password: str = ""
    database: str = ""
    
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = ""
    schema_registry_url: str = ""

    model_config = SettingsConfigDict(
        env_prefix="KAFKA_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
