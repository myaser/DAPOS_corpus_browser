from utils.string_processor import split_unicode
import re


class Operator():
    def set_index(self, index):
        self.index = index

    def operate(self, queryset, tokens):
        '''
        do nothing
        '''
        return queryset, tokens


class QueryProcessor(object):

    def __init__(self, index, search_phrase='', operator=Operator):
        self.search_phrase = search_phrase
        self.index = index

        if operator is None:
            raise ValueError('operator should be given!')
        operator.set_index(index)
        self.operator = operator

        self.parse_search()

    def parse_search(self):
        '''
        process the search phrase and decide what type of
        query (boolean, proximity, phrase) should be done
        '''
        # phrase search
        if self.search_phrase.startswith(('"', "'")) and self.search_phrase.endswith(('"',"'")):
            self.query_type = 'phrase'
            self.tokens = split_unicode(self.search_phrase[1:-1])

        # proximity search
        elif re.search('\\\d+$', self.search_phrase):
            self.query_type = 'proximity'
            self.phrase, self.proximity, _ = re.split(r'\\\d+$', self.search_phrase)
            self.tokens = split_unicode(self.phrase)

        # boolean search
        else:
            self.query_type = 'boolean'
            self.tokens = split_unicode(self.search_phrase)

    def excute_query(self):
        '''
        execute parsed query
        '''
        if self.query_type == 'phrase':
            self.query_result = self.index.objects.consequent(
                                                      token__in=self.tokens)

        elif self.query_type == 'proximity':
            self.query_result = self.index.objects.proximity(
                                                      token__in=self.tokens,
                                                      window=self.proximity)

        elif self.query_type == 'boolean':
            self.query_result = self.index.objects.intersect(
                                                      token__in=self.tokens)
        return self.post_query()

    def post_query(self):
        '''
        do post query processing according to `self.operator`
        '''
        return self.operator.operate(self.query_result, self.tokens)
