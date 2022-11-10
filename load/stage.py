import sys
from pathlib import Path

import snowflake.connector
from config.snowflake_config import SnowflakeSettings

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from snowflake_scripts.python_scripts.storage_integration import (
    create_integration, create_stage, grant_create_stage, grant_usage,
    list_stage, use_database, use_schema)


def create_stage_func(settings: SnowflakeSettings):
    """Create the storage integration

    Args:
        settings (SnowflakeSettings): Snowflake settings object
    """

    connection = snowflake.connector.connect(
        user=settings.SNOWFLAKE_USER,
        password=settings.SNOWFLAKE_PASSWORD.get_secret_value(),
        account=settings.SNOWFLAKE_ACCOUNT,
    )

    with connection.cursor() as cursor:
        cursor = connection.cursor()
        try:
            cursor.execute(grant_create_stage)
            cursor.execute(grant_usage)
            cursor.execute(use_schema)
            cursor.execute(create_stage)
            cursor.execute(list_stage)
        except Exception as e:
            print(e)

    connection.close()


if __name__ == "__main__":
    snowflake_settings = SnowflakeSettings()
    create_stage_func(snowflake_settings)
