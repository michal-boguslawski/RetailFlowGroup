from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class MongoDBConfig(BaseSettings):
    host: str = "localhost"
    host_docker: str = ""
    user: str = ""
    password: str = ""
    database: str = ""
    port: int = 27017
    port_docker: int = 27017
    local: bool = True

    model_config = SettingsConfigDict(
        env_prefix="MONGODB_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def uri(self) -> str:
        host = self.host if self.local else self.host_docker
        port = self.port if self.local else self.port_docker
        return f"mongodb://{self.user}:{self.password}@{host}:{port}/"
