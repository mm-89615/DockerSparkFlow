from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

with DAG(dag_id='test_airflow',
        start_date=days_ago(1),
        schedule_interval=None,
        catchup=False) as dag:
    spark_submit_task = SparkSubmitOperator(task_id='spark_submit_job',
        application='jobs/test_airflow.py',
        conn_id='spark_conn',
        packages='org.postgresql:postgresql:42.5.0')
