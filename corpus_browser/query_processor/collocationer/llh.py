#! /usr/bin/python
# -*- Coding:UTF-8 -*-

from math import log

from query_processor.collocationer import Scorer


class LogLikeliHood(Scorer):

    def calc(self, freq1, freq2, collocate_freq, corpus_size, span=6):
        self.freq1, self.freq2 = float(freq1), float(freq2)
        self.collocate_freq = float(collocate_freq)
        self.corpus_size = float(corpus_size)
        self.span = span

        return -2 * self.loglikelihood_ratio()

    def loglikelihood_ratio(self):
        ''' log10(lambda) '''
        return self.hypothesis1 - self.hypothesis2

    @property
    def hypothesis1(self):
        term1 = self._log_l(self.collocate_freq, self.freq1, self._p)
        term2 = self._log_l(self.freq2 - self.collocate_freq, self.corpus_size - self.freq1, self._p)
        return term1 + term2

    @property
    def hypothesis2(self):
        term1 = self._log_l(self.collocate_freq, self.freq1, self._p1)
        term2 = self._log_l(self.freq2 - self.collocate_freq, self.corpus_size - self.freq1, self._p2)
        return term1 + term2

    @property
    def _p(self):
        # return Decimal(self.freq2) / self.corpus_size
        return self.freq2 / self.corpus_size

    @property
    def _p1(self):
        return self.collocate_freq / self.freq1

    @property
    def _p2(self):
        return (self.freq2 - self.collocate_freq)/(self.corpus_size - self.freq1)

    def _log_l(self, k, n, x):
        return k * log(x)+ (n-k)*log(1-x)
