# AWS DB Migration

#### Short description
Project used to migrate relatively small databases from local machine to cloud and vice versa.

#### Long description
Project that can migrate your local _MySql_ database to an AWS cloud database and vice versa.

This project runs on AWS Lambda function and on a local machine.

Migration is executed in 3 steps: creating mysql dump file, uploading it to S3, restoring the
database from a file. 

Migration from local to cloud looks like this: A mysql dump file from
a local database is created, the file is uploaded to S3, a lambda function (this project) is
invoked to restore a cloud database from a recently uploaded S3 file.

Migration from cloud to local looks like this:
A lambda function (this project) is invoked to create a mysql dump file from
a cloud database and upload it to S3. The most recent dump file is downloaded and 
a local database is restored from it.

Why lambda function? Why can't a direct migration between databases be achieved? Well,
the answer is simple - of course it can! However in this case your cloud database is 
most likely deployed incorrectly. The cloud database should NOT be accessible to the 
whole internet. It should be deployed to a private subnet with a strict security group
attached to it. This way the only way a migration between local and cloud can happen
is through an additional AWS resource instance e.g. lambda, ec2, ecs, etc. This project
has chosen Lambda to keep it light-weight. 

## Prerequisites

#### Local prerequisites
- Mysql server installed.
- Mysql client installed.
- Database set up.
- This project installed with:
```bash
pip install aws-db-migration
```
or:
```bash
./install.sh
```

#### Cloud prerequisites
- Mysql set up on aws cloud (e.g. _RDS_)
- This project deployed as a lambda function with a configured environment 
refer to _.env.example_ file).

## Usage
Note, this project must be deployed as a Lambda function and have access to your cloud database.

Note, that database credentials can be provided either with a _DatabaseCredentials_ class
or through environment variables (refer to _.env.example_ file).

#### Migration to cloud
```python
from aws_db_migration.run_local import RunLocal
from aws_db_migration.database_credentials import DatabaseCredentials
from aws_db_migration.aws_credentials import AwsCredentials

db_credentials = DatabaseCredentials(
    username='username',
    password='password',
    database_name='database',
    host='localhost',
    port='3306'
)

aws_credentials = AwsCredentials()

RunLocal(aws_credentials, db_credentials).to_cloud()
```

#### Migration from cloud
```python
from aws_db_migration.run_local import RunLocal
from aws_db_migration.database_credentials import DatabaseCredentials
from aws_db_migration.aws_credentials import AwsCredentials

db_credentials = DatabaseCredentials(
    username='username',
    password='password',
    database_name='database',
    host='localhost',
    port='3306'
)

aws_credentials = AwsCredentials()

RunLocal(aws_credentials, db_credentials).from_cloud()
```

#### Adding post/pre triggers
```python
from aws_db_migration.run_local import RunLocal
from aws_db_migration.database_credentials import DatabaseCredentials
from aws_db_migration.aws_credentials import AwsCredentials

def f1():
    print('Pre-download!!!')
    
def f2():
    print('Post-download!!!')

runner = RunLocal(AwsCredentials(), DatabaseCredentials())
runner.pre_download = f1
runner.post_download = f2
```
