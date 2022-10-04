import warnings

from config.aws_settings import AWSSettings
from config.db_settings import DBSettings
from db_gateway import DatabaseGateway
from utils import Loader

warnings.filterwarnings("ignore", category=UserWarning)

db_settings = DBSettings()
aws_settings = AWSSettings()

db = DatabaseGateway(db_settings)
loader = Loader(aws_settings)

if __name__ == "__main__":

    tables = [
        "olist_customers_dataset",
        "olist_geolocation_dataset",
        "olist_order_items_dataset",
        "olist_order_payments_dataset",
        "olist_order_reviews_dataset",
        "olist_orders_dataset",
        "olist_products_dataset",
        "olist_sellers_dataset",
    ]

    for table in tables:
        results = db.get_df_from_table(table)
        path = f"staging/{table}.csv"
        loader.load_data(results, path)
