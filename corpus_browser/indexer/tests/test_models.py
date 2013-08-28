import os

from corpus_browser.settings import PROJECT_ROOT

from indexer.tests import TestTweet, MongoTestCase, TestIndex


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
        pass


class IndexTest(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT, 'indexer/fixtures/testindex.json')
        fixture = open(fixture_file).read()
        TestIndex.load_data(fixture)

    def test_target_documents(self):
        TestIndex.objects.get(id='521b0cd2c454fe116c319878')
        pass

    def test_creation(self):
        pass

    def test_frequencies(self):
        pass

    def test_merge(self):
        pass
