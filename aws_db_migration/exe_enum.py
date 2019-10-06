from enum import Enum
from aws_db_migration import root


class MysqlExeEnum(Enum):
    """
    Executable constants for restoring a database from a dump file.
    """
    LOCAL_MYSQL = 'mysql'
    SERVER_MYSQL = f'{root}/amazon-linux-mysql'


class MysqlDumpExeEnum(Enum):
    """
    Executable constants for creating a database dump file.
    """
    LOCAL_MYSQL_DUMP = 'mysqldump'
    SERVER_MYSQL_DUMP = f'{root}/amazon-linux-mysqldump'
