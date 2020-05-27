import tweepy
import json

class MyStreamListener(tweepy.StreamListener):

    # def on_status(self, status):
    #     print(status.text)

    def on_data(self, data):
        # print(data.text)
        j = json.loads(data)
        print(j['text'])


if __name__ == "__main__":

    with open("tokens.json") as f:
        tokens = json.load(f)

    auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
    auth.set_access_token(tokens['access_token'], tokens['access_token_secret'])

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = auth, listener=myStreamListener)

    myStream.filter(track=['python'])
