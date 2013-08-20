import os
import csv

from django.utils import simplejson as json

from django.db import transaction

TOPSY_SCRAP_DIR = '/media/my_files/data/Rania/topsy1_to_150/'

FIXTURE_DIR = os.path.join(PROJECT_ROOT, 'data/fixtures')


def get_csv_file():
    for path, dirlist, filelist in os.walk(TOPSY_SCRAP_DIR):
        for mfile in filelist:
            with open(path + mfile, 'rb') as csvfile:
                csvfile.readline()
                tweets_generator = csv.reader(csvfile,
                                              delimiter=',', quotechar='"')
                yield mfile.strip("topsySscrap.txt"), tweets_generator


if __name__ == '__main__':
    print 'start ...'
    index = 1
    for num, csvfile in get_csv_file():
        print 'writing from file num {n} ...'.format(n=num)
        m = 1
        with transaction.commit_on_success():
            for tweet in csvfile:
                del tweet[2]
                keys = ['user_id', 'username', 'tweet_text', 'tweet_id',
                    'posting_date', 'retweets', 'hash_tags', 'mentions', 'links']
                kwargs = dict(zip(keys, tweet))
                kwargs['hash_tags'] = kwargs['hash_tags'].split(',')
                kwargs['mentions'] = kwargs['mentions'].split(',')
                kwargs['links'] = kwargs['links'].split(',')
                print 'tweet num {m}'.format(m=m)
#                print 'tweet num {m}: {tweet}'.format(m=m, tweet=kwargs)

                tweet = Tweets.objects.get_or_create(tweet_id=kwargs['tweet_id'])[0]
                tweet.update(**kwargs)
                m += 1
