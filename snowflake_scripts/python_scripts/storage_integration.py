from snowflake_scripts.config.aws_s3_config import S3Settings

settings = S3Settings()
data_path = settings.BUCKET + settings.PATH

use_database = f"""
                    use database {settings.DB_NAME};
                """

create_integration = f"""
                        CREATE STORAGE INTEGRATION {settings.INTEGRATION_NAME}
                            TYPE = EXTERNAL_STAGE
                            STORAGE_PROVIDER = 'S3'
                            ENABLED = TRUE
                            STORAGE_AWS_ROLE_ARN = '{settings.ROLE_ARN}'
                            STORAGE_ALLOWED_LOCATIONS = ('{data_path}');
                    """

grant_create_stage = f"""
                        grant create stage on schema {settings.DB_NAME}.{settings.DB_SCHEMA}
                        to role {settings.USER_ROLE};
                    """

grant_usage = f"""
                grant usage on integration {settings.INTEGRATION_NAME}
                to role {settings.USER_ROLE};
            """


use_schema = f"""
                use schema {settings.DB_NAME}.{settings.DB_SCHEMA};
            """

create_stage = f"""
                    create or replace stage {settings.STAGE_NAME}
                        storage_integration = {settings.INTEGRATION_NAME}
                        url = '{data_path}'
                        file_format = {settings.FILE_FORMAT};
                """

list_stage = f"""
                list @{settings.STAGE_NAME};
            """
