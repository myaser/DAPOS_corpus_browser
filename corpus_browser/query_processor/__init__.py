from mi import MutualInformation
from llh import LogLikeliHood
from tscore import TTest
from ngram import NGram


class QueryProcessor(object):
    def __init__(self, strategy):
        '''
        apply strategy design pattern for processing core
        '''
        self.strategy = strategy

    def calc(self, *args, **kwargs):
        return self.strategy.calc(*args, **kwargs)


def make_query_processor(algorithm):
    '''
    take the name of algorithm and return a QueryProcessor object
    with chosen algorithm as processing core.
    now, you can use it like this
    value = make_query_processor(:replaceable:`someAlgoOption`).calc(....)
    '''
    strategy = {
        'mutual_information': MutualInformation,
        'loglikelihood': LogLikeliHood,
        't-score': TTest,
        'ngram': NGram
    }.get(algorithm)
    return QueryProcessor(strategy())
