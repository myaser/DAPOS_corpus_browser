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

    def operate(self, queryset, tokens, window=5, *args, **kwargs):

        other_tokens = self._other_tokens(queryset, set(tokens), window)

        collocation_frequency = self.index.objects.collocation_frequency(
                                                     other_tokens, tokens,
                                                     queryset, window=window)

        search_tokens_freq = len(queryset)
        other_tokens_freqs = {index.token: index.term_frequency for index in
                  self.index.objects.filter(token__in=other_tokens)
                                    .only('token', 'term_frequency')}
        corpus_size = self.index.get_size()

        collocations = {}
        for token in other_tokens:
            score_params = (collocation_frequency[token],
             (search_tokens_freq, other_tokens_freqs[token]), corpus_size)
            collocations.update({token: self.scoring_fn(*score_params)})

        collocations = sorted(collocations.items(),
                              key=lambda coll: coll[1], reverse=True)
        return collocations
