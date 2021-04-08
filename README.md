# twitter-kafka

Final assignment of Cloud Computing course (CS6847) at IIT Madras.

Use Twitter API to fetch tweets of New York and California states, and publish them as Kafka topics to be consumed by Spark and perform basic analysis such as Frequent Pairs of words

Prerequisites -

- Java 8 - `sudo apt-get install openjdk-8-jdk`
- [`Kafka` - 2.5.0](https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz)
- [`Spark` - 2.4.6](https://archive.apache.org/dist/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz)
- Get Twitter developer account and generate Consumer & User keys for application

Create `tokens.json` file with the tokens as following -

```json
{
    "api_key": "XXXXX",
    "api_secret_key": "XXXXX",
    "access_token": "XXXXX",
    "access_token_secret": "XXXXX"
}
```

Add Kafka & Spark to `.bashrc` or `.zshrc`. E.g (paths are assumed to be at home directory below).

```shell
# Java
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# Spark
export SPARK_HOME=~/spark-2.4.6-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3

# Kafka
export KAFKA_DIR=~/kafka_2.12-2.5.0
```

Python Libraries used -

1. `kafka-python`
2. Tweepy
3. `flask`

Use `pip3 install -r requirements.txt`

Create outputs directory - `mkdir outputs`

Commands -

1. Start Kafka - `./start_kafka.sh`
2. Edit config file, Start Tweets producer - `python3 tweets.py -c tweets_producer_config.json`
3. Edit `spark_consumer_config.json`.
    Spark consumer - `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6 spark_consumer.py --executor-memory 500m`
4. Start Web UI - `python3 ui/ui.py`
5. To close Kafka, `./stop_kafka.sh`

Use `test_kafka_producer.py` & `test_kafka_consumer.py` to make sure that Kafka is running properly.

By default, the config files are set for the local system (`localhost`), and can be easily changed to use different brokers when running on muliple machines.

**NOTES**:

To run without command exiting when `ssh` shell dies -

```shell
nohup spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6 spark_consumer.py --executor-memory 500m &
```

You might need to add a port rule for 9092 which is used for Kafka if running on AWS or Azure. Port 5000 will also need to be exposed for Flask
