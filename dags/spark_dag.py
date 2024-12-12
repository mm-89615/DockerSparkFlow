from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago

with DAG(dag_id='spark_submit_example',
        start_date=days_ago(1),
        schedule_interval=None,
        catchup=False) as dag:
    spark_submit_task = SparkSubmitOperator(task_id='spark_submit_job',
        application='jobs/example_jobs.py',
        conn_id='spark_conn')
