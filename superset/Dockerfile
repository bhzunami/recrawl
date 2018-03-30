FROM debian:stretch

# Superset version
ARG SUPERSET_VERSION=0.22.1

# Configure environment
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONPATH=/etc/superset:$PYTHONPATH \
    SUPERSET_VERSION=${SUPERSET_VERSION} \
    SUPERSET_HOME=/home/superset

# Create superset user & install dependencies
RUN useradd -U -m superset && \
    apt-get update && \
    apt-get install -y \
        build-essential \
        curl \
        default-libmysqlclient-dev \
        libffi-dev \
        libldap2-dev \
        libpq-dev \
        libsasl2-dev \
        libssl-dev \
        openjdk-8-jdk \
        python3-dev \
        python3-pip && \
    pip3 install \
        flask-cors==3.0.3 \
        flask-mail==0.9.1 \
        gevent==1.2.2 \
        impyla==0.14.0 \
        psycopg2==2.6.1 \
        redis==2.10.5 \
        superset==${SUPERSET_VERSION}

# Configure Filesystem
WORKDIR /home/superset
COPY superset_config.py /home/superset/superset_config.py
COPY startup.sh /home/superset/startup.sh
# Remove windows \r linefeed in shellscript using dos2unix
RUN apt-get update && apt-get install -y dos2unix
RUN dos2unix /home/superset/startup.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

# Deploy application
#HEALTHCHECK CMD ["curl", "-f", "http://localhost:8088/health"]
USER superset

ENTRYPOINT ["/home/superset/startup.sh"]
