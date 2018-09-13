d = {'a': 1, 'b': {'c': 2}, 'd': ['hi', {'foo': 'bar'}]}


def obj_dic(d):
    top = type('testBean', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, obj_dic(j))
        elif isinstance(j, seqs):
            setattr(top, i,
                    type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top


x = obj_dic(d)
print(x)
