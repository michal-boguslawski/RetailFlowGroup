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


class MongoDBSettings(BaseSettings):
    host: str = "localhost"
    user: str = ""
    password: str = ""
    database: str = ""
    port: int = 27017

    model_config = SettingsConfigDict(
        env_prefix="MONGODB_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def uri(self) -> str:
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/"


class S3Settings(BaseSettings):
    endpoint_url: str = ""
    access_key: str = ""
    secret_key: str = ""
    region_name: str = "us-east-1"
    secure: bool = True

    model_config = SettingsConfigDict(
        env_prefix="S3_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
