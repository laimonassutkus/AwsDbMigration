#!/usr/bin/env bash

set -e

USERNAME=$1;
PASSWORD=$2;
DATABASE=$3;
HOST=$4;
PORT=$5;
DUMP_PATH=$6
MYSQL_EXE=$7
# Ensure that action type is supported by a provided mysql executable.
MYSQL_ACTION_TYPE=$9

if [[ "$MYSQL_ACTION_TYPE" = "BACKUP" ]]
then
    echo "Using mysqldump to create a backup file."
    ${MYSQL_EXE} -u"$USERNAME" -p"$PASSWORD" -h"$HOST" -P"$PORT" "$DATABASE" > "$DUMP_PATH"
elif [[ "$MYSQL_ACTION_TYPE" = "RESTORE" ]]
then
    echo "Using mysql to load a backup file."
    ${MYSQL_EXE} -u"$USERNAME" -p"$PASSWORD" -h"$HOST" -P"$PORT" "$DATABASE" < "$DUMP_PATH"
else
    echo "Unsupported event. Should be BACKUP or RESTORE."
    exit 127
fi
