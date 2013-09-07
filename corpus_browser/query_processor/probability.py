from nltk.probability import FreqDist


class IndexFreqDist(FreqDist):

    def __init__(self, samples=None):
        raise NotImplementedError()

    def inc(self, sample, count=1):
        raise NotImplementedError()

    def __setitem__(self, sample, value):
        raise NotImplementedError()

    def N(self):
        raise NotImplementedError()

    def B(self):
        raise NotImplementedError()

    def samples(self):
        raise NotImplementedError()

    def hapaxes(self):
        raise NotImplementedError()

    def Nr(self, r, bins=None):
        raise NotImplementedError()

    def _cache_Nr_values(self):
        raise NotImplementedError()

    def _cumulative_frequencies(self, samples=None):
        raise NotImplementedError()

    def freq(self, sample):
        raise NotImplementedError()

    def max(self):
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

    def __getitem__(self, sample):
        raise NotImplementedError()
