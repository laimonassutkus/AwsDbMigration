import base64
import json
import logging
import os
import boto3

from typing import Optional, Tuple
from aws_db_migration.action_enum import ActionEnum

logr = logging.getLogger(__name__)


class InvokeLambda:
    def __init__(self, event_type: ActionEnum, key_secret: Optional[Tuple[str, str]] = None):
        self.action = event_type

        if key_secret:
            self.__client = boto3.client(
                'lambda',
                aws_access_key_id=key_secret[0],
                aws_secret_access_key=key_secret[1]
            )
        else:
            self.__client = boto3.client('lambda')

    def run(self) -> bool:
        success = True

        response = self.__client.invoke(
            FunctionName=os.environ['AWS_LAMBDA_MIGRATION_NAME'],
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps({
                'type': self.action.name
            }).encode()
        )

        if response.get('FunctionError'):
            success = False
            logr.error(f'Lambda function threw an error. Error type: {response["FunctionError"]}.')

        log_result = base64.b64decode(response['LogResult']).decode()
        logr.info(log_result)

        return success
