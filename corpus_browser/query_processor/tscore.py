#! /usr/bin/python
# -*- Coding:UTF-8 -*-

from query_processor_strategy import QueryProcessorStrategy
from math import sqrt


class TTest(QueryProcessorStrategy):
    '''
         2.576 is the critical value for deviation = 005.
         So we cannot reject the null hypothesis if it less than it.
    '''
    def calc(self, freq1, freq2, collocate_freq, corpus_size, span=6):
        self.freq1, self.freq2 = float(freq1), float(freq2)
        self.collocate_freq = float(collocate_freq)
        self.corpus_size = float(corpus_size)
        self.span = span

        return (self.sample_mean - self.mean ) /             \
               sqrt(self.sample_variance/self.corpus_size)

    def posipility(self, freq):
        return freq / float(self.corpus_size)

    @property
    def mean(self):
        return self.posipility(self.freq1) * self.posipility(self.freq2)

    @property
    def sample_mean(self):
        return self.posipility(self.collocate_freq)

    @property
    def sample_variance(self):
        return self.sample_mean
