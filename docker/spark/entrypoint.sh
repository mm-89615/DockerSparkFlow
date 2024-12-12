#!/usr/bin/env bash
set -e

echo "Starting Spark initialization script..."

SPARK_HOME=/opt/bitnami/spark
echo "SPARK_HOME set to $SPARK_HOME"

if [ "$SPARK_MODE" = "master" ]; then
    echo "Starting Spark Master node..."
    ${SPARK_HOME}/bin/spark-class org.apache.spark.deploy.master.Master \
        --ip 0.0.0.0 \
        --port 7077 \
        --webui-port 8080
elif [ "$SPARK_MODE" = "worker" ]; then
    echo "Spark Master is ready. Starting Spark Worker node..."
    ${SPARK_HOME}/bin/spark-class org.apache.spark.deploy.worker.Worker \
        ${SPARK_MASTER_URL:-spark://spark-master:7077}
else
    echo "SPARK_MODE not set to master or worker! Exiting."
    exit 1
fi

echo "Spark node initialization completed."
