#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/dataspace.py
@description Dataspace implementation
'''


from mfs.objects import MFSObject, MFSObjectHeader
from mfs.types import MFSTypes
from mfs.string_buffer import StringBuffer

class DataspaceHeader(MFSObjectHeader):
    '''
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |         ver        |       dims         |       flags        |
    +-----------------------------------------------------------------------------------+
    |                                  res                                              |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+

    mfs_type   - MFSObject Type
    ver        - dataspace version
    dims       - number of dimensions (0 is for scalars)
    flags      - dataspace flags
    res        - reserved
    total_size - total size in bytes of the dataspace object
    '''

    mfs_type   = None
    ver        = None
    dims       = None
    flags      = None
    total_size = None
    
    def __init__(self, dims=0, flags=0, total_size=0):
        self.mfs_type = MFSTypes.Dataspace
        self.ver = 0
        self.dims = dims
        self.flags = flags
        self.total_size = total_size

    def serialize(self):
        sb = StringBuffer(16)
        sb.pack('<BBBBIQ', self.mfs_type, self.ver, self.dims, self.flags, 0, self.total_size)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        mfs_type = sb.read_uint(1)
        if mfs_type != MFSTypes.Dataspace:
            raise TypeError('object is not a dataspace')
        ver = sb.read_uint(1)
        if ver != 0:
            raise TypeError('unsupported dataspace version')
        dims = sb.read_uint(1)
        flags = sb.read_uint(1)
        sb.read_uint(4)
        total_size = sb.read_uint(8)

        return cls(dims, flags, total_size)


class Dataspace(MFSObject):
    pass


