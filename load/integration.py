import sys
from pathlib import Path

import snowflake.connector
from config.snowflake_config import SnowflakeSettings

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from snowflake_scripts.python_scripts.storage_integration import (
    create_integration,
    use_database
)


def create_storage_integration(settings: SnowflakeSettings):
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
            cursor.execute(use_database)
            cursor.execute(create_integration)
        except Exception as e:
            print(e)

    connection.close()


if __name__ == "__main__":
    snowflake_settings = SnowflakeSettings()
    create_storage_integration(snowflake_settings)
