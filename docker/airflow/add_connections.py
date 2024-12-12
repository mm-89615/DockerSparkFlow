import logging

from airflow import settings
from airflow.models.connection import Connection

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Определяем список соединений для добавления
    connections = [
        Connection(
            conn_id='spark_conn',
            conn_type='spark',
            host='spark://spark-master',
            port=7077,
            extra='{"use_ssl": false}'
        ),
        Connection(
            conn_id='postgres_conn',
            conn_type='postgres',
            host='postgres',
            port=5432,
            login='airflow',
            password='airflow',
            schema='airflow',
            extra='{}'
        )
    ]

    # Устанавливаем сессию для взаимодействия с базой данных
    session = settings.Session()

    # Обрабатываем каждый объект соединения
    for conn in connections:
        existing_conn = (session.query(Connection)
                         .filter(Connection.conn_id == conn.conn_id)
                         .first())
        if not existing_conn:
            session.add(conn)
            logger.info(f"Connection '{conn.conn_id}' added successfully!")
        else:
            logger.info(f"Connection '{conn.conn_id}' already exists.")

    # Сохраняем изменения
    session.commit()

except Exception as e:
    logger.error(f"An error occurred while adding connections: {e}")
finally:
    # Закрываем сессию
    session.close()
