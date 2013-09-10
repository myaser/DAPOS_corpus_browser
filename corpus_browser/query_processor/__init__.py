#!/usr/bin/python
# -*- coding: utf-8 -*-


from indexer.models import MainIndex
from utils.string_processor import split_unicode
from .collocationer import Operator
import re


class QueryProcessor(object):

    def __init__(self, search_phrase='', operator=None):
        self.search_phrase = search_phrase
        if operator is None:
            raise ValueError('operator should be given!')
        self.operator = Operator.from_str(operator)
        self.parse_search()

    def parse_search(self):
        '''
        process the search phrase and decide what type of
        query (boolean, proximity, phrase) should be done
        '''
        if self.search_phrase.startswith(('"',"'")) and self.search_phrase.endswith(('"',"'")):
            self.query_type = 'phrase'
            self.tokens = split_unicode(self.search_phrase[1:-1])
        elif re.search('\\\d+$', self.search_phrase):
            self.query_type = 'proximity'
            self.phrase, self.proximity, _ = re.split(r'\\\d+$', self.search_phrase)
            self.tokens = split_unicode(self.phrase)
        else:
            self.query_type = 'boolean'
            self.tokens = split_unicode(self.search_phrase)

    def excute_query(self, scoring_algorithm):
        '''
        excute parsed query
        '''
        if self.query_type == 'phrase':
            raise NotImplementedError()
        elif self.query_type == 'proximity':
            self.query_set = MainIndex.objects.proximity(
                window=self.proximity,
                token__in=self.tokens
            )
        elif self.query_type == 'boolean':
            self.query_set = MainIndex.objects.intersect(
                token__in=self.tokens
            )
        return self.post_query(scoring_algorithm)

    def post_query(self, scoring_algorithm):
        '''
        do post query processing according to `self.operator`
        '''
        return self.operator.operate(self.query_set, self.tokens, scoring_algorithm)



def usage_example():
    q = QueryProcessor(u'الله اكبر', 'collocation')
    print q.excute_query('log_likelihood')
