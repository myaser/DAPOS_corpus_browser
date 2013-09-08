from nltk.probability import FreqDist
from django.core.cache import cache
from utils.decorators import get_or_cache
from django.utils.decorators import method_decorator


class IndexFreqDist(FreqDist):

    def __init__(self, index=None):
        self.index = index

    def __getitem__(self, sample):
        if isinstance(sample, tuple):
            return len(self.index.consequent(token__in=sample))  # it will work with ngrams but won't with collocations!
        else:
            return self.index.objects.get(token=sample).term_frequency or 0

    def freq(self, sample):
        N = self.N()
        if N < 1:
            return 0
        return float(self[sample]) / N

    @method_decorator(get_or_cache('max_value'))
    def max(self):
        max_token = self.index.objects.order_by("-term_frequency").first()
        return (max_token.token, max_token.term_frequency)

    def inc(self, sample, count=1):
        raise NotImplementedError()

    def __setitem__(self, sample, value):
        raise NotImplementedError()

    @method_decorator(get_or_cache('corpus_size'))
    def N(self):
        return sum(map(lambda term: term.term_frequency, self.index.objects))

    @method_decorator(get_or_cache('words_count'))
    def B(self):
        return self.index.objects.count()

    def samples(self):
        raise NotImplementedError()

    @method_decorator(get_or_cache('hapaxes'))
    def hapaxes(self):
        return self.Nr(1)

    def Nr(self, r, bins=None):
        if r < 0: raise IndexError, 'FreqDist.Nr(): r must be non-negative'

        # Special case for Nr(0):
        if r == 0:
            if bins is None: return 0
            else: return bins-self.B()

        return self.index.objects.get(term_frequency=r).count()

    def _cache_Nr_values(self):
        raise NotImplementedError()

    def _cumulative_frequencies(self, samples=None):
        raise NotImplementedError()

    def plot(self, *args, **kwargs):
        raise NotImplementedError()

    def tabulate(self, *args, **kwargs):
        raise NotImplementedError()

    def _sort_keys_by_value(self):
        raise NotImplementedError()

    def keys(self):
        raise NotImplementedError()

    def values(self):
        raise NotImplementedError()

    def items(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def iterkeys(self):
        raise NotImplementedError()

    def itervalues(self):
        raise NotImplementedError()

    def iteritems(self):
        raise NotImplementedError()

    def copy(self):
        raise NotImplementedError()

    def update(self, samples):
        raise NotImplementedError()

    def pop(self, other):
        raise NotImplementedError()

    def popitem(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def _reset_caches(self):
        raise NotImplementedError()

    def __add__(self, other):
        raise NotImplementedError()

    def __le__(self, other):
        raise NotImplementedError()

    def __lt__(self, other):
        raise NotImplementedError()

    def __ge__(self, other):
        raise NotImplementedError()

    def __gt__(self, other):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

