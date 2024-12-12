#!/usr/bin/env bash
set -e
echo "Starting Airflow initialization script..."

echo "Upgrading Airflow database schema..."
airflow db migrate

echo "Checking if admin user already exists..."
ADMIN_EXISTS=$(airflow users list --output table | grep admin || true)

if [ -z "$ADMIN_EXISTS" ]; then
    echo "Admin user does not exist. Creating admin user..."
    airflow users create \
        --username admin \
        --password admin \
        --firstname Airflow \
        --lastname Admin \
        --role Admin \
        --email admin@example.com
else
    echo "Admin user already exists. Skipping admin creation."
fi
echo "Running Python script to add connections..."
python /add_connections.py

echo "Initialization script completed. Starting Airflow service..."
exec "$@"
