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
    symbols = None
    def __init__(self, entry_no=0, total_size=0):
        self.entry_no = entry_no
        self.total_size = total_size
        self.symbols = []

    def serialize(self):
        sb = StringBuffer(16 + self.total_size)
        sb.pack('<BBHIQ', self.mfs_type, 0, 0, self.entry_no, self.total_size)
        for symbol in self.symbols:
            sb.write(symbol.serialize())
        sb.seek(0)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        mfs_type = sb.read_uint(1)
        if not mfs_type == cls.mfs_type:
            raise TypeError("object is not a symbol table")
        sb.seek(sb.offset()+3)
        entry_no = sb.read_uint(4)
        total_size = sb.read_uint(8)
        return cls(entry_no, total_size)
    
    def add(self, symbol):
        if isinstance(symbol, basestring):
            if self.symbols:
                idx = self.symbols[-1].idx + 1
            else:
                idx = 0
            symbol_length = len(symbol)+1
            symbol = SymbolTableEntry(idx, symbol_length, symbol)
            return self.add(symbol)
        elif isinstance(symbol, SymbolTableEntry):
            self.entry_no += 1
            self.total_size += len(symbol)
            if self.total_size % 8 != 0:
                self.total_size += 8 - (self.total_size % 8)
            self.symbols.append(symbol)
        else:
            raise TypeError("unknown symbol")

    def deserialize_table(self, string_buffer):
        sb = string_buffer

        for i in xrange(self.entry_no):
            o = string_buffer.offset()
            if o % 8 != 0: # Align
                o += 8 - (o%8)
                string_buffer.seek(o)
            symbol = SymbolTableEntry.deserialize(sb)
            self.symbols.append(symbol)

    def __len__(self):
        return 16 + self.total_size


class SymbolTableEntry(MFSObject):
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

    idx           = None
    symbol_length = None
    symbol        = None

    def __init__(self, idx=0, symbol_length=0, symbol=''):
        self.idx = idx
        if symbol_length < len(symbol):
            raise ValueError('symbol length is less than required')
        self.symbol_length = max(len(symbol)+1, symbol_length)
        self.symbol = symbol


    def serialize(self):
        sb = StringBuffer(8 + self.symbol_length)
        sb.pack('<HHI', self.idx, 0, max(len(self.symbol)+1, self.symbol_length)) # Account for null-terminator
        sb.write(self.symbol)
        sb.seek(0)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        sb = string_buffer
        idx = sb.read_uint(2)
        sb.read_uint(2)
        symbol_length = sb.read_uint(4)
        symbol = sb.raw_read(symbol_length, strip_null=True)
        return cls(idx,symbol_length,symbol)

    def __len__(self):
        return 8 + self.symbol_length






