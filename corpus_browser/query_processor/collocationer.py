from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from collections import Iterable
from types import StringTypes
from indexer.models import MainIndex

class Operator(object):
    '''
    operator executed after query to do(concordance,OR collocation,OR N-gram)
    '''

    @classmethod
    def from_str(cls, operator):
        return {
            'collocation': Collocationer,
            'concordance': Concordance,
            'ngram': Ngram,
        }.get(operator)()

    def operate(self):
        raise NotImplementedError()


class Collocationer(Operator):

    supported_scoring_algorithms = {
    't-score': BigramAssocMeasures.student_t,
    'mutual_information': BigramAssocMeasures.pmi,
    'log_likelihood': BigramAssocMeasures.likelihood_ratio,
    }

    def _other_tokens(self, queryset, window):
        documents = map(lambda posing: posing.document, queryset)
        other_tokens = set([])
        for document in documents:
            other_tokens = other_tokens | (set(document.tokens) - self.tokens)
        return other_tokens

    def extract_freq(self, w1, w2):
        freq1 = len(self.queryset)
        freq2 = MainIndex.objects.frequency(w2)
        collocation_freq = MainIndex.objects.frequency(w1, w2, window=self.window)

        return (collocation_freq, (freq1, freq2), MainIndex.get_size())

    def collocations(self, tokens,other_tokens):
        return  [
                (
                    (self.tokens, token),
                        self.scoring_fn(*self.extract_freq(
                        self.tokens,
                        token)
                    )
                ) for token in self.other_tokens
            ]

    def operate(self, queryset, tokens, scoring_algorithm, window=5):
        self.queryset = queryset
        self.scoring_fn = self.supported_scoring_algorithms.get(
            scoring_algorithm
        )
        self.window = window
        self.tokens = set(tokens)
        self.other_tokens = self._other_tokens(queryset, self.window)

        return sorted(self.collocations(self.tokens, self.other_tokens), reverse=True, key=lambda item: item[1])


class Concordance(Operator):
    pass


class Ngram(Operator):
    pass
