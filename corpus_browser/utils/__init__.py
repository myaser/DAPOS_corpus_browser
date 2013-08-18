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


def model_repr(model):
        representation = model.__dict__.copy()
        del representation['_entity_exists']
        del representation['_original_pk']
        del representation['_state']
        return representation.__repr__()
