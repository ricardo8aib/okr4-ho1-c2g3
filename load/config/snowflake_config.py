import os

import pydantic


class SnowflakeSettings(pydantic.BaseSettings):
    SNOWFLAKE_USER: str
    SNOWFLAKE_PASSWORD: pydantic.SecretStr
    SNOWFLAKE_ACCOUNT: str
    FILE_FORMAT: str
    SNOWFLAKE_WAREHOUSE: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"
