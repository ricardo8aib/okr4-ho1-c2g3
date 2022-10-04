from typing import List

import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
from config.db_settings import DBSettings


class DatabaseGateway:
    def __init__(self, settings: DBSettings) -> None:
        self.db_name = settings.DATABASE_NAME
        self.user = settings.DATABASE_USERNAME
        self.password = settings.DATABASE_PASSWORD.get_secret_value()
        self.host = settings.DATABASE_HOST
        self.port = settings.DATABASE_PORT

        self.connection = psycopg2.connect(
            database=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def get_from_table(self, table_name: str) -> List:
        with self.connection.cursor() as cursor:
            statement = f"SELECT * FROM {table_name} limit 10"
            cursor.execute(statement)
            result = cursor.fetchall()

            return result

    def get_df_from_table(self, table_name: str) -> pd.DataFrame:
        statement = f"SELECT * FROM {table_name} limit 10"
        df = sqlio.read_sql_query(statement, self.connection)
        return df
