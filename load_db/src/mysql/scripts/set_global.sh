#!/bin/bash
set -e

mysql -v ON_ERROR_STOP=1 -u "$MYSQL_USER" -p "$MYSQL_PASSWORD" <<-EOSQL
    SET GLOBAL local_infile=1;
EOSQL
