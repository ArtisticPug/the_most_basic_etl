#!/bin/bash

# Install python3-venv and activate it
sudo apt install python3-venv -y
sleep 1
python3 -m venv venv
sleep 1
. ./venv/bin/activate
sleep 1
# Dependencies
sudo apt install libpq-dev python-dev gcc build-essential libssl-dev libffi-dev python3-dev openjdk-8-jre -y
pip install wheel psycopg2 flask kafka-python chardet
sleep 1
# Create dir for Kafka, download it and extract
wget -P ./kafka https://mirror.linux-ia64.org/apache/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xf ./kafka/kafka_2.13-2.8.0.tgz -C ./kafka/
rm ./kafka/kafka_2.13-2.8.0.tgz
sleep 1
# Start Zookeeper daemon
./kafka/kafka_2.13-2.8.0/bin/zookeeper-server-start.sh -daemon ./kafka/kafka_2.13-2.8.0/config/zookeeper.properties
sleep 2
# Start Kafka broker daemon
./kafka/kafka_2.13-2.8.0/bin/kafka-server-start.sh -daemon ./kafka/kafka_2.13-2.8.0/config/server.properties
sleep 2
# Create Kafka topic
./kafka/kafka_2.13-2.8.0/bin/kafka-topics.sh --create --topic test --zookeeper localhost:2181 --partitions 1 --replication-factor 1
sleep 2
# create dir for postgres volume
mkdir postgres
sleep 1
# run Docker postgres
sudo docker run --name postgres_db \
    --detach \
    --rm \
    -v ./postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=postgres -d -p 5432:5432 postgres
sleep 5
# enter postgres docker container and Postgres, create custom schema and table, also trgm extension
sudo docker exec postgres_db \
    psql -U postgres --command="
                CREATE SCHEMA the_database;
                CREATE TABLE the_database.the_table(
                id serial PRIMARY KEY,
                word varchar(50) UNIQUE
                );
                CREATE EXTENSION pg_trgm;
                "
# Launch Flink JobManager
FLINK_PROPERTIES="jobmanager.rpc.address: jobmanager"
sudo docker run \
	--detach \
	--rm \
	--name=jobmanager \
	--network flink-network \
	--publish 8081:8081 \
	--env FLINK_PROPERTIES="${FLINK_PROPERTIES}" \
	flink:1.13.0-scala_2.11 jobmanager
sleep 2
# Launch Flink TaskManager	
FLINK_PROPERTIES="jobmanager.rpc.address: jobmanager"
sudo docker run \
	--detach \
    --rm \
    --name=taskmanager \
    --network flink-network \
    --env FLINK_PROPERTIES="${FLINK_PROPERTIES}" \
    flink:1.13.0-scala_2.11 taskmanager
# Run python consumer and producer
chmod +x ./pythoncode/from_kafka.py
nohup python3 ./pythoncode/from_kafka.py &
sleep 1
chmod +x ./pythoncode/to_kafka.py
nohup python3 ./pythoncode/to_kafka.py &
sleep 1
# Install Flask, run Flask server in debug mode listenin on :5000
export FLASK_ENV=development
python -m flask run --host=0.0.0.0
