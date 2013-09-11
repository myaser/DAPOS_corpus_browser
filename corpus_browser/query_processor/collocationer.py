from nltk.collocations import BigramAssocMeasures
from query_processor import Operator


class Collocationer(Operator):

    supported_scoring_algorithms = {
    't-score': BigramAssocMeasures.student_t,
    'mutual_information': BigramAssocMeasures.pmi,
    'log_likelihood': BigramAssocMeasures.likelihood_ratio,
    }

    def __init__(self, scoring_algorithm, window=5):
        self.scoring_algorithm = scoring_algorithm
        self.window = window

    def _other_tokens(self, queryset, window):
        documents = map(lambda posing: posing.document, queryset)
        other_tokens = set([])
        for document in documents:
            other_tokens = other_tokens | (set(document.tokens) - self.tokens)
        return other_tokens

    def extract_freq(self, w1, w2):
        freq1 = len(self.queryset)
        freq2 = self.index.objects.frequency(w2)
        collocation_freq = self.index.objects.frequency(w1, w2, window=self.window)

        return (collocation_freq, (freq1, freq2), self.index.get_size())

    def collocations(self, tokens, other_tokens):
        return  [
                (
                    (self.tokens, token),
                        self.scoring_fn(*self.extract_freq(
                        self.tokens,
                        token)
                    )
                ) for token in self.other_tokens
            ]

    def operate(self, queryset, tokens):
        self.queryset = queryset
        self.scoring_fn = self.supported_scoring_algorithms.get(
                                                    self.scoring_algorithm)
        self.tokens = set(tokens)
        self.other_tokens = self._other_tokens(self.queryset, self.window)

        return sorted(self.collocations(self.tokens, self.other_tokens),
                      reverse=True, key=lambda item: item[1])
