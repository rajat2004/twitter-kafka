import org.apache.spark.SparkConf
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010._

import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.common.serialization.StringDeserializer

object TweetConsumer {
    def main(args: Array[String]) {
        if (args.length < 3) {
          System.err.println(s"""
            |Usage: TweetConsumer <brokers> <groupId> <topics>
            |  <brokers> is a list of one or more Kafka brokers
            |  <groupId> is a consumer group name to consume from topics
            |  <topics> is a list of one or more kafka topics to consume from
            |
            """.stripMargin)
          System.exit(1)
        }

        val Array(brokers, groupId, topics) = args

        val conf = new SparkConf().setMaster("local[2]").setAppName("TweetConsumer")
        val ssc = new StreamingContext(conf, Seconds(1))

        val topicsSet = topics.split(",").toSet
        val kafkaParams = Map[String, Object](
            ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> brokers,
            ConsumerConfig.GROUP_ID_CONFIG -> groupId,
            ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer],
            ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer]
        )

        val messages = KafkaUtils.createDirectStream[String, String](
            ssc,
            LocationStrategies.PreferConsistent,
            ConsumerStrategies.Subscribe[String, String](topicsSet, kafkaParams)
        )

        val lines = messages.map(_.value)
        val words = lines.flatMap(_.split(" "))
        val pairs = words.map(word => (word, 1))
        val wordCounts = pairs.reduceByKey(_ + _)
        wordCounts.print()

        ssc.start()             // Start the computation
        ssc.awaitTermination()
    }
}
