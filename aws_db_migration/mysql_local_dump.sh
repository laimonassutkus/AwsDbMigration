#!/usr/bin/env bash

set -e

USERNAME=$1;
PASSWORD=$2;
DATABASE=$3;
HOST=$4;
PORT=$5;
DUMP_PATH=$6

echo "Using mysqldump to create a backup file."
mysqldump -u"$USERNAME" -p"$PASSWORD" -h"$HOST" -P"$PORT" "$DATABASE" --single-transaction --routines --triggers > "$DUMP_PATH"
