import logging

from pyspark.sql import SparkSession

# Настройка логирования
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Параметры подключения
DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "database": "postgres",
    "user": "airflow",
    "password": "airflow"
}

JDBC_URL = f"jdbc:postgresql://{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
JDBC_PROPERTIES = {
    "user": DB_CONFIG["user"],
    "password": DB_CONFIG["password"],
    "driver": "org.postgresql.Driver"
}

TABLE_NAME = "test_table"


def read_with_spark():
    try:
        spark = SparkSession.builder \
            .appName("ReadTable") \
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
    read_with_spark()
