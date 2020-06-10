import tweepy
import json
import logging
import os
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from utils import check_location

log = logging.getLogger()
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, producer, topics):
        """
        Stream listener for publishing tweets to topics based on location

        producer - Kafka producer
        topics - List of topics with topic name & rectangular bounding box
        """
        self.producer = producer
        self.topics = topics
        super().__init__()

    def on_data(self, data):
        j = json.loads(data)

        # Check the tweet for location
        # Needed to figure out topic to send the tweet on
        if j['coordinates'] is not None:
            topic_name = None

            for topic in self.topics:
                if check_location(j['coordinates']['coordinates'], topic['location']):
                    topic_name = topic['name']
                    break

            if topic_name is None:
                log.warn(f'Topic name none for coordinates - {j["coordinates"]["coordinates"]}, returning')
                return

            log.info(f'{topic_name} - {j["coordinates"]["coordinates"]} - {j["text"]}')
            self.producer.send(topic_name, j['text'])


if __name__ == "__main__":

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'], client_id="tweet_producer")

    # Load Twitter API access tokens
    with open("tokens.json") as f:
        tokens = json.load(f)

    auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])

    # Load Tweet filtering data
    with open('tweets_filter.json') as f:
        tweets_filter = json.load(f)

    languages = tweets_filter['languages']

    new_topics = []
    locations = []

    # Create topics & filter locations list
    for topic in tweets_filter['topics']:
        new_topics.append(NewTopic(topic['name'], num_partitions=1, replication_factor=1))
        locations += topic['location']

    # Topics might already exist
    try:
        admin_client.create_topics(new_topics=new_topics)
    except TopicAlreadyExistsError as e:
        log.warn(f'Topics already exist - {e}')

    # Create Stream Listener
    myStreamListener = MyStreamListener(producer, tweets_filter['topics'])
    myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

    myStream.filter(languages=languages, locations=locations)
