import time
from datetime import datetime


from mongoengine import (Document, EmbeddedDocument, DateTimeField, StringField,
                 IntField, ListField, ReferenceField, EmbeddedDocumentField)

from utils import document_repr, change_collection
from indexer.query import TweetsQuerySet, IndexQuerySet
from utils import clear_cache

class DocumentFixturesMixin(object):

    @classmethod
    def dump_data(cls, queryset=None, out_file_path=None, *args, **kwargs):
        if not queryset:
            queryset = cls.objects
        json_data = queryset.to_json(*args, **kwargs)

        if out_file_path:
            open(out_file_path, 'w').write(json_data)
        return json_data

    @classmethod
    def load_data(cls, in_data=None, in_file_path=None):

        def created(obj):
            obj._created = True
            return obj

        if bool(in_data) == bool(in_file_path):
            raise Exception('can only take either in_data or in_file_path and not both')

        json_data = in_data or open(in_file_path).read()
        objects = cls.objects.from_json(json_data)
        objects = map(created, objects)

        cls.objects.insert(objects)
        return objects


class Tweet(Document, DocumentFixturesMixin):

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

    meta = {'queryset_class': TweetsQuerySet,
            'allow_inheritance': True}

    def __unicode__(self):
        return document_repr(self)

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

    document = ReferenceField('Tweet', required=True)
    positions = ListField()

    def __unicode__(self):
        return document_repr(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.document.id == other.document.id

    def __hash__(self):
        return hash(self.document.id)


class MainIndex(Document, DocumentFixturesMixin):
    '''
    the index serving users' queries
    '''

    token = StringField(unique=True)

    # TODO: use SetField with postings
    postings = ListField(EmbeddedDocumentField(Posting))
    term_frequency = IntField()

    meta = {'queryset_class': IndexQuerySet,
            'allow_inheritance': True,
            'indexes': ['token']}

    @property
    def document_frequency(self):
        return len(self.postings)

    @classmethod
    @get_or_cache('corpus_size')
    def get_size(self):
        return self.objects.sum('term_frequency')

    @classmethod
    @get_or_cache('tokens_count')
    def get_tokens_count(self):
        return self.objects.count()

    @property
    def target_documents(self):
        return [posting.document for posting in self.postings]

    @property
    def as_result(self):
        result = self.postings[:]
        for document in result:
            document.positions = [(self.token, document.positions)]
        return result

    @classmethod
    def get_index_size(cls):
        # TODO: needs caching
        return sum([obj.term_frequency for obj in cls.objects])

    @classmethod
    def get_tokens_count(cls):
        # TODO: needs caching
        return cls.objects.count()

    def __unicode__(self):
        return document_repr(self)

    def __cmp__(self, other):
        return cmp(self.document_frequency, other.document_frequency)

    def clean(self, *args, **kwargs):
        self.postings = list(set(self.postings))
        self.term_frequency = sum([len(posting.positions)
                                    for posting in self.postings])


@change_collection(collection='auxiliary_index')
class AuxiliaryIndex(MainIndex):
    '''
    hold the data from scrapper to keep the MainIndex serving users
    '''

    @classmethod
    def merge(cls, index, sleep=5):
        '''
        merge the Auxiliary index to the MainIndex.
        '''
        objs = cls.objects.all()
        seg_length = 100
        obj_lists = [objs[x:x + seg_length] for x in range(0, len(objs), seg_length)]
        for obj_list in obj_lists:
            time.sleep(sleep)
            for obj in obj_list:
                index.objects.add_postings(obj.token, obj.postings)
        objs.delete()
        clear_cache()

# TODO: when tweet is deleted, remove from index
