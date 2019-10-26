import os

from typing import Optional


class DatabaseCredentials:
    def __init__(
            self,
            username: Optional[str] = None,
            password: Optional[str] = None,
            database_name: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[str] = None
    ):
        self.username = username or os.environ.get('AWS_DB_MIGRATION_USERNAME')
        self.password = password or os.environ.get('AWS_DB_MIGRATION_PASSWORD')
        self.database_name = database_name or os.environ.get('AWS_DB_MIGRATION_DATABASE')
        self.host = host or os.environ.get('AWS_DB_MIGRATION_HOST')
        self.port = port or os.environ.get('AWS_DB_MIGRATION_PORT')
