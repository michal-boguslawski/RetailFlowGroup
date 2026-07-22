from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class MongoDBConfig(BaseSettings):
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
