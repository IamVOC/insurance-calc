from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


class KafkaConfig(BaseSettings):
    HOST: str
    PORT: int
    TOPIC: str

    @property
    def BOOTSTRAP_SERVER(self) -> str:
        return f"{self.HOST}:{self.PORT}"


class DBConfig(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str

    @property
    def URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.USER}:{self.PASS}@{self.HOST}:"
            f"{self.PORT}/{self.NAME}"
        )


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="_", env_file=".env", env_file_encoding="utf-8"
    )

    ENVIRONMENT: Environment = Environment.production

    DB: DBConfig
    KAFKA: KafkaConfig


settings = Config()
