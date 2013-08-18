from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangotoolbox import fields as mongo_fields
from indexer.managers import TweetsManager
from utils import model_repr


class IndexMixin():

    @property
    def document_frequency(self):
        pass

    @property
    def term_frequency(self):
        pass

    @property
    def target_documents(self):
        pass

    def __unicode__(self):
        return model_repr(self)


class Tweet(models.Model):

    INFLUENCE_CHOICES = (
        ('HF', 'highly influential'),
        ('MF', 'influential'),
        ('LF', ''),
    )
    created_at = models.DateField(auto_now_add=True)
    user_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    influence = models.CharField(max_length=50, choices=INFLUENCE_CHOICES)
    tweet_text = models.TextField()
    tweet_id = models.CharField(max_length=100, unique=True)
    posting_date = models.DateField()
    retweets = models.IntegerField()
    hash_tags = mongo_fields.ListField()
    mentions = mongo_fields.ListField()
    links = mongo_fields.ListField()

    objects = TweetsManager()

    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')

    def __unicode__(self):
        return model_repr(self)

    @property
    def tokens(self):
        '''
        linguistically process tweet_text and return tokenized terms
        '''
        return self.tweet_text.split()


class Posting(models.Model):

    document = models.ForeignKey(Tweet)
    positions = mongo_fields.ListField()

    @property
    def target_document(self):
        pass

    def __unicode__(self):
        return model_repr(self)


class MainIndex(models.Model, IndexMixin):

    token = models.CharField(max_length=10, unique=True)
    postings = mongo_fields.ListField(mongo_fields.EmbeddedModelField('Posting'))


class AuxilaryIndex(models.Model, IndexMixin):

    token = models.CharField(max_length=10, unique=True)
    postings = mongo_fields.ListField(mongo_fields.EmbeddedModelField('Posting'))

    def merge(self):
        pass
