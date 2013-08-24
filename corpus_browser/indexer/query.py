from django.db import models
from utils import Counter


class TweetsQuerySet(models.query.QuerySet):

    def index(self):
        '''
        invert query results to be ready for indexing
        TODO: performance optimization and enhance the algorithm
        '''

        index = Counter()
        for tweet in self:
            tokens = tweet.tokens
            positions = range(len(tokens))
            for token, position in zip(tokens, positions):
                index.update({token: Counter(dict([(tweet.pk, [position])]))})
        return index


class IndexQuerySet(models.query.QuerySet):

    def intersect(self, *args, **kwargs):
        '''
        find documents that have all tokens of the query set.
        "AND boolean query"
        '''
        rows = self.filter(*args, **kwargs)
        if not rows:
            return set([])
        postings = [set(row.postings) for row in rows]
        common_postings = postings[0]
        for posting in postings[1:]:
            common_postings &= posting
        return common_postings

    def proximity(self, proximity_list):
        '''
        '''
        pass
