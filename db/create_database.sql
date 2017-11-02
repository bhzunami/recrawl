#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" postgres <<-EOSQL
    CREATE USER '$POSTGRES_DB' WITH PASSWORD '$POSTGRES_PASSWORD';
    CREATE DATABASE immo;
    GRANT ALL PRIVILEGES ON DATABASE '$POSTGRES_DB' TO '$POSTGRES_USER';
EOSQL

echo "Import schema"
psql --username "$POSTGRES_USER" "$POSTGRES_DB" < database_schema.sql

echo "Import Municipalities"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" "$POSTGRES_DB" <<-EOSQL
\copy municipalities from './municipalities_import.csv' delimiter ';' csv HEADER quote e'\x01';
EOSQL

echo "Import Object_types"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" "$POSTGRES_DB" <<-EOSQL
  \copy object_types from './object_types_import.csv' delimiter ';' csv HEADER;
EOSQL