#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/file.py
@description Merkle File
'''

from mfs.objects import MFSObjectHeader
import os

class MerkleFile:
    '''
    File wrapper for a Merkle Object
    '''
    path = None
    merkle_object_header = None
    def __init__(self, path, merkle_object_header):
        if not os.path.isdir(path):
            raise IOError('bad path: not a directory')
        self.path = path
        self.merkle_object_header = merkle_object_header

    def open(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

