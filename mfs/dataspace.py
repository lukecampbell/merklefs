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
    
    dataspaces = []
    def __init__(self, shape=0, flags=0):
        self.mfs_type = MFSTypes.Dataspace
        self.ver = 0
        self.flags = flags
        if isinstance(shape, (tuple, list)):
            dims = len(shape)
            self.dims = dims
            self.total_size = dims * 8
            self.dataspaces = [Dataspace(i) for i in shape]
        elif isinstance(shape, int):
            dims = shape
            self.dims = dims
            self.total_size = dims * 8
            self.dataspaces = [Dataspace(0) for i in xrange(dims)]
        else:
            raise ValueError('invalid shape')


    def serialize(self):
        sb = StringBuffer(16 + self.total_size)
        sb.pack('<BBBBIQ', self.mfs_type, self.ver, self.dims, self.flags, 0, self.total_size)
        for ds in self.dataspaces:
            sb.write(ds.serialize())
        sb.seek(0)
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

        return cls(dims, flags)

    def deserialize_dataspaces(self, string_buffer):
        sb = string_buffer
        for i in xrange(self.dims):
            self.dataspaces[i] = Dataspace.deserialize(sb)

    def __len__(self):
        return self.total_size + 16


class Dataspace(MFSObject):
    '''
    +-----------------------------------------------------------------------------------+
    |                               dim_size                                            |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+

    dim_size - Number of elements the dimension contains
    '''

    dim_size = None

    def __init__(self, dim_size):
        self.dim_size = dim_size

    def serialize(self):
        sb = StringBuffer(8)
        sb.pack('<Q', self.dim_size)
        sb.seek(0)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        dim_size = sb.read_uint(8)
        return cls(dim_size)


    def __len__(self):
        return 8

