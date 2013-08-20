#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/datatype.py
@description Datatype block
'''

from mfs.objects import MFSObject, MFSObjectHeader
from mfs.types import MFSTypes
from mfs.string_buffer import StringBuffer

class DatatypeHeader(MFSObjectHeader):
    '''
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    datatype        |               flags                     |
    +-----------------------------------------------------------------------------------+
    |                                   size                                            |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    mfs_type   - MFSObject Type
    datatype   - The class of data
    flags      - flags for the datatype
    size       - the size in bytes of the datatype
    total_size - currently 0

    datatype:
      0x00 ubyte 
      0x01 byte  
      0x02 ushort 
      0x03 short
      0x04 uint
      0x05 int
      0x06 uint64
      0x07 int64
      0x08 float32
      0x09 double
      0x10 fixed-length string
    '''

    mfs_type   = None
    datatype   = None
    flags      = None
    size       = None
    total_size = 0

    def __init__(self, datatype, flags, size, total_size=0):
        self.mfs_type = MFSTypes.Datatype
        self.datatype = datatype
        self.flags = flags
        self.size = size
        self.total_size = total_size

    def serialize(self):
        sb = StringBuffer(16)
        sb.pack('<BBHIQ', self.mfs_type, self.datatype, self.flags, self.size, self.total_size)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        mfs_type = string_buffer.read_uint(1)
        if mfs_type != MFSTypes.Datatype:
            raise TypeError('object is not a datatype')
        datatype = string_buffer.read_uint(1)
        flags = string_buffer.read_uint(2)
        size = string_buffer.read_uint(4)
        total_size = string_buffer.read_uint(8)
        return cls(datatype, flags, size, total_size)

class MFSUByteType(DatatypeHeader):
    def __init__(self):
        datatype = 0x00
        flags = 0x00 # Little Endian unsigned
        size = 1
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSByteType(DatatypeHeader):
    def __init__(self):
        datatype = 0x01
        flags = 0x01 # Little endian, signed
        size = 1
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSUShortType(DatatypeHeader):
    def __init__(self):
        datatype = 0x02
        flags = 0x00 # Little Endian unsigned
        size = 2
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSShortType(DatatypeHeader):
    def __init__(self):
        datatype = 0x03
        flags = 0x01 # Little endian, signed
        size = 2
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSUIntType(DatatypeHeader):
    def __init__(self):
        datatype = 0x04
        flags = 0x00 # Little Endian unsigned
        size = 4
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSIntType(DatatypeHeader):
    def __init__(self):
        datatype = 0x05
        flags = 0x01 # Little endian, signed
        size = 4
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSUInt64Type(DatatypeHeader):
    def __init__(self):
        datatype = 0x06
        flags = 0x00 # Little Endian unsigned
        size = 8
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSInt64Type(DatatypeHeader):
    def __init__(self):
        datatype = 0x07
        flags = 0x01 # Little endian, signed
        size = 8
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSFloat32Type(DatatypeHeader):
    def __init__(self):
        datatype = 0x08
        flags = 0x00 # Little endian, no support for big endian at the moment
        size = 4
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class MFSDoubleType(DatatypeHeader):
    def __init__(self):
        datatype = 0x09
        flags = 0x00 # Little endian, no support for big endian at the moment
        size = 8
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)

class StringEncoding:
    ASCII = 0x00
    UTF8  = 0x01

class StringPadding:
    NULLTERM = 0x00 # Null Terminated String
    NULLPAD  = 0x01
    SPACEPAD = 0x02 # Not really supported

class MFSStringType(DatatypeHeader):
    def __init__(self, encoding=StringEncoding.ASCII, padding=StringPadding.NULLTERM):
        datatype = 0x10
        flags = encoding << 4 | padding
        size = 1
        total_size = 0
        DatatypeHeader.__init__(self, datatype, flags, size, total_size)




class Datatype(MFSObject):
    '''
    This may contain a property field but mostly it'll be used in VLEN situations which I won't support yet
    '''
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Datatype is not implemented")

