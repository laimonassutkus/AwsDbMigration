import base64
import json
import logging
import os
import boto3

from typing import Optional
from aws_db_migration.action_enum import ActionEnum
from aws_db_migration.aws_credentials import AwsCredentials

logr = logging.getLogger(__name__)


class InvokeLambda:
    def __init__(self, aws_credentials: AwsCredentials, event_type: ActionEnum, lambda_name: Optional[str] = None):
        self.__lambda_name = lambda_name or os.environ['AWS_LAMBDA_MIGRATION_NAME']

        self.action = event_type

        self.__client = boto3.client(
            'lambda',
            region_name=aws_credentials.region,
            aws_access_key_id=aws_credentials.access_key,
            aws_secret_access_key=aws_credentials.secret_key
        )

    def run(self) -> bool:
        success = True

        response = self.__client.invoke(
            FunctionName=self.__lambda_name,
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
