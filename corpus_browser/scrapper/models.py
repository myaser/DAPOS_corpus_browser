from django.db import models
from django.utils.translation import ugettext_lazy as _
from scrapper.crawler import fetcher

# from tasks import lunch_crawlers

class Criterion(models.Model):
    HASH_TAG = 'hash_tag'
    USER_NAME = 'user_name'
    criteria_supported = (
        (HASH_TAG, 'Hash tag'),
        (USER_NAME, 'User name'),
    )
    type = models.CharField(max_length=50, choices=criteria_supported)
    value = models.CharField(max_length=70)
    last_tweet_id = models.CharField(max_length=100, blank=True, null=True)

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
        return {
            self.USER_NAME: fetcher.fetch_user_tweets,
            self.HASH_TAG: fetcher.fetch_hash_tweets,
        }.get(self.type)(self.value, self.last_tweet_id)
