from collections import Counter as StandardCounter
from _abcoll import Mapping


class Counter(StandardCounter):
    '''
    Counter subclass that allows update() through + operator
    '''

    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})

        '''
#         import pdb; pdb.set_trace()
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            if elem in other.keys():
                newcount = count + other[elem]
            else:
                newcount = count

            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return result

    def update(self, iterable=None, **kwds):

        if iterable is not None:
            if isinstance(iterable, Mapping):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, Counter()) + count
                else:
                    super(Counter, self).update(iterable)  # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)


def model_repr(model):
    _dict = model.__dict__
    representation = {k: v for k, v in _dict.items() if '__' not in k}
    return representation.__repr__()
