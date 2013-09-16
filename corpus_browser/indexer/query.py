from utils import Counter
from mongoengine import QuerySet
import itertools
from types import StringTypes
from collections import Iterable
from copy import deepcopy


class TweetsQuerySet(QuerySet):

    def index(self, *args, **kwargs):
        '''
        invert query results to be ready for indexing
        TODO: performance optimization and enhance the algorithm
        '''
        self = self.filter(*args, **kwargs).select_related_documents()  # delegate query to filter

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

    def intersect(self, token__in=[]):
        '''
        find documents that have all tokens of the query set.
        "AND boolean query"
        TODO: performance enhancement
        '''

        queryset = self.filter(token__in=token__in).order_by().select_related_documents()

        if not queryset or len(queryset) != len(token__in):
            return []

        common = [index.as_result for index in queryset]
        return self._intersect(common[0], common[1:])

    def _intersect(self, result, other_results):
        all_results = [result] + other_results
        result = set(result)
        result = result.intersection(*other_results)
        for posting in result:
            for _posting in itertools.chain.from_iterable(all_results):
                if posting == _posting:
                    posting.positions.extend(_posting.positions)
        return list(result)

    def proximity(self, window=1, token__in=[]):
        '''
        do positional search and return documents that has all tokens of the
        query set near each other in window size
        '''
        common = self.intersect(token__in=token__in)
        return self._proximity(common, window)

    def _proximity(self, boolean_results, window=1):
        result = []
        for posting in boolean_results:
            positions_lists = zip(*posting.positions)[1]
            for item in itertools.product(*positions_lists):
                if max(item) - min(item) <= window:
                    result.append(posting)
        return result

    def consequent(self, token__in=[]):
        common = self.intersect(token__in=token__in)
        return self._consequent(token__in, common)

    def _consequent(self, token__in, boolean_results):
        num_tokens = len(token__in)
        result = []
        for posting in boolean_results:
            pos = dict(posting.positions)
            positions_lists = [pos[token] for token in token__in]

            for item in itertools.product(*positions_lists):
                start = item[0]

                if item == tuple(range(start, start + num_tokens)):
                    result.append(posting)
        return result

    def collocation_frequency(self, collocation_tokens, search_tokens, search_result, window=None):
        queryset = self.filter(token__in=collocation_tokens).select_related_documents()
        results = {}
        for index in queryset:
            collocation = self._intersect(index.as_result, [search_result])

            if window is None:
                # consequent in both directions
                collocation = self._consequent(
                               search_tokens + collocation_tokens, collocation)
                collocation += self._consequent(
                               collocation_tokens + search_tokens, collocation)
            if window > 0:
                collocation = self._proximity(collocation, window)

            results.update({index.token: len(collocation)})
        return results

    def select_related_documents(self):
        from indexer.models import Tweet
        # collect ids
        result = self.clone()
        ids = itertools.chain.from_iterable([[posting._data['document'].id for posting in index.postings] for index in result])

        # query documents
        docs = Tweet.objects.filter(id__in=ids)
        assert len(docs) == len(ids)
        tweets = dict(zip(ids, docs))

        # replace documents
        def derefrence(posting):
            posting._data['document'] = tweets[posting._data['document'].id]
            return posting

        for index in result:
            import pdb; pdb.set_trace()
            map(derefrence, index.postings)

        return result
