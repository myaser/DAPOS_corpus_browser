import os

from django.test import TestCase

from corpus_browser.settings import PROJECT_ROOT
from indexer.tests import TestTweet, MongoTestCase, TestIndex


class TestIndexQuerySet(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT, 'indexer/fixtures/testindex.json')
        fixture = open(fixture_file).read()
        TestIndex.load_data(fixture)

    def test_proximity(self):
        TestIndex.objects.proximity(token__in=["@AlshakeroN", u"\u060c"])



