from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangotoolbox import fields as mongo_fields


class Tweet(models.Model):
    INFLUENCE_CHOICES = (
        ('HF', 'highly influential'),
        ('MF', 'influential'),
        ('LF', ''),
    )
    user_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    influence = models.CharField(max_length=50, choices=INFLUENCE_CHOICES,
                                 null=True, blank=True)
    tweet_text = models.TextField()
    tweet_id = models.CharField(max_length=100, unique=True)
    posting_date = models.DateField(null=True, blank=True)
    retweets = models.IntegerField(null=True, blank=True)
    hash_tags = mongo_fields.ListField()
    mentions = mongo_fields.ListField()
    links = mongo_fields.ListField()


    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')

    def __unicode__(self):
        return u'<Tweet user: {0} text: {1}>'.format(self.username, self.tweet_text)


class Posting(models.Model):

    document = models.ForeignKey(Tweet)
    positions = mongo_fields.ListField()

    @property
    def target_document(self):
        pass


class MainIndex(models.Model):

    token = models.CharField(max_length=10)
    postings = mongo_fields.ListField(mongo_fields.EmbeddedModelField('Posting'))

    @property
    def document_frequency(self):
        pass

    @property
    def term_frequency(self):
        pass

    @property
    def target_documents(self):
        pass


class AuxilaryIndex(MainIndex):

    def merge(self):
        pass

# from datetime import date
# from indexer.models import *
# tweet = Tweet(user_id='', username='', influence='', tweet_text='',
#               tweet_id='', posting_date=date(2013,3,3), hash_tags=[],
#               mentions=[], links=[], retweets=0)
# tweet.save()
