from django.conf import settings


try:
    APP_KEY = getattr(settings, 'APP_KEY')
except AttributeError:
    raise AttributeError('You should provide APP_KEY')

try:
    CONSUMER_SERCRET = getattr(settings, 'CONSUMER_SERCRET')
except AttributeError:
    raise AttributeError('You should provide CONSUMER_SERCRET')

try:
    ACCESS_TOKEN = getattr(settings, 'ACCESS_TOKEN')
except AttributeError:
    raise AttributeError('You should provide ACCESS_TOKEN')

try:
    ACCESS_TOKEN_SECRET = getattr(settings, 'ACCESS_TOKEN_SECRET')
except AttributeError:
    raise AttributeError('You should provide ACCESS_TOKEN_SECRET')


from twython import Twython
twitter = Twython(app_key=APP_KEY,
                  app_secret=CONSUMER_SERCRET,
                  oauth_token=ACCESS_TOKEN,
                  oauth_token_secret=ACCESS_TOKEN_SECRET)
