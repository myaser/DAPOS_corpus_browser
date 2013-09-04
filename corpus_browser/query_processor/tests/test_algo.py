from django.test import TestCase
from query_processor.llh import LogLikeliHood
from query_processor.mi import MutualInformation
from query_processor.ngram import NGram
from query_processor.tscore import TTest
from query_processor import make_query_processor, QueryProcessor


class DefaultTest(TestCase):
    def setUp(self):
        self.word1 = 'purple'
        self.freq1 = 1262
        self.word2 = 'colour'
        self.freq2 = 115
        self.collocate_freq = 24
        self.corpus_size =  96263399
        self.span = 6


class TestQueryProcessorCreator(TestCase):

    def setUp(self):
        TestCase.setUp(self)

    def test_make_loglikelihood(self):

        self.processor = make_query_processor('loglikelihood')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, LogLikeliHood))

    def test_make_mutual_information(self):

        self.processor = make_query_processor('mutual_information')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, MutualInformation))

    def test_make_t_score(self):

        self.processor = make_query_processor('t-score')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, TTest))

    def test_make_ngram(self):

        self.processor = make_query_processor('ngram')
        self.assertTrue(isinstance(self.processor, QueryProcessor))
        self.assertTrue(isinstance(self.processor.strategy, NGram))


class TestLogLikelihood(DefaultTest):

    def setUp(self):
        TestCase.setUp(self)

    def test_method(self):

        self.assertEqual(
            round(make_query_processor('loglikelihood').calc(
                12593,
                932,
                150,
                14307668,
                6
            ), 2),
            1291.32
        )
        self.assertEqual(
            round(make_query_processor('loglikelihood').calc(
                379,
                932,
                10,
                14307668,
                6
            ), 2),
            100.5
        )
        self.assertEqual(
            round(make_query_processor('loglikelihood').calc(
                932,
                934,
                10,
                14307668,
                6
            ), 2),
            82.38
        )
        self.assertEqual(
            round(make_query_processor('loglikelihood').calc(
                932,
                3424,
                13,
                14307668,
                6
            ), 2),
            80.37
        )
        self.assertEqual(
            round(make_query_processor('loglikelihood').calc(
                932,
                291,
                6,
                14307668,
                6
            ), 2),
            57.29
        )

class TestMutualInformation(DefaultTest):

    def setUp(self):
        TestCase.setUp(self)
    def test_method(self):

        self.assertEqual(
            round(make_query_processor('mutual_information').calc(
                42,
                20,
                20,
                14307668,
                6
            ), 2),
            18.38
        )
        self.assertEqual(
            round(make_query_processor('mutual_information').calc(
                13484,
                10570,
                20,
                14307668,
                6
            ), 2),
            1.01
        )
        self.assertEqual(
            round(make_query_processor('mutual_information').calc(
                106,
                6,
                1,
                14307668,
                6
            ), 2),
            14.46
        )


class TestNgram(DefaultTest):
    def setUp(self):
        self.skipTest('error')
        TestCase.setUp(self)


class TestTTest(DefaultTest):
    def test_method(self):
        self.assertEqual(
            round(make_query_processor('t-score').calc(
                15828,
                4675,
                8,
                14307668,
                6
            ), 6),
            0.999932
        )
        self.assertEqual(
            round(make_query_processor('t-score').calc(
                42,
                20,
                20,
                14307668,
                6
            ), 4),
            4.4721
        )
        self.assertEqual(
            round(make_query_processor('t-score').calc(
                14907,
                9017,
                20,
                14307668,
                6
            ), 4),
            2.3714
        )
