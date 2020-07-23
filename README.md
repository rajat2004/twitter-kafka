# twitter-kafka

Final assignment of Cloud Computing course (CS6847) at IIT Madras.

Use Twitter API to fetch tweets of New York and California states, and publish them as Kafka topics to be consumed by Spark and perform basic analysis such as WordCount, Frequent Pairs of words

Prerequisites -

- `Kafka`
- `Spark`
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

Python Libraries used -

1. `kafka-python`
2. Tweepy
3. `flask`

Use `pip install -r requirements.txt`

Commands -

1. Start Kafka - `./start_kafka.sh`
2. Edit config file, Start Tweets producer - `python tweets.py -c tweets_producer_config.json`
3. Edit `spark_consumer_config.json`.
    Spark consumer - `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6 spark_consumer.py --executor-memory 500m`
4. Start Web UI - `python ui/ui.py`
5. To close Kafka, `./stop_kafka.sh`

To run without command exiting when `ssh` shell dies -

```shell
nohup spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.6 spark_consumer.py --executor-memory 500m &
```
