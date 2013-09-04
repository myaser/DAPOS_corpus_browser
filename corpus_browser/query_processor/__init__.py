class QueryProcessor:

    def __init__(self, search_phrase='', operator=None):
        self.search_phrase = search_phrase  # search phrase entered by user
        self.operator = operator  # operator executed after query to do(concordance,OR collocation,OR N-gram)

    def parse_search(self, search_phrase=''):
        '''
        process the search phrase and decide what type of
        query (boolean, proximity, phrase) should be done
        '''
        self.query_type
        self.tokens
        pass

    def excute_query(self):
        '''
        excute parsed query
        '''
        self.queryset
        pass

    def post_query(self):
        '''
        do post query processing according to `self.operator`
        '''
        pass


class Operator(object):
    def operate(self):
        pass
