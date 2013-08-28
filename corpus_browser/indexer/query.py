from utils import Counter
from mongoengine import QuerySet


class TweetsQuerySet(QuerySet):

    def index(self, *args, **kwargs):
        '''
        invert query results to be ready for indexing
        TODO: performance optimization and enhance the algorithm
        '''
        self.filter(*args, **kwargs)  # delegate query to filter

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
        '''
        self = self.filter(*args, **kwargs)
        if not self:
            return set([])
        postings = [set(row.postings) for row in self]
        common_postings = postings[0].copy()
        for posting in postings[1:]:
            common_postings &= posting
        return common_postings

    def proximity(self, proximity_list):
        '''
        '''
        pass
