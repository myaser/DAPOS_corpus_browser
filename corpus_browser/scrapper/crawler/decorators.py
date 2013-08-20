

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
