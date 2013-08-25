import time
from datetime import datetime

from django.utils.translation import ugettext_lazy as _

from mongoengine import (Document, DateTimeField, StringField, IntField,
                         ListField)

from indexer.managers import TweetsManager, IndexManager
from utils import model_repr


class Tweet(Document):

    created_at = DateTimeField(default=datetime.now())
    user_id = StringField(max_length=50)
    username = StringField(max_length=50)

    tweet_text = StringField(required=True)
    tweet_id = StringField(max_length=100, unique=True, required=True)
    posting_date = DateTimeField()
    retweets = IntField()
    hash_tags = ListField()
    mentions = ListField()
    links = ListField()

#     objects = TweetsManager()
# 
#     class Meta:
#         verbose_name = _('Tweet')
#         verbose_name_plural = _('Tweets')
# 
#     def __unicode__(self):
#         return model_repr(self)
# 
#     @property
#     def tokens(self):
#         '''
#         linguistically process tweet_text and return tokenized terms
#         '''
#         return self.tweet_text.split()
# 
#     def update(self, **kwargs):
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#         return self.save()


# class Posting(models.Model):
#     '''
#     encapsulate a search result
#     '''
# 
#     # TODO: make it serializable (pk error)
#     document = models.ForeignKey(Tweet)
#     positions = mongo_fields.ListField()
# 
#     def __unicode__(self):
#         return model_repr(self)
# 
#     def __eq__(self, other):
#         return isinstance(other, self.__class__) and self.document == other.document
# 
# 
# class Index(models.Model):
# 
#     objects = IndexManager()
# 
#     token = models.CharField(max_length=10, unique=True)
#     postings = mongo_fields.ListField(mongo_fields.EmbeddedModelField('Posting'))
#     term_frequency = models.IntegerField(null=True)
# 
#     @property
#     def document_frequency(self):
#         return len(self.postings)
# 
#     @property
#     def target_documents(self):
#         return [posting.document for posting in self.postings]
# 
#     def __unicode__(self):
#         return model_repr(self)
# 
#     def save(self, *args, **kwargs):
#         self.term_frequency = sum([len(posting.positions)
#                                     for posting in self.postings])
#         models.Model.save(self, *args, **kwargs)
# 
#     class Meta:
#         abstract = True
# 
# 
# class MainIndex(Index):
#     '''
#     the index serving users' queries
#     '''
# 
# 
# class AuxiliaryIndex(Index):
#     '''
#     hold the data from scrapper to keep the MainIndex serving users
#     '''
# 
#     @classmethod
#     def merge(cls, index):
#         '''
#         merge the Auxiliary index to the MainIndex.
#         '''
#         objs = cls.objects.all()
#         seg_length = 100
#         obj_lists = [objs[x:x + seg_length] for x in range(0, len(objs), seg_length)]
#         with transaction.commit_on_success():
#             for obj_list in obj_lists:
#                 # prevent overloading the index to stay serving users while merge
#                 time.sleep(5)
#                 for obj in obj_list:
#                     index_entery = index.objects.get_or_create(token=obj.token)[0]
#                     index_entery.postings += obj.postings_list
#                     index_entery.save()
#         objs.delete()
