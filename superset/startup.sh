#!/bin/bash

set -e
if [ ! -f /tmp/shared/superset_done ]; then
    # Create an admin user
    fabmanager create-admin --app superset \
            --username $SUPERSET_USER \
            --firstname $SUPERSET_FIRSTNAME \
            --lastname $SUPERSET_LASTNAME \
            --email $SUPERSET_EMAIL  \
            --password $SUPERSET_PASSWORD && \
        superset db upgrade && \
        superset init

    echo "OK" > /tmp/shared/superset_done
fi

# Create default roles and permissions
superset runserver