import logging
import os

from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.exe_enum import MysqlDumpExeEnum, MysqlExeEnum
from aws_db_migration.invoke_lambda import InvokeLambda
from aws_db_migration.mysql_action import execute_mysql_action
from aws_db_migration.s3 import S3

logr = logging.getLogger(__name__)


class RunLocal:
    def __init__(self, event_type: ActionEnum):
        self.__event_type = event_type

        key = os.environ.get('AWS_DB_MIGRATION_AWS_KEY')
        secret = os.environ.get('AWS_DB_MIGRATION_AWS_SECRET')

        if key and secret:
            self.__key_secret_pair = (key, secret)
        else:
            self.__key_secret_pair = None

        self.s3 = S3(key_secret=self.__key_secret_pair)

    def run(self):
        # Request to create a backup of a local database.
        if self.__event_type == ActionEnum.BACKUP:
            # Create a sql dump file from a local database.
            logr.info('Creating mysql dump file of a local database...')
            execute_mysql_action(MysqlDumpExeEnum.LOCAL_MYSQL_DUMP)
            # Upload the dump file to S3.
            logr.info('Uploading dump file to S3...')
            self.s3.upload()
            # Restore cloud database from a recently uploaded file.
            logr.info('Restoring cloud database from an uploaded sql dump file...')
            InvokeLambda(ActionEnum.RESTORE, key_secret=self.__key_secret_pair).run()

            logr.info('Success!')
        # Request to restore a local database from a file.
        elif self.__event_type == ActionEnum.RESTORE:
            # Ask lambda function to create a sql dump file from a cloud database.
            logr.info('Creating cloud database sql dump file...')
            InvokeLambda(ActionEnum.BACKUP, key_secret=self.__key_secret_pair).run()
            # Download the created file from S3.
            logr.info('Downloading dump from s3...')
            self.s3.download()
            # Restore the local database from a recently downloaded file.
            logr.info('Restoring local database...')
            execute_mysql_action(MysqlExeEnum.LOCAL_MYSQL)

            logr.info('Success!')
        else:
            raise ValueError('Unsupported event type.')
