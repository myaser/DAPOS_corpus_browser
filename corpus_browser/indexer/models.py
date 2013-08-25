import time
from datetime import datetime


from mongoengine import (Document, EmbeddedDocument, DateTimeField, StringField,
         IntField, ListField, ReferenceField, EmbeddedDocumentField, CASCADE,
         PULL)

from utils import model_repr, change_collection
from indexer.query import TweetsQuerySet, IndexQuerySet


class Tweet(Document):

    created_at = DateTimeField(default=datetime.now())
    user_id = StringField()
    username = StringField()

    tweet_text = StringField()
    tweet_id = StringField(unique=True, required=True)
    posting_date = DateTimeField()
    retweets = IntField()
    hash_tags = ListField()
    mentions = ListField()
    links = ListField()

    meta = {'queryset_class': TweetsQuerySet}

    def __unicode__(self):
        return model_repr(self)

    @property
    def tokens(self):
        '''
        linguistically process tweet_text and return tokenized terms
        '''
        return self.tweet_text.split()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


class Posting(EmbeddedDocument):
    '''
    encapsulate a search result
    '''

    document = ReferenceField('Tweet')
    positions = ListField()

    def __unicode__(self):
        return model_repr(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.document == other.document


class MainIndex(Document):
    '''
    the index serving users' queries
    '''

    token = StringField(unique=True)
    postings = ListField(EmbeddedDocumentField(Posting))
    term_frequency = IntField()

    meta = {'queryset_class': IndexQuerySet,
            'allow_inheritance': True,
            'indexes': ['token']}

    @property
    def document_frequency(self):
        return len(self.postings)

    @property
    def target_documents(self):
        return [posting.document for posting in self.postings]

    def __unicode__(self):
        return model_repr(self)

    def clean(self):
        self.term_frequency = sum([len(posting.positions)
                                    for posting in self.postings])


@change_collection(collection='auxiliary_index')
class AuxiliaryIndex(MainIndex):
    '''
    hold the data from scrapper to keep the MainIndex serving users
    '''

#     meta = MainIndex._meta.copy()
#     meta['collection'] = 'auxiliary_index'

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
#             time.sleep(5)
            for obj in obj_list:
                index_entery = index.objects.get_or_create(token=obj.token)[0]
                index_entery.postings += obj.postings
                index_entery.save()
        import pdb; pdb.set_trace()
        objs.delete()


# Tweet.register_delete_rule(MainIndex, 'postings', PULL)
