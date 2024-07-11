FROM apache/superset:e274925-py310

USER root

RUN apt-get update && \
    apt-get -y install gcc

RUN pip install psycopg2

COPY ./superset-init.sh /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]


# Copy entrypoint script into the container
COPY superset_config.py /app/superset_config/superset_config.py
COPY __init__.py /app/superset_config/__init__.py

