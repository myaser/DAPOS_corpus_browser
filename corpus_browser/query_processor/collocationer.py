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

#     def extract_freq(self, w1, w2, queryset):
#         freq1 = len(queryset)
#         freq2 = self.index.objects.frequency(w2)
#         collocation_freq = self.index.objects.frequency(w1, w2, window=self.window)
# 
#         return (collocation_freq, (freq1, freq2), self.index.get_size())

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

        import pdb; pdb.set_trace()
#         return sorted(self.collocations(self.tokens, self.other_tokens, self.search_result),
#                       reverse=True, key=lambda item: item[1])
