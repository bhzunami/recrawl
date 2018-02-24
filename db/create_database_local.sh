#!/bin/bash
set -e

# Check that the four environments are correctly set
: "${POSTGRES_ADMIN?Need to set POSTGRES_ADMIN}"
: "${POSTGRES_PASSWORD?Need to set POSTGRES_PASSWORD}"
: "${POSTGRES_USER?Need to set POSTGRES_USER}"
: "${DATABASE_NAME?Need to set DATABASE_NAME}"

dropdb --if-exists --username "$POSTGRES_ADMIN" immo
dropdb --if-exists --username "$POSTGRES_ADMIN" metabase
dropdb --if-exists --username "$POSTGRES_ADMIN" superset

dropuser --if-exists immo


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_ADMIN" postgres <<-EOSQL
    CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
    CREATE DATABASE $DATABASE_NAME OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE $DATABASE_NAME TO $POSTGRES_USER;
    CREATE DATABASE metabase OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE metabase TO $POSTGRES_USER;
    CREATE DATABASE superset OWNER $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE superset TO $POSTGRES_USER;
EOSQL

echo "Import schema"
psql --username "$POSTGRES_USER" "$DATABASE_NAME" < database_schema.schema

echo "Import Municipalities"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" "$DATABASE_NAME" <<-EOSQL
\copy municipalities from './municipalities_import.csv' delimiter ';' csv HEADER quote e'\x01';
EOSQL

echo "Import Object_types"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" "$DATABASE_NAME" <<-EOSQL
  \copy object_types from './object_types_import.csv' delimiter ';' csv HEADER;
EOSQL