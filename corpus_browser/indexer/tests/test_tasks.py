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
        self.skipTest('takes very long time')

        def modify_object(obj):
            obj._created = True
            obj.postings = obj.postings[:len(obj.postings) / 2]
            return obj

        # instantiate Index with data:
        objects = map(modify_object,
                      MainIndex.objects.from_json(self.index_fixture))
        MainIndex.objects.insert(objects)

        desired = [obj.__dict__['_data'] for obj in AuxiliaryIndex.objects]

        merge_index(sleep=0.1)

        result = [obj.__dict__['_data'] for obj in MainIndex.objects]

        self.assertEqual(AuxiliaryIndex.objects.count(), 0)

        # i may need to sort postings before assertion
        for i in range(len(result)): print i, result[i]==desired[i]
#         self.assertEqual(result, desired)
