#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/hl/attribute.py
@description High Level Attribute Definition
'''

from mfs.util.decor import not_implemented

class MFSAttribute:
    @not_implemented
    def __init__(self, *args, **kwargs):
        pass

    @not_implemented
    def __getitem__(self, key):
        pass

    @not_implemented
    def __setitem__(self, key, value):
        pass


