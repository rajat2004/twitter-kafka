from pyspark.sql import SparkSession
from pyspark.mllib.fpm import FPGrowth
import time
from datetime import datetime
import json
import logging
import os

log = logging.getLogger()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def process_batch(df, epoch_id, topic_name):
    """
    Counts tweets in a batch, runs FPGrowth, and saves output to text file
    """
    # Open file in outputs folder in append mode
    file = open(f'outputs/{topic_name}', 'a')

    now = datetime.now()
    current_time = now.strftime("%d/%m/%y %H:%M:%S")
    file.write(f"Time: {current_time}\n")

    log.info(f"Custom Batch process for {topic_name}")
    log.debug(df.collect())
    log.info(f"Current Time: {current_time}, Epoch ID: {epoch_id}")

    tweet_count = df.count()
    log.info(f"Total tweets in batch: {tweet_count}")
    file.write(f"Total tweets in batch: {tweet_count}\n")

    if tweet_count > 3:
        log.info("Running FPGrowth")
        file.write("Frequent Itemsets:\n")
        # Remove duplicate entries in a row
        transactions = df.rdd.map(lambda line: line.value.split(" "))
        unique = transactions.map(lambda x: list(set(x)) )

        model = FPGrowth.train(unique, minSupport=0.3)
        # Sort items based on frequency
        result = sorted(model.freqItemsets().collect(), reverse=True, key=lambda x: x[1])
        for fi in result:
            log.debug(fi)
            file.write(f'{fi}\n')
    else:
        file.write('Not running FPGrowth due to low no. of tweets\n')

    file.write('\n\n')
    file.close()


if __name__ == "__main__":

    spark = SparkSession \
            .builder \
            .appName("StructuredNetworkWordCount") \
            .getOrCreate()

    spark.sparkContext.setLogLevel('WARN')

    topic_ca = "CA"
    topic_ny = "NY"

    # Load Tweet filtering data
    with open('spark_consumer_config.json') as f:
        spark_consumer_config = json.load(f)

    brokers = spark_consumer_config['kafka-brokers']
    interval_min = spark_consumer_config.get('interval', 10)

    time_interval = f"{interval_min} minutes"

    log.info(f"Brokers: {brokers}, Interval: {time_interval}")

    lines_ca = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", brokers) \
            .option("subscribe", topic_ca) \
            .load() \
            .selectExpr("CAST(value AS STRING)")

    lines_ny = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", brokers) \
            .option("subscribe", topic_ny) \
            .load() \
            .selectExpr("CAST(value AS STRING)")

    # lines.printSchema()

    # def process_row(row):
    #     print("Custom row function: " + "|".join(map(str,row)) )


    query_ca = lines_ca \
            .writeStream \
            .foreachBatch(lambda df, epoch_id: process_batch(df, epoch_id, topic_ca)) \
            .trigger(processingTime = time_interval) \
            .start()

    query_ny = lines_ny \
            .writeStream \
            .foreachBatch(lambda df, epoch_id: process_batch(df, epoch_id, topic_ny)) \
            .trigger(processingTime = time_interval) \
            .start()


    query_ca.awaitTermination()
    query_ny.awaitTermination()

    # queries = [query_ca, query_ny]
    # for query in queries:
    #     query.awaitTermination()
    #     time.sleep(30)
