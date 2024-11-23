from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


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
    model_config = SettingsConfigDict(env_nested_delimiter="_")

    ENVIRONMENT: Environment = Environment.production

    DB: DBConfig


settings = Config()
