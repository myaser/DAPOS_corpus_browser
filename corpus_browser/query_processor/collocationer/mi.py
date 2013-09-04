#! /usr/bin/python
# -*- Coding:UTF-8 -*-

from llh import LogLikeliHood
from math import log


class MutualInformation(LogLikeliHood):
    def calc(self, freq1, freq2, collocate_freq, corpus_size, span=6):
        self.freq1, self.freq2 = float(freq1), float(freq2)
        self.collocate_freq = float(collocate_freq)
        self.corpus_size = float(corpus_size)
        self.span = span
        return self.I()

    def I(self):
        return log(self.posipility(self.collocate_freq) / (self.posipility(self.freq1) * self.posipility(self.freq2)), 2)

    def posipility(self, freq):
        return freq / self.corpus_size
