import logging
import os
import shutil
import subprocess

from typing import Union
from aws_db_migration import root
from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.exe_enum import MysqlDumpExeEnum, MysqlExeEnum

logr = logging.getLogger(__name__)

SQL_FILE_DUMP_DIR = '/tmp/aws-db-migration/mysql/'
SQL_FILE_DUMP_PATH = f'{SQL_FILE_DUMP_DIR}dump.sql'


def execute_mysql_action(mysql_exe: Union[MysqlExeEnum, MysqlDumpExeEnum]):
    """
    Executes mysql (mysql or mysqldump) action depending on provided enum value.

    :return: No return.
    """
    if isinstance(mysql_exe, MysqlExeEnum):
        action = ActionEnum.RESTORE

        if not os.path.isfile(SQL_FILE_DUMP_PATH):
            raise ValueError('Can not initiate restore action. Sql dump file is missing.')
    elif isinstance(mysql_exe, MysqlDumpExeEnum):
        action = ActionEnum.BACKUP

        # Clear directory from previous dump files.
        try:
            shutil.rmtree(SQL_FILE_DUMP_DIR)
        except FileNotFoundError:
            pass

        # Create a directory for dump file if it does not exist.
        if not os.path.exists(SQL_FILE_DUMP_DIR):
            os.makedirs(SQL_FILE_DUMP_DIR)
    else:
        raise ValueError('Unsupported mysql execute enum type.')

    args = [
        os.environ['AWS_DB_MIGRATION_USERNAME'],
        os.environ['AWS_DB_MIGRATION_PASSWORD'],
        os.environ['AWS_DB_MIGRATION_DATABASE'],
        os.environ['AWS_DB_MIGRATION_HOST'],
        os.environ['AWS_DB_MIGRATION_PORT'],
        SQL_FILE_DUMP_PATH,
        mysql_exe.value,
        action.name
    ]

    try:
        output = subprocess.check_output([f'{root}/mysql_exe.sh', *args], stderr=subprocess.STDOUT)
        logr.info(output.decode())
    except subprocess.CalledProcessError as ex:
        logr.error(ex.output.decode())
        raise
