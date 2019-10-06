from setuptools import setup, find_packages

setup(
    name='aws_db_migration',
    version='1.0.1',
    packages=find_packages(),
    description=(
        'Management project which can run locally and on AWS Lambda function. '
        'Project aims to make database migrations from/to cloud easy.'
    ),
    include_package_data=True,
    install_requires=[
        'boto3',
        'botocore',
        'python-dotenv==0.10.3'
    ],
    author='Laimonas Sutkus',
    author_email='laimonas@myhealthyapps.com',
    keywords='AWS SDK RDS Database Backup Restore Migration Infrastructure Cloud Lambda',
    url='https://github.com/laimonassutkus/AwsDbMigration',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux'
    ],
)
