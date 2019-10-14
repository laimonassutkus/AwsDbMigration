import os

from typing import Optional


class AwsCredentials:
    def __init__(
            self,
            access_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            region: Optional[str] = None
    ) -> None:
        self.access_key = access_key or os.environ.get('AWS_DB_MIGRATION_KEY')
        self.secret_key = secret_key or os.environ.get('AWS_DB_MIGRATION_SECRET')
        self.region = region or os.environ.get('AWS_DB_MIGRATION_REGION')
