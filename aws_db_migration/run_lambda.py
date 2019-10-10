import logging

from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.database_credentials import DatabaseCredentials
from aws_db_migration.invoke_mysql import InvokeMysql
from aws_db_migration.invoke_s3 import InvokeS3

logr = logging.getLogger(__name__)


class RunLambda:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.s3 = InvokeS3()

        self.__event_type = ActionEnum[event['type']]
        self.__database_credentials = DatabaseCredentials()

    def run(self):
        if self.__event_type == ActionEnum.BACKUP:
            # Create a cloud database dump file...
            InvokeMysql(self.__database_credentials, ActionEnum.BACKUP, True).run()

            # ...and upload it to S3.
            self.s3.upload()
        elif self.__event_type == ActionEnum.RESTORE:
            # Download a database dump file from s3...
            self.s3.download()
            # ...and restore the could database from it.
            InvokeMysql(self.__database_credentials, ActionEnum.RESTORE, True).run()
        else:
            raise ValueError('Unsupported event type.')
