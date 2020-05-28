#!/usr/bin/env bash

KAFKA_DIR="/home/rajat/softwares/kafka_2.12-2.5.0"
$KAFKA_DIR/bin/zookeeper-server-start.sh zookeeper.properties &
sleep 10
$KAFKA_DIR/bin/kafka-server-start.sh server.properties &
# $KAFKA_DIR/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
