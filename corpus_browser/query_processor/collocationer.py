from nltk.collocations import BigramAssocMeasures
from query_processor import Operator


import logging
logger = logging.getLogger()


class Collocationer(Operator):

    supported_scoring_algorithms = {
    't-score': BigramAssocMeasures.student_t,
    'mutual_information': BigramAssocMeasures.pmi,
    'log_likelihood': BigramAssocMeasures.likelihood_ratio,
    }

    def __init__(self, scoring_algorithm):
        self.scoring_algorithm = scoring_algorithm
        self.scoring_fn = self.supported_scoring_algorithms.get(
                                                    self.scoring_algorithm)

    def _other_tokens(self, queryset, tokens, window):
        documents = map(lambda posing: posing.document, queryset)
        other_tokens = set([])
        for document in documents:
            other_tokens = other_tokens | (set(document.tokens) - tokens)
        return other_tokens

    def extract_freq(self, w1, w2, queryset):
        freq1 = len(queryset)
        freq2 = self.index.objects.frequency(w2)
        collocation_freq = self.index.objects.frequency(w1, w2, window=self.window)

        return (collocation_freq, (freq1, freq2), self.index.get_size())

    def calc_score(self, tokens, other_token, queryset):
        try:
            return self.scoring_fn(*self.extract_freq(
                tokens,
                other_token,
                queryset
            ))
        except ValueError:
            logger.error('unable to calculate scoring algorithm %{0},'
                ' with requencies %{1}.'.format(
                    self.scoring_algorithm,
                    self.extract_freq(tokens, other_token, queryset)
                ))
            return 0

    def collocations(self, tokens, other_tokens, queryset):
        return  [
                (
                    (tokens, token),
                        self.calc_score(
                            tokens,
                            token,
                            queryset
                        )
                ) for token in other_tokens
            ]

    def operate(self, queryset, tokens, window=5, *args, **kwargs):
        self.queryset = queryset
        self.tokens = set(tokens)
        self.window = window
        self.other_tokens = self._other_tokens(self.queryset, self.tokens, self.window)

        return sorted(self.collocations(self.tokens, self.other_tokens, self.queryset),
                      reverse=True, key=lambda item: item[1])
