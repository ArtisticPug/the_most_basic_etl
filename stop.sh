#!/bin/bash

# Stop python scripts
pkill -f from_kafka.py
pkill -f to_kafka.py

# Delete Kafka topic Kafka broker daemon Zookeeper daemon
./kafka/kafka_2.13-2.8.0/bin/kafka-topics.sh --delete  --topic test --zookeeper localhost:2181
sleep 2
./kafka/kafka_2.13-2.8.0/bin/kafka-server-stop.sh -daemon ./kafka/kafka_2.13-2.8.0/config/server.properties
sleep 2
./kafka/kafka_2.13-2.8.0/bin/zookeeper-server-stop.sh -daemon ./kafka/kafka_2.13-2.8.0/config/zookeeper.properties
sleep 2
sudo docker stop postgres_db
sleep 2
sudo docker stop taskmanager
sleep 2
sudo docker stop jobmanager
sleep 2
# Delete kafka, posrgres folders
rm -R kafka
rm -R postgres
deactivate
rm -R venv
rm -R __pycache__
rm nohup.out
rm ./pythoncode/nohup.out