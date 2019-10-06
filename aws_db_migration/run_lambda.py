import logging

from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.exe_enum import MysqlDumpExeEnum, MysqlExeEnum
from aws_db_migration.mysql_action import execute_mysql_action
from aws_db_migration.s3 import S3

logr = logging.getLogger(__name__)


class RunLambda:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.s3 = S3()

        self.__event_type = ActionEnum[event['type']]

    def run(self):
        if self.__event_type == ActionEnum.BACKUP:
            execute_mysql_action(MysqlDumpExeEnum.SERVER_MYSQL_DUMP)
            self.s3.upload()
        elif self.__event_type == ActionEnum.RESTORE:
            self.s3.download()
            execute_mysql_action(MysqlExeEnum.SERVER_MYSQL)
        else:
            raise ValueError('Unsupported event type.')
