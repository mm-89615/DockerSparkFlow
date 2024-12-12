import logging

from airflow.hooks.postgres_hook import PostgresHook
from psycopg2 import sql
from pyspark.sql import SparkSession

# Настройка логирования
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Подключение через Airflow PostgresHook
POSTGRES_CONN_ID = "postgres_conn"
pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
conn_params = pg_hook.get_connection(POSTGRES_CONN_ID)

JDBC_URL = f"jdbc:postgresql://{conn_params.host}:{conn_params.port}/{conn_params.schema}"
JDBC_PROPERTIES = {
    "user": conn_params.login,
    "password": conn_params.password,
    "driver": "org.postgresql.Driver"
}

TABLE_NAME = "test_table"


def write_to_postgres():
    try:
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                name TEXT,
                value INT
            );
        """).format(table_name=sql.Identifier(TABLE_NAME)))
        conn.commit()

        cursor.executemany(sql.SQL("""
            INSERT INTO {table_name} (name, value) VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """).format(table_name=sql.Identifier(TABLE_NAME)), [
            ('Test1', 100),
            ('Test2', 200),
            ('Test3', 300)
        ])
        conn.commit()

        logger.info(f"Data successfully written to table {TABLE_NAME}.")
    except Exception as e:
        logger.error(f"Error writing data to PostgreSQL: {e}")
    finally:
        cursor.close()
        conn.close()


def read_with_spark():
    try:
        spark = SparkSession.builder \
            .appName("ReadAirflowTable") \
            .getOrCreate()

        data = spark.read.jdbc(url=JDBC_URL,
            table=TABLE_NAME,
            properties=JDBC_PROPERTIES)
        data.show()
        spark.stop()
        logger.info("Data successfully read and displayed.")
    except Exception as e:
        logger.error(f"Error reading data with Spark: {e}")


if __name__ == "__main__":
    write_to_postgres()
    read_with_spark()
