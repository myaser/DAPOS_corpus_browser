from utils import Counter
from mongoengine import QuerySet
import itertools
from utils.decorators import get_or_cache
from types import StringTypes
from collections import Iterable


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

    def add_postings(self, token, postings):
        index_entery = self.get_or_create(token=token)[0]
        index_entery.postings.extend(postings)
        index_entery.save()

    def _collect_tokens(self, coll):
        result = []
        for item in coll:
            if isinstance(item, StringTypes):
                result.append(item)
            elif isinstance(item, Iterable):
                result += self._collect_tokens(item)
            else:
                raise ValueError('tokens should be string of collection of strings')
        return result

    def _collect_freq(self, tokens_list):
        '''
            simple implementation
            results are aproximated not exact !
            expected tokens_list: intersect or aproximity methods output !!
        '''
        return len(tokens_list)

    def frequency(self, *tokens, **kwargs):
        window = kwargs.pop('window', None)
        if len(tokens) == 1 and isinstance(tokens[0], StringTypes):
            return self.get(token=tokens[0]).term_frequency
        else:
            tokens = self._collect_tokens(tokens)
            if window is None:
                return self._collect_freq(self.consequent(token__in=tokens))
            elif window == 0:
                return self._collect_freq(self.intersect(token__in=tokens))
            return self._collect_freq(self.proximity(window=window, token__in=tokens))

    def intersect(self, *args, **kwargs):
        '''
        find documents that have all tokens of the query set.
        "AND boolean query"
        TODO: performance enhancement
        '''
        self = self.filter(*args, **kwargs).order_by()
        if not self:
            return []
        self = [index.as_result for index in self]
        result, remaining = set(self[0]), self[1:]

        result = result.intersection(*remaining)
        for posting in result:
            for _posting in list(itertools.chain.from_iterable(self)):
                    if posting == _posting:
                        posting.positions.extend(_posting.positions)
        return list(result)

    def proximity(self, *args, **kwargs):
        '''
        do positional search and return documents that has all tokens of the
        query set near each other in window size
        '''
        window = kwargs.pop('window', 1)
        common = self.intersect(*args, **kwargs)
        result = []
        for posting in common:
            positions_lists = zip(*posting.positions)[1]
            for item in itertools.product(*positions_lists):
                if max(item) - min(item) <= window:
                    result.append(posting)
        return result

    def consequent(self, *args, **kwargs):
        # TODO:
        return self.proximity(*args, **kwargs)
