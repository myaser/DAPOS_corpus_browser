from .fetcher import fetch_hash_tweets, fetch_user_tweets
from indexer.models import Tweet


def extract_data(json):
    return {
        'user_id': json['user']['id_str'],
        'username': json['user']['screen_name'],
        'influence': json[''],
        'tweet_text': json['text'],
        'tweet_id': json['id_str'],
        'posting_date': json['created_at'],
        'retweets': json['retweet_count'],
        'hash_tags': [h['text'] for h in json['entities']['hashtags']],
        'mentions': [user['screen_name'] for user in json['entities']['user_mentions']],
        'links': [link['url'] for link in json['entities']['urls'] + json['entities']['media']],
    }


def fetch():
    from scrapper.models import Heuristic
    heuristics = Heuristic.objects.all()
    for heuristic in heuristics:
        data = map(heuristic.fetch_data(), extract_data)
        Tweet.objects.bulk_create(map(data, lambda x: Tweet(**x)))
