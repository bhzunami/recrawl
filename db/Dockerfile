FROM postgres:9.6

COPY ./create_db_docker.sh /docker-entrypoint-initdb.d/
COPY ./database_schema.schema /docker-entrypoint-initdb.d/
COPY ./municipalities_import.csv /docker-entrypoint-initdb.d/
COPY ./object_types_import.csv /docker-entrypoint-initdb.d/