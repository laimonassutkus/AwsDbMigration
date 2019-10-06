import logging
import os
import subprocess

from typing import Union
from aws_db_migration import root
from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.exe_enum import MysqlDumpExeEnum, MysqlExeEnum

logr = logging.getLogger(__name__)

SQL_FILE_DUMP_PATH = '/tmp/aws-db-migration/mysql/dump.sql'


def execute_mysql_action(mysql_exe: Union[MysqlExeEnum, MysqlDumpExeEnum]):
    """
    Executes mysql (mysql or mysqldump) action depending on provided enum value.

    :return: No return.
    """
    if isinstance(mysql_exe, MysqlExeEnum):
        action = ActionEnum.RESTORE
    elif isinstance(mysql_exe, MysqlDumpExeEnum):
        action = ActionEnum.BACKUP
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
        output = subprocess.check_output([f'{root}/mysql_exe.sh', args], stderr=subprocess.STDOUT)
        logr.info(output.decode())
    except subprocess.CalledProcessError as ex:
        logr.error(ex.output.decode())
        raise
