from .fetcher import fetch_hash_tweets, fetch_user_tweets
from .decorators import filter_tweets
from celery import task
from indexer.models import Tweet
from django.db import transaction
import re
from datetime import datetime


month_to_nums = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 5, 'Jul': 6, 'Aug': 7,
    'Seb': 9,'Oct': 10, 'Nov': 11, 'Des': 12
}

@transaction.commit_on_success
def bulk_create(Model, *intries):
    '''
        masive create models
        use transaction to make one commit for all data
    '''
    for intry in intries:
        Model.objects.create(**intry)

def extract_date(date_string):
    '''
        convert from date format in twitter api to datetime object
    '''
    p = re.compile('\w{3} (?P<month>\w{3}) (?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}) \+0000 (?P<year>\d{4})')
    date_dict = p.match(date_string).groupdict()
    if not date_dict:
        return None
    date_dict['month'] = month_to_nums[date_dict['month']]
    date_dict = dict((key, int(value)) for key, value in date_dict.iteritems())
    return datetime(**date_dict)


def extract_data(json):
    '''
        match data from twitter api params to our params
    '''
    Empty = []
    return {
        'user_id': json.get('user', Empty).get('id_str', Empty),
        'username': json.get('user', Empty).get('screen_name', Empty),
        # 'influence': json[''],
        'tweet_text': json.get('text', Empty),
        'tweet_id': json.get('id_str', Empty),
        'posting_date':extract_date(json.get('created_at', 'Empty')),
        'retweets': json.get('retweet_count', Empty),
        'hash_tags': [h.get('text', Empty) for h in json.get('entities', Empty).get('hashtags', Empty)],
        'mentions': [user.get('screen_name', Empty) for user in json.get('entities', Empty).get('user_mentions', Empty)],
        'links': [link.get('url', Empty) for link in json.get('entities', Empty).get('urls', Empty) + json.get('entities', Empty).get('media', Empty)],
    }

@filter_tweets
def fetch(criterion):
    '''
        fetch new tweets for a critrion (Model object)
        return dict of tweets
        (side effect!)update critrion with the last tweet_id
    '''
    tweets = map(extract_data, criterion.fetch_data())
    criterion.last_tweet_id = tweets[0]['tweet_id']
    criterion.save()
    return tweets


@task
def update_tweets(criteria):
    '''
        fetch new tweets according to the critria
        critria is a QuerySet object from Model Critrion
    '''
    for criterion in criteria:
        bulk_create(Tweet, *fetch(criterion))
