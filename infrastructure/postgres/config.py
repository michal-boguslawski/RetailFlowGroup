from pydantic_settings import BaseSettings, SettingsConfigDict
from infrastructure.config.paths import ENV_PATH


class BasePostgresConfig(BaseSettings):
    host: str = ""
    host_docker: str = ""
    port: int = 5432
    port_docker: int = 5432
    user: str = ""
    password: str = ""
    database: str = ""
    local: bool = True

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def url(self):
        host = self.host if self.local else self.host_docker
        port = self.port if self.local else self.port_docker
        return (
            f"postgresql+psycopg2://"
            f"{self.user}:{self.password}@"
            f"{host}:{port}/{self.database}"
        )

    @property
    def jdbc_url(self):
        host = self.host if self.local else self.host_docker
        port = self.port if self.local else self.port_docker
        return (
            f"jdbc:postgresql://"
            f"{host}:{port}/{self.database}"
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
