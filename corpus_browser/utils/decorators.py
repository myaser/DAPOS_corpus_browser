from django.core.cache import cache
from functools import partial, wraps


def _get_or_cache(key, fn, *args, **kwargs):
    @wraps(fn)
    def wrapper(*arg, **kwargs):
        if cache.get(key):
            return cache.get(key)

        result = fn(*arg, **kwargs)
        cache.set(key, result)
        return result

    return wrapper

get_or_cache = lambda key: partial(_get_or_cache, key)
