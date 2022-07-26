import tweepy as tw
import json
from dotenv import load_dotenv
import os


load_dotenv()

twitter_cred = dict()
twitter_cred["CONSUMER_KEY"] = os.getenv('consumer_key')
twitter_cred["CONSUMER_SECRET"] = os.getenv('consumer_secret')
twitter_cred["ACCESS_KEY"] = os.getenv('access_token')
twitter_cred["ACCESS_SECRET"] = os.getenv('access_token_secret')

auth = tw.OAuthHandler(
    twitter_cred["CONSUMER_KEY"], twitter_cred["CONSUMER_SECRET"])
auth.set_access_token(
    twitter_cred["ACCESS_KEY"], twitter_cred["ACCESS_SECRET"])
api = tw.API(auth, wait_on_rate_limit=True)


class StreamAPI(tw.StreamingClient):
    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        print(raw_data)
        print()


streamer = StreamAPI(os.getenv('bearer_token'))

for rule in streamer.get_rules().data:
    streamer.delete_rules(rule.id)
print(streamer.get_rules())

rules = []
rules.append("#shop OR #shopping OR #sale OR #sale OR #flipkart OR #fashion")
# rules.append("from:godofgeeks_")

for rule in rules:
    streamer.add_rules(tw.StreamRule(rule))

streamer.filter()
