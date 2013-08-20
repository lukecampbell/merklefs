#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/objects.py
@description Definitions for the basic objects
'''

from mfs.types import MFSTypes

class MFSObjectHeader:
    '''
    MFS Object Header
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    res             |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |     res            |    res             |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    '''
    mfs_type = None

    @classmethod
    def deserialize(cls, string_buffer):
        offset = string_buffer.offset()
        mfs_type = string_buffer.read_uint(1)
        string_buffer.seek(offset)

        if mfs_type == MFSTypes.SymbolTable:
            from mfs.symbol_table import SymbolTableHeader
            return SymbolTableHeader.deserialize(string_buffer)
        elif mfs_type == MFSTypes.Datatype:
            from mfs.datatype import DatatypeHeader
            return DatatypeHeader.deserialize(string_buffer)
        elif mfs_type == MFSTypes.Dataspace:
            from mfs.dataspace import DataspaceHeader
            return DataspaceHeader.deserialize(string_buffer)
        raise TypeError("unrecognized object type")





class MFSObject:
    pass


