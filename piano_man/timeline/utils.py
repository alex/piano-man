from itertools import chain

def merge_sorted_iters(*iters, **kwargs):
    keys = kwargs['keys']
    reverse = kwargs.pop('reverse', False)
    def key_func(o):
        return getattr(o, keys[type(o)])
    return sorted(chain(*iters), key=key_func, reverse=reverse)
