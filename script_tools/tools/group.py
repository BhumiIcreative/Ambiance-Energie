# coding: utf-8


def groupby(recordset, key):
    keys = key.replace(' ', '').split(',')
    first_key = keys[0]
    res = dict()
    for record in recordset:
        key_val = getattr(record, first_key)
        if key_val not in res:
            res[key_val] = record.env[record._name]
        res[key_val] |= record
    if len(keys) > 1:
        for key in res:
            res[key] = groupby(res[key], ','.join(keys[1:]))
    return res
