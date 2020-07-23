#!/usr/bin/env bash

# KAFKA_DIR="/home/rajat/softwares/kafka_2.12-2.5.0"
$KAFKA_DIR/bin/zookeeper-server-start.sh zookeeper.properties &
sleep 10
$KAFKA_DIR/bin/kafka-server-start.sh server.properties &
