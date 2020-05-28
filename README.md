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
