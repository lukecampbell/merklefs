#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/symbol_table.py
@description Implementation for symbol table
'''

from mfs.objects import MFSObject, MFSObjectHeader
from mfs.exceptions import SerializationError
from mfs.string_buffer import StringBuffer
from mfs.types import MFSTypes

class SymbolTableHeader(MFSObjectHeader):
    '''
    Symbol Table Header
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    res             |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |                               entry_no                                            |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+

    mfs_type   - MFS Object Type
    res        - reserved
    entry_no   - Number of entries
    total_size - Total size in bytes of table after this field
    '''

    mfs_type = MFSTypes.SymbolTable
    entry_no = 0
    total_size = 0
    def __init__(self, entry_no=0, total_size=0):
        self.entry_no = entry_no
        self.total_size = total_size

    def serialize(self):
        sb = StringBuffer(16)
        sb.pack('<BBHIQ', self.mfs_type, 0, 0, self.entry_no, self.total_size)
        sb.seek(0)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        mfs_type = sb.read_uint(1)
        if not mfs_type == cls.mfs_type:
            print mfs_type
            raise TypeError("object is not a symbol table")

        sb.seek(sb.offset()+3)
        entry_no = sb.read_uint(4)
        total_size = sb.read_uint(8)


        return cls(entry_no, total_size)




class SymbolTable(MFSObject):
    '''
    Symbol Table Entry
    +-----------------------------------------------------------------------------------+
    |              idx                        |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |                               symbol_length                                       |
    +-----------------------------------------------------------------------------------+
    |                               symbol*                                             |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
        * - Variable length and aligned on a 8-byte boundary.

    idx           - Index (key) of symbol
    res           - Reserved
    symbol_length - Length in bytes of symbol (not including the 0 - padding for 
                    8-byte alignment)
    '''

    table = []
    def __init__(self, initializer=None):
        self.table = []
        if initializer:
            self.table.extend(initializer)

    def add(self, symbol):
        if not isinstance(symbol,basestring):
            raise SerializationError("Failed to serialize symbol")

        self.table.append(symbol)
        return self

    def __getitem__(self, item):
        return self.table.__getitem__(item)

    def get_header(self):
        total_size = 0
        for i,sym in enumerate(self.table):
            total_size += 4 # Short for the index and 2 for reserved
            total_size += 4 # size_t for string length
            total_size += len(sym)
            if total_size % 8 != 0:
                total_size += 8 - (total_size % 8)
        return SymbolTableHeader(len(self.table), total_size)


    def serialize(self):
        total_size = 0
        total_size += 16 # Table header
        header = self.get_header()
        total_size += header.total_size
        sb = StringBuffer(total_size)
        sb.write(header.serialize())
        for i, sym in enumerate(self.table):
            sb.pack('<HH', i, 0) # Short | reserved
            sb.pack('<I', len(sym))
            sb.write(sym)
            if sb.offset() % 8 != 0: # Align on word-boundary
                o = sb.offset()
                sb.seek(o + (8 - (o % 8)))

        return sb

    @classmethod
    def deserialize(cls, string_buf):
        entries = []
        sb = string_buf
        
        header = StringBuffer(sb.raw_read(16))
        header = SymbolTableHeader.deserialize(header)

        for i in xrange(header.entry_no):
            idx = sb.read_uint(2)
            
            sb.read_uint(2) # Reserved
            
            buflen = sb.read_uint(4)
            if buflen % 8 != 0:
                buflen += 8 - (buflen % 8)
            buf = sb.raw_read(buflen)
            null = buf.find('\x00')
            if null > 0:
                buf = buf[:null]
            for j in xrange(idx - len(entries)):
                entries.append('')

            entries.append(buf)
        return cls(entries)

