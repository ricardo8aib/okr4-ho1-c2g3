import sys
from pathlib import Path

import snowflake.connector
from config.snowflake_config import SnowflakeSettings

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from snowflake_scripts.python_scripts.load_from_stage import (
    create_customers, create_geolocation, create_name_translation,
    create_order, create_order_items, create_order_payments,
    create_order_reviews, create_products, create_sellers)

settings = SnowflakeSettings()

connection = snowflake.connector.connect(
    user=settings.SNOWFLAKE_USER,
    password=settings.SNOWFLAKE_PASSWORD.get_secret_value(),
    account=settings.SNOWFLAKE_ACCOUNT,
)

with connection.cursor() as cursor:
    cursor = connection.cursor()
    try:
        cursor.execute(create_customers)
        cursor.execute(create_geolocation)
        cursor.execute(create_name_translation)
        cursor.execute(create_order)
        cursor.execute(create_order_items)
        cursor.execute(create_order_payments)
        cursor.execute(create_order_reviews)
        cursor.execute(create_products)
        cursor.execute(create_sellers)
    except Exception as e:
        print(e)

connection.close()
