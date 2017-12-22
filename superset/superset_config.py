import os

#---------------------------------------------------------
# Superset specific config
#---------------------------------------------------------
ROW_LIMIT = int(os.environ.get('ROW_LIMIT', 5000))
SUPERSET_WORKERS = int(os.environ.get('SUPERSET_WORKERS', 4))

SUPERSET_WEBSERVER_PORT = int(os.environ.get('APP_PORT', 8088))
#---------------------------------------------------------

#---------------------------------------------------------
# Flask App Builder configuration
#---------------------------------------------------------
# Your App secret key
SECRET_KEY = os.environ.get('SECRET_KEY', 'G7_JNk:K[?=;_}>')

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/superset.db'
DATABASE_USER = os.environ.get('DATABASE_USER', 'superset')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'tesrpus')
DATABSE_NAME = os.environ.get('DATABASE_NAME', 'superset')
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:5432/{}'.format(DATABASE_USER,
                                                            DATABASE_PASSWORD,
                                                            DATABASE_HOST,
                                                            DATABSE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True

CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://redis:6379/1'}

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''