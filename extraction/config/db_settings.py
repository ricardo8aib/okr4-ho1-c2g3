import os

import pydantic


class DBSettings(pydantic.BaseSettings):
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: pydantic.SecretStr
    DATABASE_HOST: str
    DATABASE_PORT: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"
