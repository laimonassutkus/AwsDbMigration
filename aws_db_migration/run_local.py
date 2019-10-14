import logging

from typing import Callable, Optional
from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.aws_credentials import AwsCredentials
from aws_db_migration.database_credentials import DatabaseCredentials
from aws_db_migration.invoke_lambda import InvokeLambda
from aws_db_migration.invoke_mysql import InvokeMysql
from aws_db_migration.invoke_s3 import InvokeS3

logr = logging.getLogger(__name__)


class RunLocal:
    def __init__(
            self,
            aws_credentials: AwsCredentials,
            local_database_credentials: DatabaseCredentials,
            backups_bucket: Optional[str] = None,
            lambda_name: Optional[str] = None
    ):
        self.__aws_credentials = aws_credentials
        self.__database_credentials = local_database_credentials
        self.__lambda_name = lambda_name

        self.s3 = InvokeS3(aws_credentials=aws_credentials, bucket_name=backups_bucket)

        # Callbacks to call before/after dumping a local database.
        self.pre_dump: Optional[Callable] = None
        self.post_dump: Optional[Callable] = None

        # Callbacks to call before/after restoring a local database.
        self.pre_restore: Optional[Callable] = None
        self.post_restore: Optional[Callable] = None

        # Callbacks to call before/after uploading a local mysql database dump file to S3.
        self.pre_upload: Optional[Callable] = None
        self.post_upload: Optional[Callable] = None

        # Callbacks to call before/after downloading a cloud mysql database dump file from S3.
        self.pre_download: Optional[Callable] = None
        self.post_download: Optional[Callable] = None

        # Callbacks to call before/after a lambda invocation to execute a mysql restore action against a cloud database.
        self.pre_restore_invoke: Optional[Callable] = None
        self.post_restore_invoke: Optional[Callable] = None

        # Callbacks to call before/after a lambda invocation to execute a mysql dump action against a cloud database.
        self.pre_dump_invoke: Optional[Callable] = None
        self.post_dump_invoke: Optional[Callable] = None

    def to_cloud(self):
        # Create a sql dump file from a local database.
        if self.pre_dump: self.pre_dump()
        logr.info('Creating mysql dump file of a local database...')
        InvokeMysql(self.__database_credentials, ActionEnum.BACKUP, False).run()
        if self.post_dump: self.post_dump()

        # Upload the dump file to S3.
        if self.pre_upload: self.pre_upload()
        logr.info('Uploading dump file to S3...')
        self.s3.upload()
        if self.post_upload: self.post_upload()

        # Restore cloud database from a recently uploaded file.
        if self.pre_restore_invoke: self.pre_restore_invoke()
        logr.info('Restoring cloud database from an uploaded sql dump file...')
        status = InvokeLambda(self.__aws_credentials, ActionEnum.RESTORE, self.__lambda_name).run()
        assert status
        if self.post_restore_invoke: self.post_restore_invoke()

    def from_cloud(self):
        # Ask lambda function to create a sql dump file from a cloud database.
        if self.pre_dump_invoke: self.pre_dump_invoke()
        logr.info('Creating cloud database sql dump file...')
        status = InvokeLambda(self.__aws_credentials, ActionEnum.BACKUP, self.__lambda_name).run()
        assert status
        if self.post_dump_invoke: self.post_dump_invoke()

        # Download the created file from S3.
        if self.pre_download: self.pre_download()
        logr.info('Downloading dump from s3...')
        self.s3.download()
        if self.post_download: self.post_download()

        # Restore the local database from a recently downloaded file.
        if self.pre_restore: self.pre_restore()
        logr.info('Restoring local database...')
        InvokeMysql(self.__database_credentials, ActionEnum.RESTORE, False).run()
        if self.post_restore: self.post_restore()
