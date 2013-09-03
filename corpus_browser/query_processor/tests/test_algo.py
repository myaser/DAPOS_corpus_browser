from django.test import TestCase
from query_processor.llh import LogLikeliHood
from query_processor.mi import MutualInformation
from query_processor.ngram import NGram
from query_processor.tscore import TTest
from query_processor import make_query_processor, QueryProcessor
from unittest.case import SkipTest


class DefaultTest(TestCase):
    def setup(self):
        self.word1 = 'purple'
        self.freq1 = 1262
        self.word2 = 'colour'
        self.freq2 = 115
        self.collocate_freq = 24
        self.corpus_size =  96263399
        self.span = 6


class TestQueryProcessorCreator(TestCase):

    def test_make_loglikelihood(self):
        SkipTest('pass')
        self.processor = make_query_processor('loglikelihood')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, LogLikeliHood))

    def test_make_mutual_information(self):
        SkipTest('pass')
        self.processor = make_query_processor('mutual_information')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, MutualInformation))

    def test_make_t_score(self):
        SkipTest('pass')
        self.processor = make_query_processor('t-score')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, TTest))

    def test_make_ngram(self):
        SkipTest('pass')
        self.processor = make_query_processor('ngram')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, NGram))


class TestLogLikelihood(DefaultTest):

    def test_method(self):
        SkipTest('pass')
        self.assertEqual(
            round(make_query_processor('loglikelihood').calc(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            1111
        )


class TestMutualInformation(DefaultTest):
    def test_method(self):
        SkipTest('pass')
        self.assertEqual(
            round(make_query_processor('mutual_information').calc(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            11.37
        )


class TestNgram(DefaultTest):
    def test_method(self):
        SkipTest('pass')
        self.assertEqual(
            round(make_query_processor('ngram').calc(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            1111
        )


class TestTTest(DefaultTest):
    def test_method(self):
        SkipTest('pass')
        self.assertEqual(
            round(make_query_processor('t-score').calc(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            1111
        )
