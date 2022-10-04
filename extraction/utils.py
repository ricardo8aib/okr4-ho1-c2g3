from io import StringIO

import boto3
import pandas as pd
from config.aws_settings import AWSSettings


class Loader:
    def __init__(self, settings: AWSSettings) -> None:
        self.profile = settings.AWS_PROFILE
        self.bucket = settings.BUCKET
        self.session = boto3.Session(profile_name=self.profile)
        self.s3_resource = self.session.resource("s3")

    def load_data(self, df: pd.DataFrame, path: str) -> None:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        self.s3_resource.Object(self.bucket, path).put(Body=csv_buffer.getvalue())
