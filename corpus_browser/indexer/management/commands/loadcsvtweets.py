import csv
import os

from django.core.management.base import BaseCommand, CommandError
from indexer.models import Tweet


class Command(BaseCommand):
    help = "Installs the named csvfile(s) in the Tweet database table.\n\
if directory provided it will load all files in it"
    args = "path [path ...]"

    def handle(self, *csvfile_labels, **options):

        loaded_object_count = 0  # successfully installed objects
        csvfile_object_count = 0  # objects in csvfiles

        # search file system
        try:
            files = []
            for csvfile_label in csvfile_labels:
                csvfile_label = os.path.abspath(csvfile_label)
                if os.path.isdir(csvfile_label):
                    for path, dirlist, filelist in os.walk(csvfile_label):
                        self.stdout.write(
                          "Searching folder '%s'...\n" % path)
                        files.extend([os.path.join(path, _file)
                                      for _file in filelist])
                else:
                    files.append(csvfile_label)
            csvfile_count = len(files)
        except Exception, e:
            raise CommandError(e)

        # parse csvfile
        try:
            def get_tweets(filelist):
                for mfile in filelist:
                    with open(mfile, 'rb') as csvfile:
                        csvfile.readline()  # skip first line identifying schema
                        tweets_generator = csv.reader(csvfile,
                                              delimiter=',', quotechar='"')
                        self.stdout.write("Loading tweets from '%s' ...\n" %
                                            mfile.rpartition('/')[2])
                        yield tweets_generator
        except Exception, e:
            raise CommandError(e)

        # write database
        try:
            for tweets in get_tweets(files):
                for tweet in tweets:
                    csvfile_object_count += 1
                    del tweet[2]
                    keys = ['user_id', 'username', 'tweet_text', 'tweet_id',
                        'posting_date', 'retweets', 'hash_tags', 'mentions', 'links']
                    kwargs = dict(zip(keys, tweet))
                    kwargs['hash_tags'] = kwargs['hash_tags'].split(',')
                    kwargs['mentions'] = kwargs['mentions'].split(',')
                    kwargs['links'] = kwargs['links'].split(',')
                    mtweet, created = Tweet.objects.get_or_create(
                                            tweet_id=kwargs['tweet_id'])
                    mtweet.update(**kwargs)
                    if created:
                        loaded_object_count += 1
            self.stdout.write("Installed {0} object(s) (of {1}) from {2} \
csvfile(s)\n".format(loaded_object_count, csvfile_object_count, csvfile_count))
        except Exception, e:
            raise CommandError(e)
