import os

import pydantic


class AWSSettings(pydantic.BaseSettings):
    AWS_PROFILE: str
    BUCKET: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"
