from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangotoolbox import fields as mongo_fields
from indexer.managers import TweetsManager
from utils import model_repr
import time


class IndexMixin():

    @property
    def document_frequency(self):
        return len(self.postings)

    @property
    def term_frequency(self):
        return sum([len(posting.positions) for posting in self.postings])

    @property
    def target_documents(self):
        return [posting.document for posting in self.postings]

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
    '''
    encapsulate a search result
    '''

    # TODO: make it serializable
    document = models.ForeignKey(Tweet)
    positions = mongo_fields.ListField()

    def __unicode__(self):
        return model_repr(self)


class MainIndex(models.Model, IndexMixin):
    '''
    the index serving users' queries
    '''

    token = models.CharField(max_length=10, unique=True)
    postings = mongo_fields.ListField(mongo_fields.EmbeddedModelField('Posting'))


class AuxiliaryIndex(models.Model, IndexMixin):
    '''
    hold the data from scrapper to keep the MainIndex serving users
    '''

    token = models.CharField(max_length=10, unique=True)
    postings = mongo_fields.ListField(mongo_fields.EmbeddedModelField('Posting'))

    @classmethod
    def merge(cls, index):
        '''
        merge the Auxiliary index to the MainIndex.
        '''
        objs = cls.objects.all()
        seg_length = 100
        obj_lists = [objs[x:x + seg_length] for x in range(0, len(objs), seg_length)]

        for obj_list in obj_lists:
            # prevent overloading the index to stay serving users while merge
            time.sleep(5)
            for obj in obj_list:
                index_entery = index.objects.get_or_create(token=obj.token)[0]
                index_entery.postings += obj.postings_list
                index_entery.save()
