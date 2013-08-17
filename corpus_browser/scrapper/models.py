from django.db import models
from django.utils.translation import ugettext_lazy as _
from scrapper import crawler


class Heuristic(models.Model):
    HASH_TAG = 'hash_tag'
    USER_NAME = 'user_name'
    heurestics_supported = (
        (HASH_TAG, 'Hash tag'),
        (USER_NAME, 'User name'),
    )
    type = models.CharField(max_length=50, choices=heurestics_supported)
    value = models.CharField(max_length=70)
    last_tweet_id = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Heurstic')
        verbose_name_plural = _('Heurstics')

    def __unicode__(self):
        return "#{0}".format(self.value) if self.type == self.hash_tag \
            else "@{0}".format(self.value)

    def fetch_data(self):
        return {
            self.USER_NAME: crawler.fetch_user_tweets,
            self.HASH_TAG: crawler.fetch_hash_tweets,
        }.get(self.type)(self.value, self.last_tweet_id)
