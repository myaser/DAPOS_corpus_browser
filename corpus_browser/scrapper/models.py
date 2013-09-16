from django.db import models
from django.utils.translation import ugettext_lazy as _
from scrapper.crawler import fetcher
from utils import iter_to_str

# from tasks import lunch_crawlers


def mix(first, second=[]):
    def iter_generator(x):
        while True:
            yield x

    return zip(iter_generator(first), second)

class BulkCreateOrSkipManager(models.Manager):
    def bulk_create_or_skip(self, *args, **kwargs):
        from django.db import connection, transaction
        cursor = connection.cursor()

        db_table = self.model._meta.db_table
        base_sql = 'INSERT OR IGNORE INTO %s (%s) VALUES %s'

        hash_tags = kwargs.get('hash_tags', [])
        user_name = kwargs.get('user_name', [])
        values = mix('hash_tag', hash_tags)
        values += mix('user_name', user_name)

        values_str = map(iter_to_str, values)

        sql = base_sql % (db_table, 'type, value', ', '.join(values_str))

        # import pdb; pdb.set_trace()
        cursor.execute(sql)
        transaction.commit_unless_managed()

class Criterion(models.Model):
    HASH_TAG = 'hash_tag'
    USER_NAME = 'user_name'
    criteria_supported = (
        (HASH_TAG, 'Hash tag'),
        (USER_NAME, 'User name'),
    )
    type = models.CharField(max_length=50, choices=criteria_supported)
    value = models.CharField(max_length=70, unique=True)
    last_tweet_id = models.CharField(max_length=100, blank=True, null=True)

    objects = BulkCreateOrSkipManager()
    class Meta:
        verbose_name = _('Criterion')
        verbose_name_plural = _('Criteria')

    def __unicode__(self):
        if self.type == self.HASH_TAG:
            if self.value.startswith('#'):
                return u'{0}'.format(self.value)
            return u"#{0}".format(self.value)
        return u"@{0}".format(self.value)

    def fetch_data(self):
        try:
            return {
                self.USER_NAME: fetcher.fetch_user_tweets,
                self.HASH_TAG: fetcher.fetch_hash_tweets,
            }.get(self.type)(self.value, self.last_tweet_id)
        except:
            pass  # rescue from connection errors !

