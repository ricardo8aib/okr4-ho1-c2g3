from snowflake_scripts.config.aws_s3_config import S3Settings

settings = S3Settings()

create_file_format = f"""
                    CREATE FILE FORMAT "OLIST"."STAGING".{settings.FILE_FORMAT}
                    TYPE = 'CSV'
                    COMPRESSION = 'AUTO'
                    FIELD_DELIMITER = ','
                    RECORD_DELIMITER = '\n'
                    SKIP_HEADER = 1
                    FIELD_OPTIONALLY_ENCLOSED_BY = 'NONE'
                    TRIM_SPACE = FALSE
                    ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE
                    ESCAPE = 'NONE'
                """

create_customers = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_CUSTOMERS_DATASET (
                        customer_id varchar(40),
                        customer_unique_id varchar(40),
                        customer_zip_code_prefix varchar(40),
                        customer_city varchar(40),
                        customer_state varchar(40)
                    );
                """

create_geolocation = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_GEOLOCATION_DATASET (
                        geolocation_zip_code_prefix varchar(40),
                        geolocation_lat float,
                        geolocation_lng float,
                        geolocation_city varchar(40),
                        geolocation_state varchar(40)
                    );
                """


create_order_items = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_ORDER_ITEMS_DATASET (
                        order_id varchar(40),
                        order_item_id integer,
                        product_id varchar(40),
                        seller_id varchar(40),
                        shipping_limit_date date,
                        price float,
                        freight_value float
                    );
                """

create_order_payments = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_ORDER_PAYMENTS_DATASET (
                        order_id varchar(40),
                        payment_sequential integer,
                        payment_type varchar(40),
                        payment_installments integer,
                        payment_value float
                    );
                """

create_order_reviews = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_ORDER_REVIEWS_DATASET (
                        review_id varchar(40),
                        order_id varchar(40),
                        review_score integer,
                        review_comment_title varchar(40),
                        review_comment_message varchar(500),
                        review_creation_date date,
                        review_answer_timestamp date
                    );
                """

create_order = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_ORDER_DATASET (
                        order_id varchar(40),
                        customer_id varchar(40),
                        order_status varchar(40),
                        order_purchase_timestamp date,
                        order_approved_at date,
                        order_delivered_carrier_date date,
                        order_delivered_customer_date date,
                        order_estimated_delivery_date date
                    );
                """

create_products = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_PRODUCTS_DATASET (
                        product_id varchar(40),
                        product_category_name varchar(40),
                        product_name_lenght integer,
                        product_description_lenght integer,
                        product_photos_qty integer,
                        product_weight_g integer,
                        product_length_cm integer,
                        product_height_cm integer,
                        product_width_cm integer
                    );
                """

create_sellers = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.OLIST_SELLERS_DATASET (
                        seller_id varchar(40),
                        seller_zip_code_prefix varchar(40),
                        seller_city varchar(40),
                        seller_state varchar(40)
                    );
                """

create_name_translation = """
                    CREATE OR REPLACE TABLE OLIST.STAGING.PRODUCT_CATEGORY_NAME_TRANSLATION (
                        product_category_name varchar(40),
                        product_category_name_english varchar(40)
                    );
                """

copy_customers = """
                    COPY INTO OLIST.STAGING.OLIST_CUSTOMERS_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_customers_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_geolocation = """
                    COPY INTO OLIST.STAGING.OLIST_GEOLOCATION_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_geolocation_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_order_items = """
                    COPY INTO OLIST.STAGING.OLIST_ORDER_ITEMS_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_order_items_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_order_payments = """
                    COPY INTO OLIST.STAGING.OLIST_ORDER_PAYMENTS_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_order_payments_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_order_reviews = """
                    COPY INTO OLIST.STAGING.OLIST_ORDER_REVIEWS_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_order_reviews_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_order = """
                    COPY INTO OLIST.STAGING.OLIST_ORDER_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_orders_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_products = """
                    COPY INTO OLIST.STAGING.OLIST_PRODUCTS_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_products_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_sellers = """
                    COPY INTO OLIST.STAGING.OLIST_SELLERS_DATASET
                    FROM @my_s3_stage
                    FILES = ('olist_sellers_dataset.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """

copy_sname_translation = """
                    COPY INTO OLIST.STAGING.PRODUCT_CATEGORY_NAME_TRANSLATION
                    FROM @my_s3_stage
                    FILES = ('product_category_name_translation.csv')
                    FILE_FORMAT = (format_name='olist_tables_csv' );
                """
