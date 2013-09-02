import os

from corpus_browser.settings import PROJECT_ROOT

from indexer.tests import MongoTestCase
from indexer.models import Posting, TestIndex, TestTweet
from utils import change_collection, document_repr


class FixturesTest(MongoTestCase):

    def setUp(self):
        self.json_data = '''[
    {
        "username": "Rehab Bassam",
        "hash_tags": [""],
        "user_id": "hadouta",
        "links": [""],
        "created_at": {
            "$date": 1377417143904
        },
        "tweet_text": "\u0645\u0631\u0633\u064a \u0627\u062a\u062c\u0646\u0646! \u0645\u0631\u0633\u064a \u0627\u062a\u062c\u0646\u0646! ",
        "tweet_id": "http://twitter.com/hadouta/status/352193652631674880",
        "retweets": 0,
        "mentions": [""],
        "posting_date": {
            "$date": 1372723200000
        },
        "_id": {
            "$oid": "5219fe08c454fe20195f7593"
        }
    }
]'''
        self.json_file_path = '/tmp/json_test_file'
        open(self.json_file_path, 'w').write(self.json_data)

        self.object = TestTweet.objects.from_json(self.json_data)

    def test_load_data(self):
        self.assertRaisesMessage(Exception,
                 'can only take either in_data or in_file_path and not both',
                 TestTweet.load_data, in_data=self.json_data,
                 in_file_path=self.json_file_path)

        self.assertEqual(self.object, TestTweet.load_data(in_data=self.json_data))

        TestTweet.objects.delete()
        self.assertEqual(self.object,
                         TestTweet.load_data(in_file_path=self.json_file_path))

    def test_dump_data(self):
        self.object[0]._created = True
        TestTweet.objects.insert(self.object[0])

        TestTweet.dump_data(out_file_path=self.json_file_path)

        self.assertEqual(TestTweet.objects.to_json(),
                         open(self.json_file_path).read())


class IndexTest(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testindex.json')
        self.index_fixture = open(fixture_file).read()
        TestIndex.load_data(self.index_fixture)

        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testtweets.json')
        self.tweet_fixture = open(fixture_file).read()
        TestTweet.load_data(self.tweet_fixture)

        @change_collection(collection='test_other_index')
        class Index(TestIndex):
            pass

        self.Index = Index

    def tearDown(self):
        self.Index.objects.delete()
        MongoTestCase.tearDown(self)

    def test_target_documents(self):
        index_object = TestIndex.objects.get(id='521b0cd2c454fe116c319878')

        desired = ["5219fe08c454fe20195f75c4", "5219fe0ac454fe20195f7705",
                   "5219fe0ac454fe20195f76e3", "5219fe09c454fe20195f7601",
                   "5219fe0ac454fe20195f76dd", "5219fe0ac454fe20195f7691"]
        self.assertEqual(desired, [doc.id.__str__() for doc in
                                   index_object.target_documents])

    def test_creation(self):
        '''
        make sure postings lists contains unique elements
        make sure document frequency is saved
        '''
        _document = TestTweet.objects.get(id="5219fe08c454fe20195f75c4")

        index_object = TestIndex.objects.create(token='test',
             postings=[Posting(document=_document, positions=[1, 2, 3])] * 5)

        self.assertEqual(index_object.document_frequency, 1)
        self.assertEqual(index_object.term_frequency, 3)
        self.assertEqual(index_object.postings,
                         [Posting(document=_document, positions=[1, 2, 3])])

    def test_merge(self):

        def modify_object(obj):
            obj._created = True
            obj.postings = obj.postings[:len(obj.postings) / 2]
            return obj

        # instantiate Index with data:
        objects = map(modify_object,
                      self.Index.objects.from_json(self.index_fixture))
        self.Index.objects.insert(objects)

        desired = [obj for obj in TestIndex.objects]

        TestIndex.merge(self.Index, sleep=0.1)

        result = [obj for obj in self.Index.objects]

        self.assertEqual(TestIndex.objects.count(), 0)
        self.assertEqual(result, desired)
