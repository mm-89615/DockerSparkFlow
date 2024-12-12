FROM apache/airflow:2.10.3-python3.12

USER airflow

COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r /opt/airflow/requirements.txt

USER root

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends \
      openjdk-17-jdk \
      ant && \
    apt-get clean;

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

COPY docker/airflow/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY docker/airflow/add_connections.py /add_connections.py
RUN chmod +x /add_connections.py

USER airflow

ENTRYPOINT ["/entrypoint.sh"]
CMD ["airflow", "webserver"]
