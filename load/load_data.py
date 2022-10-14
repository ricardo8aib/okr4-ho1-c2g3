import sys
from pathlib import Path

import snowflake.connector
from config.snowflake_config import SnowflakeSettings

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from snowflake_scripts.python_scripts.load_from_stage import (
    copy_customers, copy_geolocation, copy_order, copy_order_items,
    copy_order_payments, copy_order_reviews, copy_products, copy_sellers,
    copy_sname_translation)
from snowflake_scripts.python_scripts.storage_integration import (
    grant_create_stage, grant_usage, use_database, use_schema)

settings = SnowflakeSettings()

connection = snowflake.connector.connect(
    user=settings.SNOWFLAKE_USER,
    password=settings.SNOWFLAKE_PASSWORD.get_secret_value(),
    account=settings.SNOWFLAKE_ACCOUNT,
)

with connection.cursor() as cursor:
    cursor = connection.cursor()
    try:
        cursor.execute(f"USE WAREHOUSE {settings.SNOWFLAKE_WAREHOUSE}")
        cursor.execute(use_database)
        cursor.execute(grant_create_stage)
        cursor.execute(grant_usage)
        cursor.execute(use_schema)

        cursor.execute(copy_customers)
        cursor.execute(copy_geolocation)
        cursor.execute(copy_order_items)
        cursor.execute(copy_order_payments)
        cursor.execute(copy_order_reviews)
        cursor.execute(copy_order)
        cursor.execute(copy_products)
        cursor.execute(copy_sellers)
        cursor.execute(copy_sname_translation)
    except Exception as e:
        print(e)

connection.close()
