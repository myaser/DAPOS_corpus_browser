# -*- coding: UTF-8 -*-

import os
from corpus_browser.settings import PROJECT_ROOT
from utils.tests import MongoTestCase
from indexer.models import AuxiliaryIndex, Tweet
from query_processor.collocationer import Collocationer
from query_processor import QueryProcessor
from collections import Iterable


class TestCollocationer(MongoTestCase):

    def setUp(self):
        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testindex.json')
        fixture = open(fixture_file).read()
        AuxiliaryIndex.load_data(fixture)

        fixture_file = os.path.join(PROJECT_ROOT,
                                            'indexer/fixtures/testtweets.json')
        tweet_fixture = open(fixture_file).read()
        Tweet.load_data(tweet_fixture)

        self.collocationer = Collocationer('t-score')
        self.collocationer.set_index(AuxiliaryIndex)
        self.tokens = [u'الله', u'كبير']
        self.search_result = AuxiliaryIndex.objects.intersect(token__in=self.tokens)

    def test_other_tokens(self):
        tokens = self.collocationer._other_tokens(self.search_result, set(self.tokens), 5)
        self.assertEqual(set([
            u'الفاشلين', u'في', u'الخروج', u'الليلة', u'دي', u'زيي', u'اقعدوا',
            u'صلوا', u'وادعوا..', u'الدعا', u'بيرد', u'القضا،', u'ادعو', u'خوف',
            u'وطمع..', u'الفاشلين', u'في', u'الخروج',
            u'الليلة', u'دي', u'زيي', u'اقعدوا', u'صلوا', u'وادعوا..', u'الدعا',
            u'بيرد', u'القضا،', u'ادعو', u'خوف', u'وطمع..']),
            tokens)

    def test_extract_freq(self):
        self.collocationer.window = 0
        freq = AuxiliaryIndex.objects.collocation_frequency([u'خوف'], self.tokens,
                                                  self.search_result, window=0)
        self.assertEqual(1, freq[u'خوف'])

    def test_t_score(self):
        # TODO:
        query_processor = QueryProcessor(AuxiliaryIndex, u'الله كبير', Collocationer('t-score'))
        result = query_processor.excute_query()
        self.assertTrue(isinstance(result, Iterable))

    def test_mutual_information(self):
        # TODO:
        query_processor = QueryProcessor(AuxiliaryIndex, u'الله كبير', Collocationer('mutual_information'))
        result = query_processor.excute_query()
        self.assertTrue(isinstance(result, Iterable))

    def test_log_likelihood(self):
        # TODO:
        query_processor = QueryProcessor(AuxiliaryIndex, u'الله كبير', Collocationer('log_likelihood'))
        result = query_processor.excute_query()
        self.assertTrue(isinstance(result, Iterable))
