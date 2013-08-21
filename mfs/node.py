#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/node.py
@description Merkle Node
'''

from mfs.objects import MFSObject, MFSObjectHeader
from mfs.string_buffer import StringBuffer
from mfs.types import MFSTypes

class MerkleNodeHeader(MFSObjectHeader):
    '''
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    version         |              children                   |
    +-----------------------------------------------------------------------------------+
    |                               signature                                           |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+

    mfs_type   - MFS Object Type (0x02 in this case)
    version    - Node version number, currently 0
    children   - number of children that the node contains
    total_size - total size in bytes of the node
    '''
    signature  = '.MFS'
    version    = 0
    total_size = 0
    objects    = []
    children   = 0
    mfs_type   = MFSTypes.MerkleNode

    def __init__(self):
        self.total_size = 0
        self.objects = []
        self.children = 0

    def serialize(self):
        sb = StringBuffer(16 + self.total_size)
        sb.pack('<BBH', self.mfs_type, self.version, self.children)
        sb.write(self.signature)
        sb.pack('<Q', self.total_size)
        for o in self.objects:
            sb.write(o.serialize())
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        mfs_type = sb.read_uint(1)
        if mfs_type != cls.mfs_type:
            raise TypeError('not a node header')
        version = sb.read_uint(1)
        if version != cls.version:
            raise TypeError('version mismatch')
        children = sb.read_uint(2)
        signature = sb.raw_read(4)
        if signature != cls.signature:
            raise TypeError('signature mismatch')

        total_size = sb.read_uint(8)

        inst = cls()
        inst.total_size = total_size
        inst.children = children
        return inst

    def deserialize_children(self, string_buffer):
        sb = string_buffer
        for i in xrange(self.children):
            o = MerkleNode.deserialize(sb)
            self.objects.append(o)

    def add_child(self, merkle_node):
        self.total_size += len(merkle_node)
        self.children += 1 
        self.objects.append(merkle_node)

    def delete_child(self, sha):
        for o in self.objects:
            if o.sha == sha:
                o.mfs_type = MFSTypes.Nil # Delete it



class MerkleNode(MFSObject):
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
        sha = sb.raw_read(20)

        return cls(mfs_type, mode, flags, sha)

    def serialize(self):
        sb = StringBuffer(24)
        sb.pack('<BBH', self.mfs_type, self.mode, self.flags)
        sb.write(self.sha)
        sb.seek(0)

        return sb
        
    def __len__(self): 
        return 24

