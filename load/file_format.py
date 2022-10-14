import sys
from pathlib import Path

import snowflake.connector
from config.snowflake_config import SnowflakeSettings

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from snowflake_scripts.python_scripts.load_from_stage import create_file_format

settings = SnowflakeSettings()

connection = snowflake.connector.connect(
    user=settings.SNOWFLAKE_USER,
    password=settings.SNOWFLAKE_PASSWORD.get_secret_value(),
    account=settings.SNOWFLAKE_ACCOUNT,
)

with connection.cursor() as cursor:
    cursor = connection.cursor()
    try:
        cursor.execute(create_file_format)
    except Exception as e:
        print(e)

connection.close()
