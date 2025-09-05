Real-time data pipeline

Downloaded docker desktop

Download docker desktop from official site ,benefit of using docker desktop it now comes with inbuilt linux feature as WSL(windows subsystem for linux) this will get installed along with the installation of docker

Tweek some setting so that WSL is recognized by VM’s

Download Ubuntu to run the docker command

Setting kafka on docker

To setup kafka on docker we will create a docker-compose.yml file

Once yml file is configured depending on what version we want yml will vary; if we are using kafka with zookeeper which is the version below 7.0.1

Configure yml like this

version: '3.8'


services:

zookeeper:

image: confluentinc/cp-zookeeper:7.0.1

container_name: zookeeper

ports:

- "2181:2181"

environment:

ZOOKEEPER_CLIENT_PORT: 2181

ZOOKEEPER_TICK_TIME: 2000


kafka:

image: confluentinc/cp-kafka:7.0.1

container_name: kafka

ports:

- "9092:9092"

environment:

KAFKA_BROKER_ID: 1

KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181

KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092

KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT

KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT

KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

depends_on:

- zookeeper


If using kraft configure doker-compose.yml like this

environment:

KAFKA_PROCESS_ROLES: broker,controller

KAFKA_NODE_ID: 1

KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093

KAFKA_LISTENERS: PLAINTEXT://kafka:29092,CONTROLLER://kafka:9093,PLAINTEXT_HOST://localhost:9092

KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092

KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT

KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT


docker compose down -v to stop the process running

docker compose up -d to start the process

check running container – docker ps
