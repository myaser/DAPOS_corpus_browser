import os

from corpus_browser.settings import PROJECT_ROOT
from indexer.models import AuxiliaryIndex
from indexer.tests import MongoTestCase


class TestIndexQuerySet(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT, 'indexer/fixtures/testindex.json')
        fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(fixture)
        self.token1 = u"\u0648\u0627\u0639\u062f"
        self.token2 = u"\u0647\u064a\u062a\u062c\u0646\u0646\u0648\u0627"
        self.token3 = u"\u0648\u0627\u0642\u0641\u0629"

    def test_intersect(self):
        result = AuxiliaryIndex.objects.intersect(
            token__in=[self.token1, self.token2]
        )
        t1 = AuxiliaryIndex.objects.get(token=self.token1)
        t2 = AuxiliaryIndex.objects.get(token=self.token2)
        for posting in result:
            self.assertTrue(posting.document in map(lambda x:x.document, t1.postings))
            self.assertTrue(posting.document in map(lambda x:x.document, t2.postings))

            p1 = [p for p in t1.postings if posting.document == p.document][0].positions
            p2 = [p for p in t2.postings if posting.document == p.document][0].positions

            self.assertTrue((self.token1, p1) in posting.positions)
            self.assertTrue((self.token2, p2) in posting.positions)

        result2 = AuxiliaryIndex.objects.intersect(
            token__in=[self.token1, self.token3]
        )
        self.assertFalse(bool(result2))

    def test_proximity(self):
        result = AuxiliaryIndex.objects.proximity(
            window=5,
            token__in=[self.token1, self.token2]
        )
        t1 = AuxiliaryIndex.objects.get(token=self.token1)
        t2 = AuxiliaryIndex.objects.get(token=self.token2)
        for posting in result:
            self.assertTrue(posting.document in map(lambda x:x.document, t1.postings))
            self.assertTrue(posting.document in map(lambda x:x.document, t2.postings))

            p1 = [p for p in t1.postings if posting.document == p.document][0].positions
            p2 = [p for p in t2.postings if posting.document == p.document][0].positions

            self.assertTrue((self.token1, p1) in posting.positions)
            self.assertTrue((self.token2, p2) in posting.positions)

        result2 = AuxiliaryIndex.objects.proximity(
            window=3,
            token__in=[self.token1, self.token2]
        )
        self.assertFalse(bool(result2))

        result3 = AuxiliaryIndex.objects.intersect(
            token__in=[self.token1, self.token3]
        )
        self.assertFalse(bool(result3))
