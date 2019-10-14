import logging
import os
import shutil
import subprocess

from aws_db_migration import root
from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.database_credentials import DatabaseCredentials

logr = logging.getLogger(__name__)


class InvokeMysql:
    PATH_TO_SQL_DIR = '/tmp/aws-db-migration/mysql/'
    PATH_TO_SQL_FILE = f'{PATH_TO_SQL_DIR}dump.sql'

    SCRIPTS_MAP = {
        ActionEnum.BACKUP: {
            True: 'mysql_cloud_dump.sh',
            False: 'mysql_local_dump.sh',
        },
        ActionEnum.RESTORE: {
            True: 'mysql_cloud_restore.sh',
            False: 'mysql_local_restore.sh',
        }
    }

    def __init__(self, credentials: DatabaseCredentials, action_type: ActionEnum, is_cloud: bool = False):
        self.credentials = credentials
        self.action_type = action_type
        self.is_cloud = is_cloud

    def run(self):
        """
        Executes mysql (mysql or mysqldump) action depending on provided enum value.

        :return: No return.
        """
        if self.action_type == ActionEnum.RESTORE:
            self.__assert_file()
        elif self.action_type == ActionEnum.BACKUP:
            self.__clear_and_create()
        else:
            raise ValueError('Unsupported mysql execute enum type.')

        args = [
            self.credentials.username,
            self.credentials.password,
            self.credentials.database_name,
            self.credentials.host,
            self.credentials.port,
            self.PATH_TO_SQL_FILE,
        ]

        script = self.SCRIPTS_MAP[self.action_type][self.is_cloud]

        try:
            output = subprocess.check_output([f'{root}/{script}', *args], stderr=subprocess.STDOUT)
            logr.info(output.decode())
        except subprocess.CalledProcessError as ex:
            logr.error(ex.output.decode())
            raise

    @staticmethod
    def __assert_file():
        if not os.path.isfile(InvokeMysql.PATH_TO_SQL_FILE):
            raise ValueError('Can not initiate restore action. Sql dump file is missing.')

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
