from django.test import TestCase
from query_processor.llh import loglikelihood
from query_processor.mi import mutual_information
from query_processor.negma import negma
from query_processor.tscore import t_score


class DefaultTest(TestCase):
    def setup(self):
        self.word1 = 'purple'
        self.freq1 = 1262
        self.word2 = 'colour'
        self.freq2 = 115
        self.collocate_freq = 24
        self.corpus_size =  96263399
        self.span = 6


class TestLogLikelihood(DefaultTest):
    def test_method(self):
        self.assertEqual(
            round(loglikelihood(
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
        self.assertEqual(
            round(mutual_information(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            11.37
        )


class TestNegma(DefaultTest):
    def test_method(self):
        self.assertEqual(
            round(negma(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            1111
        )


class TestTScore(DefaultTest):
    def test_method(self):
        self.assertEqual(
            round(t_score(
                self.freq1,
                self.freq2,
                self.collocate_freq,
                self.corpus_size,
                self.span
            ), 2),
            1111
        )
