FROM bitnami/spark:3.5.3

USER root

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -o /opt/bitnami/spark/jars/postgresql-42.5.0.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.0/postgresql-42.5.0.jar

COPY docker/spark/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
