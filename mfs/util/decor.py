#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/util/decor.py
@description Decorators
'''


import functools

def not_implemented(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError('%s not implemented' % func.__name__)
    return wrapper

