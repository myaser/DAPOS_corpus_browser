#! /usr/bin/python
# -*- Coding:UTF-8 -*-

from query_processor_strategy import QueryProcessorStrategy
from math import log10


class MutualInformation(QueryProcessorStrategy):
    def calc(freq1, freq2, collocate_freq, corpus_size, span=6):
        return log10((collocate_freq*corpus_size)/(freq1*freq2*span))/log10(2)
