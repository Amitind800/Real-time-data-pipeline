# Real-Time Data Pipeline (Kafka → Spark → Postgres)

## Overview
This project demonstrates a real-time data pipeline using:
- **Kafka** for event streaming
- **Spark Structured Streaming** for processing
- **Postgres** for storage

Producer (Python) → Kafka → Spark → Postgres → (Future: Airflow & Grafana)

---

## Setup

### 1. Clone & Navigate
```bash
git clone <repo>
cd Real-Time-Data-Pipeline

### Start services

docker-compose up -d

Services:

Zookeeper: localhost:2181

Kafka: localhost:9092 (external), kafka:29092 (internal)

Spark Master: localhost:8080

Postgres: localhost:5432 (user: airflow, pass: airflow, db: pipeline)

###Kafka

Create topic
docker exec -it kafka kafka-topics \
  --create --topic user-topic \
  --partitions 1 --replication-factor 1 \
  --bootstrap-server kafka:29092

##list topics
docker exec -it kafka kafka-topics \
  --list --bootstrap-server kafka:29092

#Producer(python)
pip install kafka-python faker names

#run producer
python producer.py

##sample output
Sent: {'name': 'Amit', 'email': 'user24@example.com', 'timestamp': 1757266727.5482824}


##Spark streaming
submit job
docker exec -it spark-master /opt/bitnami/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.5.1 \
  /opt/bitnami/spark/apps/spark_streaming.py


##postgres 
enter postgres container

docker exec -it postgres psql -U airflow -d pipeline

create table:
CREATE TABLE users (
  name TEXT,
  email TEXT,
  timestamp DOUBLE PRECISION
);

check inserted data:
docker exec -it postgres psql -U airflow -d pipeline -c "SELECT * FROM users;"


#Common Issues

KerberosAuthException → add Spark configs for PLAINTEXT
UnknownTopicOrPartitionException → ensure topic exists, use correct bootstrap-server
PSQL command errors in PowerShell → wrap SQL in quotes "..."

#Next Steps

Add deduplication in Spark
Orchestrate pipeline with Airflow
Visualize data with Grafana/Redash
