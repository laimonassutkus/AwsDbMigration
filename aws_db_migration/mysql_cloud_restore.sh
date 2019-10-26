#!/usr/bin/env bash

set -e

USERNAME=$1;
PASSWORD=$2;
DATABASE=$3;
HOST=$4;
PORT=$5;
DUMP_PATH=$6

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

echo "Using mysql to load a backup file."
${SCRIPTPATH}/amazon-linux-mysql -u"$USERNAME" -p"$PASSWORD" -h"$HOST" -P"$PORT" "$DATABASE" < "$DUMP_PATH"
