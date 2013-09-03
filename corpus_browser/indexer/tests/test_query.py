import os

from corpus_browser.settings import PROJECT_ROOT
from indexer.models import AuxiliaryIndex
from indexer.tests import MongoTestCase


class TestIndexQuerySet(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT, 'indexer/fixtures/testindex.json')
        fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(fixture)

    def test_proximity(self):
        AuxiliaryIndex.objects.proximity(token__in=["@AlshakeroN", u"\u060c"])



