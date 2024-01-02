import tweepy

from .constants import TWITTER_BEARER_TOKEN

twitter = tweepy.Client(TWITTER_BEARER_TOKEN)


def get_models_tweets(models):
    for model in models:
        keyword = model['name']
        print(f'Keyword: {keyword}')
        tweets = twitter.search_recent_tweets(query=f'{keyword}', max_results=3)
        return tweets
