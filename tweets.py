import tweepy
import json

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        # print(data.text)
        j = json.loads(data)
        # print(j.keys())
        print(j['text'])
        # print(j['geo'])
        # print(j)
        # print(j['location'])


if __name__ == "__main__":

    with open("tokens.json") as f:
        tokens = json.load(f)

    auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])

    with open('tweets_filter.json') as f:
        tweets_filter = json.load(f)

    languages = tweets_filter['languages']

    for topics in tweets_filter['topics']:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

        myStream.filter(languages=languages, locations=topics['location'])
