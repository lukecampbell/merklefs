#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/hl/file.py
@description High Level File definition
'''

from mfs.hl.group import MFSGroup
from mfs.util.decor import not_implemented

class MFSFile(MFSGroup):
    @not_implemented
    def __init__(self, *args, **kwargs):
        pass

    @not_implemented
    def create_file(self, *args, **kwargs):
        pass

    @not_implemented
    def close(self, *args, **kwargs):
        pass

