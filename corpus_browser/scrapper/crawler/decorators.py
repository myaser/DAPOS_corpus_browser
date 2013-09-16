from utils import flatten


def is_valid_hashtag(hashtag):
    return True

def is_valid_username(username):
    return True

def is_valid_tweet(tweet):
    '''
        validate tweet
        return True of False
        Now, it's a place holder !
    '''
    return True


def filter_tweets(fn, *args, **kwargs):
    '''
        filter decorator for tweets
    '''
    def func(*args, **kwargs):
        tweets = fn(*args, **kwargs)
        return filter(is_valid_tweet, tweets)
    return func

def extract_new_criterion(fn, *args, **kwargs):
    '''
        guess new critria from tweets
    '''
    def func(*args, **kwargs):
        from scrapper.models import Criterion
        tweets = fn(*args, **kwargs)
        if tweets:
            users, hash_tags = zip(*map(
                lambda tweet:(tweet['mentions'], tweet['hash_tags']), tweets
            ))

            users = flatten(users)
            hash_tags = flatten(hash_tags)
            criteria_obj = [Criterion(type='hash_tag', value=hashtag) for hashtag in hash_tags if is_valid_hashtag(hashtag)]
            criteria_obj += [Criterion(type='user_name', value=username) for username in users if is_valid_username(username)]
            Criterion.objects.bulk_create_or_skip(hash_tags=hash_tags, user_name=users)
        return tweets
    return func

