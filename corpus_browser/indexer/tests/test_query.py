#!/usr/bin/python
# -*- coding:UTF-8 -*-


import os

from corpus_browser.settings import PROJECT_ROOT
from indexer.models import AuxiliaryIndex, Tweet
from utils.tests import MongoTestCase


class TestIndexQuerySet(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testindex.json')
        self.index_fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(self.index_fixture)

        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testtweets.json')
        self.tweet_fixture = open(fixture_file).read()
        Tweet.load_data(self.tweet_fixture)

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

    def test_consequent(self):
        # TODO:
        pass

    def test_frequency(self):
        freq1 = AuxiliaryIndex.objects.frequency(u'الله')
        self.assertEqual(3, freq1)

        freq2 = AuxiliaryIndex.objects.frequency(u'الله', u'كبير', window=0)
        self.assertEqual(1, freq2)

        freq3 = AuxiliaryIndex.objects.frequency(u'مصر', u'الإخوان')
        self.assertEqual(0, freq3)
        freq3 = AuxiliaryIndex.objects.frequency((u'مصر', u'الإخوان'), u'حرق', window=0)
        self.assertEqual(1, freq3)
        freq4 = AuxiliaryIndex.objects.frequency(u'مصر', u'الإخوان', window=0)
        self.assertEqual(3, freq4)
        freq5 = AuxiliaryIndex.objects.frequency(u'مصر', u'الإخوان', window=5)
        self.assertEqual(1, freq5)
        freq6 = AuxiliaryIndex.objects.frequency(u'مصر', u'الإخوان', window=3)
        self.assertEqual(0, freq6)

    def test_select_related_documents(self):
        def exrtact_doc_ids(index_object):
            return [posting.document.id for posting in index_object.postings]

        queryset = AuxiliaryIndex.objects.filter(token__in=[u'مصر', u'الإخوان'])
        queryset_related = queryset.clone().select_related_documents()
        self.assertEqual(len(queryset), len(queryset_related))
        self.assertEqual(map(exrtact_doc_ids, queryset),
                         map(exrtact_doc_ids, queryset_related))
