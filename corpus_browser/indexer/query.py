from utils import Counter
from mongoengine import QuerySet
import itertools


class TweetsQuerySet(QuerySet):

    def index(self, *args, **kwargs):
        '''
        invert query results to be ready for indexing
        TODO: performance optimization and enhance the algorithm
        '''
        self = self.filter(*args, **kwargs)  # delegate query to filter

        index = Counter()
        for tweet in self:
            tokens = tweet.tokens
            positions = range(len(tokens))
            for token, position in zip(tokens, positions):
                index.update({token: Counter(dict([(tweet.pk, [position])]))})
        return index


class IndexQuerySet(QuerySet):

    def intersect(self, *args, **kwargs):
        '''
        find documents that have all tokens of the query set.
        "AND boolean query"
        TODO: performance enhancement
        '''
        self = self.filter(*args, **kwargs).order_by()

        self = [index.as_result for index in self]
        result, remaining = set(self[0]), self[1:]

        result = result.intersection(*remaining)
        for posting in result:
            for _posting in list(itertools.chain.from_iterable(self)):
                    if posting == _posting:
                        posting.positions.extend(_posting.positions)
        return result

    def proximity(self, *args, **kwargs):
        '''
        do positional search and return documents that has all tokens of the
        query set near each other
        '''
        result = self.intersect(*args, **kwargs)


