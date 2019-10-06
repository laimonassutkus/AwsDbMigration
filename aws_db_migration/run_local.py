import logging

from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.exe_enum import MysqlDumpExeEnum, MysqlExeEnum
from aws_db_migration.mysql_action import execute_mysql_action
from aws_db_migration.s3 import S3

logr = logging.getLogger(__name__)


class RunLocal:
    def __init__(self, event_type: ActionEnum):
        self.s3 = S3()
        self.__event_type = event_type

    def run(self):
        if self.__event_type == ActionEnum.BACKUP:
            execute_mysql_action(MysqlDumpExeEnum.LOCAL_MYSQL_DUMP)
            self.s3.upload()
        elif self.__event_type == ActionEnum.RESTORE:
            self.s3.download()
            execute_mysql_action(MysqlExeEnum.LOCAL_MYSQL)
        else:
            raise ValueError('Unsupported event type.')
