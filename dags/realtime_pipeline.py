from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import subprocess


def start_producer():
    """Start Kafka producer"""
    subprocess.Popen(["python3", "/opt/airflow/dags/producer.py"])


default_args = {"start_date": datetime(2025, 9, 1)}

with DAG(
    "realtime_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Step 1: Start Kafka Producer
    start_kafka_producer = PythonOperator(
        task_id="start_producer",
        python_callable=start_producer
    )

    # Step 2: Run Spark Job using SparkSubmitOperator
    '''run_spark_job = SparkSubmitOperator(
        task_id="spark_job",
        application="/opt/bitnami/spark/apps/spark_streaming.py",
        conn_id="spark_default",  # Spark connection in Airflow
        packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                 "org.postgresql:postgresql:42.5.1",
        executor_cores=1,
        executor_memory="1g",
        num_executors=1,
        verbose=True,
    )'''

    run_spark_job = SparkSubmitOperator(
    task_id="spark_job",
    application="/opt/bitnami/spark/apps/spark_streaming.py",
    conn_id="spark_default",
    packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
             "org.postgresql:postgresql:42.5.1",
    conf={
        "spark.jars.ivy": "/tmp/.ivy2",
        "spark.kafka.bootstrap.servers": "kafka:29092",
        "spark.kafka.security.protocol": "PLAINTEXT"
    },
    executor_cores=1,
    executor_memory="1g",
    num_executors=1,
    verbose=True,
    )


    # Step 3: Verify data in Postgres
    verify_postgres = PostgresOperator(
        task_id="check_postgres",
        postgres_conn_id="postgres_default",
        sql="SELECT COUNT(*) FROM users;"
    )

    start_kafka_producer >> run_spark_job >> verify_postgres
