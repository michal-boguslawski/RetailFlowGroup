from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class BasePostgresConfig(BaseSettings):
    host: str =""
    port: int = 5432
    user: str = ""
    password: str = ""
    database: str = ""

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def url(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


class AlphaPostgresConfig(BasePostgresConfig):
    model_config = SettingsConfigDict(
        env_prefix="ALPHA_POSTGRES_"
    )


class ControlPostgresConfig(BasePostgresConfig):
    model_config = SettingsConfigDict(
        env_prefix="CONTROL_POSTGRES_"
    )


if __name__ == "__main__":
    config = AlphaPostgresConfig()
    print(config)
