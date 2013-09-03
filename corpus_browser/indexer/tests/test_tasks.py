import os


from corpus_browser.settings import PROJECT_ROOT
from indexer.models import MainIndex, AuxiliaryIndex, Tweet
from indexer.tasks import merge_index, build_index
from indexer.tests import MongoTestCase
import datetime


class TasksTest(MongoTestCase):

    def setUp(self):

        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testindex.json')
        self.index_fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(self.index_fixture)

        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testtweets.json')
        self.tweet_fixture = open(fixture_file).read()
        Tweet.load_data(self.tweet_fixture)

    def test_build_index(self):
        def remove_id(obj):
            del obj.id
            return obj

        desired = [remove_id(obj) for obj in AuxiliaryIndex.objects]
        AuxiliaryIndex.objects.delete()

        build_index(from_date=datetime.datetime(2013, 7, 6))
        result = [remove_id(obj) for obj in AuxiliaryIndex.objects]

        self.assertListEqual(result, desired)

    def test_merge_index(self):
        def modify_object(obj):
            obj._created = True
            obj.postings = obj.postings[:len(obj.postings) / 2]
            return obj

        # instantiate Index with data:
        objects = map(modify_object,
                      MainIndex.objects.from_json(self.index_fixture))
        MainIndex.objects.insert(objects)

        desired = sorted([obj.__dict__['_data'] for obj in AuxiliaryIndex.objects], key=lambda x:x['token'])

        merge_index(sleep=0.1)

        result = sorted([obj.__dict__['_data'] for obj in MainIndex.objects], key=lambda x:x['token'])

        self.assertEqual(AuxiliaryIndex.objects.count(), 0)

        for i in range(len(result)):
            result[i]['postings'] = set(result[i]['postings'])
            desired[i]['postings'] = set(desired[i]['postings'])
        self.assertEqual(result, desired)

