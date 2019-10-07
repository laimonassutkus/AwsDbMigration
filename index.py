"""
This file is used purely for AWS Lambda function handling. Nothing more.
"""
from aws_db_migration.run_lambda import RunLambda


def run(event, context):
    RunLambda(event, context).run()
