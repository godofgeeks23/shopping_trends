import tweepy as tw
from datetime import datetime as dt
from elasticsearch import Elasticsearch
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
# Initialize elasticsearch node
es = Elasticsearch("http://localhost:9200")

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


def acqData(search, acq):
    # Create an index name using our search criteria and today's date
    index_name = search.split(' ')[0] + '-' + dt.today().strftime('%Y-%m-%d')
    # Initialize the feed list of dictionaries
    feed = []

    print('::Acquiring Data::')

    # Data Acquisition
    for tweet in tw.Cursor(api.search_tweets, q=search, tweet_mode='extended').items(acq):
        feed.append(tweet._json)
    with open("json_dat.json", "w") as f:
        json.dump(feed, f)
# Formatting the data and extracting what we need
    count = 0

    print('::Transferring to Elasticsearch Search::')

    while count < len(feed):
        # Created variables instead of directly injecting it to the dictionary because it's easier to read
        tweet_date = feed[count]['created_at']
        username = feed[count]['user']['screen_name']
        account_creation_date = feed[count]['created_at']
        user_description = feed[count]['user']['description']
        user_url = feed[count]['user']['url']
        verified_status = feed[count]['user']['verified']
        geo_enabled = feed[count]['user']['geo_enabled']
        friends_count = feed[count]['user']['friends_count']
        followers_count = feed[count]['user']['followers_count']
        retweeted_count = feed[count]['retweet_count']
        favorite_count = feed[count]['favorite_count']
        hashtags = feed[count]['entities']['hashtags']
        tweet_full_text = feed[count]['full_text']
        # Prepare data for elasticsearch
        doc = {
            '@timestamp': dt.now(),
            'tweet_date': tweet_date,
            'username': str(username),
            'account_creation_date': str(account_creation_date),
            'user_description': str(user_description),
            'user_url': str(user_url),
            'verified_status': bool(verified_status),
            'geo_enabled': bool(geo_enabled),
            'friends_count': int(friends_count),
            'followers_count': int(followers_count),
            'retweeted_count': int(retweeted_count),
            'favorite_count': int(favorite_count),
            'hashtags': hashtags,
            'tweet_full_text': str(tweet_full_text),
            'word_list': str(tweet_full_text).split(' ')
        }
        # Import into elasticsearch using the generated index name at the top of the function <search> + <date>
        es.index(index=index_name, document=doc)
        count += 1


acqData('covid', 100)
