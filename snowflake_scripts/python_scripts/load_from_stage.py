from snowflake_scripts.config.aws_s3_config import S3Settings

settings = S3Settings()

create_file_format = f"""
                    CREATE FILE FORMAT
                    "{settings.DB_NAME}"."{settings.DB_SCHEMA}".{settings.FILE_FORMAT}
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

create_customers = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_CUSTOMERS_DATASET (
                        customer_id varchar(40),
                        customer_unique_id varchar(40),
                        customer_zip_code_prefix varchar(40),
                        customer_city varchar(40),
                        customer_state varchar(40)
                    );
                """

create_geolocation = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_GEOLOCATION_DATASET (
                        geolocation_zip_code_prefix varchar(40),
                        geolocation_lat float,
                        geolocation_lng float,
                        geolocation_city varchar(40),
                        geolocation_state varchar(40)
                    );
                """


create_order_items = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_ITEMS_DATASET (
                        order_id varchar(40),
                        order_item_id integer,
                        product_id varchar(40),
                        seller_id varchar(40),
                        shipping_limit_date date,
                        price float,
                        freight_value float
                    );
                """

create_order_payments = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_PAYMENTS_DATASET (
                        order_id varchar(40),
                        payment_sequential integer,
                        payment_type varchar(40),
                        payment_installments integer,
                        payment_value float
                    );
                """

create_order_reviews = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_REVIEWS_DATASET (
                        review_id varchar(40),
                        order_id varchar(40),
                        review_score integer,
                        review_comment_title varchar(40),
                        review_comment_message varchar(500),
                        review_creation_date date,
                        review_answer_timestamp date
                    );
                """

create_order = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_DATASET (
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

create_products = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_PRODUCTS_DATASET (
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

create_sellers = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_SELLERS_DATASET (
                        seller_id varchar(40),
                        seller_zip_code_prefix varchar(40),
                        seller_city varchar(40),
                        seller_state varchar(40)
                    );
                """

create_name_translation = f"""
                    CREATE OR REPLACE TABLE
                    {settings.DB_NAME}.{settings.DB_SCHEMA}.PRODUCT_CATEGORY_NAME_TRANSLATION (
                        product_category_name varchar(40),
                        product_category_name_english varchar(40)
                    );
                """

copy_customers = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_CUSTOMERS_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_customers_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_geolocation = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_GEOLOCATION_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_geolocation_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_order_items = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_ITEMS_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_order_items_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_order_payments = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_PAYMENTS_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_order_payments_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_order_reviews = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_REVIEWS_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_order_reviews_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_order = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_ORDER_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_orders_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_products = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_PRODUCTS_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_products_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_sellers = f"""
                    COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_SELLERS_DATASET
                    FROM @{settings.STAGE_NAME}
                    FILES = ('olist_sellers_dataset.csv')
                    FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """

copy_sname_translation = f"""
                COPY INTO {settings.DB_NAME}.{settings.DB_SCHEMA}.PRODUCT_CATEGORY_NAME_TRANSLATION
                FROM @{settings.STAGE_NAME}
                FILES = ('product_category_name_translation.csv')
                FILE_FORMAT = (format_name='{settings.FILE_FORMAT}' );
                """


create_snowpipe_customers = f"""
    create or replace pipe {settings.DB_NAME}.{settings.DB_SCHEMA}.customers_pipe
    auto_ingest=true as
    copy into {settings.DB_NAME}.{settings.DB_SCHEMA}.OLIST_CUSTOMERS_DATASET
    from @{settings.DB_NAME}.{settings.DB_SCHEMA}.{settings.STAGE_NAME}/raw/olist_customers_dataset/
    file_format = (type='CSV' SKIP_HEADER=1);
"""
