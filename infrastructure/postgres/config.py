from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class PostgresConfig(BaseSettings):
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
