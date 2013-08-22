#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/attribute.py
@description Attribute block
'''

from mfs.objects import MFSObjectHeader, MFSObject
from mfs.types import MFSTypes
from mfs.string_buffer import StringBuffer

class AttributeHeader(MFSObjectHeader):
    '''
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    ver             |                name_size                |
    +-----------------------------------------------------------------------------------+
    |              datatype_size              |              dataspace_size             |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    mfs_type       - The MFSObject Type
    ver            - Attribute version (currently 0)
    name_size      - length in bytes of the name (not including the padding for word alignment)
    datatype_size  - size in bytes of the datatype message
    dataspace_size - size in bytes of the dataspace message
    total_size     - The size in bytes of the entire attribute block
    '''

    mfs_type = MFSTypes.Attribute
    ver = 0
    name_size = None
    datatype_size = None
    dataspace_size = None
    total_size = None

    attr = None

    def __init__(self, name_size, datatype_size, dataspace_size, total_size):
        self.name_size = name_size
        self.datatype_size = datatype_size
        self.dataspace_size = dataspace_size
        self.total_size = total_size

    def serialize(self):
        sb = StringBuffer(16 + self.total_size)
        sb.pack('<BBHHHQ', self.mfs_type, self.ver, self.name_size, self.datatype_size, self.dataspace_size, self.total_size)
        if self.attr is not None:
            sb.write(self.attr.serialize())
        sb.seek(0)
        return sb


    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        mfs_type = sb.read_uint(1)
        if not mfs_type == cls.mfs_type:
            raise TypeError('not an attribute header')
        ver = sb.read_uint(1)
        if ver != cls.ver:
            raise TypeError('attribute header version mismatch')
        name_size = sb.read_uint(2)
        datatype_size = sb.read_uint(2)
        dataspace_size = sb.read_uint(2)
        total_size = sb.read_uint(8)
        return cls(name_size, datatype_size, dataspace_size, total_size)


    def __len__(self):
        return 16 + self.total_size







    

class Attribute(MFSObject):
    '''
    +-----------------------------------------------------------------------------------+
    |                              name*                                                |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |                              datatype*                                            |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |                              dataspace*                                           |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |                              data*                                                |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
      * - Variable size

    name      - a fixed length string with null padding to the word boundary
    datatype  - A datatype object
    dataspace - A dataspace object
    data      - the raw data for this attribute
    '''

    pass

