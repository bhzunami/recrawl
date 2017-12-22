#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_ADMIN" postgres <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $POSTGRES_USER;
    CREATE DATABASE metabase OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE metabase TO $POSTGRES_USER;
    CREATE DATABASE superset OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE superset TO $POSTGRES_USER;
EOSQL

echo "Import schema"
psql --username "$POSTGRES_USER" "$DATABASE_NAME" < /docker-entrypoint-initdb.d/database_schema.schema

echo "Import Municipalities"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" "$DATABASE_NAME" <<-EOSQL
\copy municipalities from '/docker-entrypoint-initdb.d/municipalities_import.csv' delimiter ';' csv HEADER quote e'\x01';
EOSQL

echo "Import Object_types"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" "$DATABASE_NAME" <<-EOSQL
  \copy object_types from '/docker-entrypoint-initdb.d/object_types_import.csv' delimiter ';' csv HEADER;
EOSQL
