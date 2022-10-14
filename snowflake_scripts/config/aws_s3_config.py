import os

import pydantic


class S3Settings(pydantic.BaseSettings):
    INTEGRATION_NAME: str
    ROLE_ARN: str
    BUCKET: str
    PATH: str
    DB_NAME: str
    DB_SCHEMA: str
    USER_ROLE: str
    FILE_FORMAT: str
    STAGE_NAME: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"
