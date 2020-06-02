import tweepy
import json
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        super().__init__()

    def on_data(self, data):
        # print(data.text)
        j = json.loads(data)
        # print(j.keys())
        print(j['text'])
        self.producer.send(self.topic, j['text'])
        # print(j['geo'])
        # print(j)
        # print(j['location'])


if __name__ == "__main__":

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'], client_id="tweet_producer")

    with open("tokens.json") as f:
        tokens = json.load(f)

    auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])

    with open('tweets_filter.json') as f:
        tweets_filter = json.load(f)

    languages = tweets_filter['languages']

    new_topics = [NewTopic(topic['name'], num_partitions=1, replication_factor=1)
                  for topic in tweets_filter['topics']]
    admin_client.create_topics(new_topics=new_topics)

    for topic in tweets_filter['topics']:
        myStreamListener = MyStreamListener(producer, topic['name'])
        myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

        myStream.filter(languages=languages, locations=topic['location'])
