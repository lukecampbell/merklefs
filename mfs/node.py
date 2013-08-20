#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/node.py
@description Merkle Node
'''

from mfs.string_buffer import StringBuffer

class MerkleNode:
    '''
    +-----------------------------------------------------------------------------------+
    |                               signature                                           |
    +-----------------------------------------------------------------------------------+
    |     version        |    res             |              children                   |
    +-----------------------------------------------------------------------------------+
    |      mfs_type      |     mode           |              flags                      |
    +-----------------------------------------------------------------------------------+
    |                               sha                                                 |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |      mfs_type      |     mode           |              flags                      |
    +-----------------------------------------------------------------------------------+
    |                               sha                                                 |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
                                             ...
    +-----------------------------------------------------------------------------------+
    |      mfs_type      |     mode           |              flags                      |
    +-----------------------------------------------------------------------------------+
    |                               sha                                                 |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+

    Each sha is 20 bytes
    '''

    signature = '.MFS'
    version = 0
    objects = []

class MerkleObject:
    '''
    +-----------------------------------------------------------------------------------+
    |      mfs_type      |     mode           |              flags                      |
    +-----------------------------------------------------------------------------------+
    |                               sha                                                 |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    '''
    mfs_type = None
    mode = None
    flags = None
    sha = None

    def __init__(self, mfs_type, mode, flags, sha):
        self.mfs_type = mfs_type
        self.mode = mode
        self.flags = flags
        self.sha = sha

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        mfs_type = sb.read_uint(1)
        mode = sb.read_uint(1)
        flags = sb.read_uint(2)
        sha = sb.read_raw(20)

        return cls(mfs_type, mode, flags, sha)

    def serialize(self):
        sb = StringBuffer(24)
        sb.pack('<BBH', self.mfs_type, self.mode, self.flags)
        sb.write(self.sha)

        return sb
        


