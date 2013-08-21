from scrapper import settings


def fetch_hash_tweets(hashtag, last_tweet=None, **params):
    if not hashtag.startswith('#'):
        hashtag = '#' + hashtag
    print u"searching for {0} ...".format(hashtag)
    return settings.twitter.search(
        q=hashtag,
        since_id=last_tweet,
        **params
    )['statuses']


def fetch_user_tweets(username, last_tweet=None, **params):
    print u'searching for @{0}'.format(username)
    return settings.twitter.get_home_timeline(
        screen_name=username,
        since_id=last_tweet,
        **params
    )
