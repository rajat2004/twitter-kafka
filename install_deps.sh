#!/bin/sh

sudo apt-get install openjdk-8-jdk
sudo apt install python3-pip

wget https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz
tar -xzf kafka_2.12-2.5.0.tgz

wget https://archive.apache.org/dist/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
tar -xzf spark-2.4.6-bin-hadoop2.7.tgz

git clone https://github.com/rajat2004/twitter-kafka
cd twitter-kafka

pip3 install -r requirements.txt
