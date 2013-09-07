from nltk.probability import FreqDist


class IndexFreqDist(FreqDist):

    def __init__(self, index=None):
        self.index = index

    def __getitem__(self, sample):
        if isinstance(sample, tuple):
            return len(self.index.consequent(token__in=sample))
        else:
            return self.index.objects.get(token=sample).term_frequency or 0

    def max(self):
        pass

    def freq(self, sample):
        pass

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

