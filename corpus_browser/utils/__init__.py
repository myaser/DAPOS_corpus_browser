from collections import Counter as StandardCounter
from _abcoll import Mapping
from django.forms.models import model_to_dict
from timeit import itertools


class Counter(StandardCounter):
    '''
    Counter subclass that allows update() through + operator
    '''

    def __add__(self, other):
        '''Add counts from two counters.
        '''
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


def document_repr(model):
    _dict = model.__dict__['_data']
    return _dict.__repr__()


def change_collection(collection=None):
    '''
    decorator to change db collection to support inheritance
    '''
    def wrap(cls):
        def new_class(collection):
            if collection:
                meta = cls.__bases__[0]._meta.copy()
                meta['collection'] = collection
                cls._meta = meta
            return cls
        return new_class(collection)
    return wrap


cache_keys = ['max_value', 'corpus_size', 'words_count', 'hapaxes']
def clear_cache():
    cache.delete_many(cache_keys)
