def normalize_attr(objs, new_attr, keys):
    def key_func(o):
        return getattr(o, keys[type(o)])
    for obj in objs:
        setattr(obj, new_attr, key_func(obj))
