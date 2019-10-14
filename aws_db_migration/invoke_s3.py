import datetime
import logging
import os
import shutil
import boto3

from typing import Tuple, Optional, List

from aws_db_migration.aws_credentials import AwsCredentials
from aws_db_migration.invoke_mysql import InvokeMysql

logr = logging.getLogger(__name__)


class InvokeS3:
    def __init__(self, aws_credentials: AwsCredentials, bucket_name: Optional[str] = None):
        self.__bucket = bucket_name or os.environ['AWS_DB_MIGRATION_BACKUPS_S3']

        self.__resource = boto3.resource(
            's3',
            region_name=aws_credentials.region,
            aws_access_key_id=aws_credentials.access_key,
            aws_secret_access_key=aws_credentials.secret_key
        )

    def upload(self):
        self.__resource.meta.client.upload_file(InvokeMysql.PATH_TO_SQL_FILE, self.__bucket, self.__gen_name())

    def download(self) -> None:
        """
        Downloads latest mysql dump from S3.

        :return: No return.
        """
        response = self.__resource.meta.client.list_objects(Bucket=self.__bucket)

        # Get all contents in the bucket.
        contents = response.get('Contents')
        if not contents:
            raise ValueError('Provided bucket is empty!')

        # Extract timestamp from the name.
        keys_with_times = self.__convert([content['Key'] for content in contents])
        if len(keys_with_times) == 0:
            raise ValueError('No object found that follow appropriate naming conventions.')

        latest_key, latest_timestamp = max(keys_with_times, key=lambda item: item[1])

        logr.info(f'Latest key: {latest_key}.')
        logr.info(f'Latest timestamp: {latest_timestamp}.')

        self.__clear_and_create()

        self.__resource.meta.client.download_file(self.__bucket, latest_key, InvokeMysql.PATH_TO_SQL_FILE)

    @staticmethod
    def __convert(keys: List[str]) -> List[Tuple[str, int]]:
        """
        Converts a list of keys to list of keys with corresponding timestamps.

        :param keys: A list of object names (S3 keys).

        :return: A list of tuples where:
            1. First value is an original key.
            2. Second value is a timestamp extracted from the key.
        """
        keys_with_timestamps = []
        for key in keys:
            try:
                keys_with_timestamps.append((key, int(key.split('_')[1].split('.')[0])))
            except (IndexError, ValueError):
                continue

        return keys_with_timestamps

    @staticmethod
    def __gen_name() -> str:
        """
        Generates a name with a timestamp.

        :return: String.
        """
        now = int(datetime.datetime.now().timestamp())
        return f'dump_{now}.sql'

    @staticmethod
    def __clear_and_create():
        # Clear directory from previous dump files.
        try:
            shutil.rmtree(InvokeMysql.PATH_TO_SQL_DIR)
        except FileNotFoundError:
            pass

        # Create a directory for dump file if it does not exist.
        if not os.path.exists(InvokeMysql.PATH_TO_SQL_DIR):
            os.makedirs(InvokeMysql.PATH_TO_SQL_DIR)
