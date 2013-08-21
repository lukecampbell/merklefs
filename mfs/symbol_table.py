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
            raise TypeError("object is not a symbol table")
        sb.seek(sb.offset()+3)
        entry_no = sb.read_uint(4)
        total_size = sb.read_uint(8)
        return cls(entry_no, total_size)

    def read_symbol_table(self, string_buffer):
        sb = string_buffer
        symbols = []

        for i in xrange(self.entry_no):
            o = string_buffer.offset()
            if o % 8 != 0: # Align
                o += 8 - (o%8)
                string_buffer.seek(o)
            symbol = SymbolTableEntry.deserialize(sb)
            symbols.append(symbol)

        return SymbolTable(self, symbols)



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


class SymbolTable(MFSObject):
    header = None
    symbols = None
    def __init__(self, symbol_table_header=None, symbols=None):
        if symbols is None:
            symbols = []
        if symbol_table_header is None:
            total_size = 0
            for i in symbols:
                total_size += len(i)
                if total_size % 8 != 0:
                    total_size += 8 - (total_size % 8)
            symbol_table_header = SymbolTableHeader(len(symbols), total_size)

        self.header = symbol_table_header
        self.symbols = symbols

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
            self.header.entry_no += 1
            self.header.total_size += len(symbol)
            if self.header.total_size % 8 != 0:
                self.header.total_size += 8 - (self.header.total_size % 8)
            self.symbols.append(symbol)
        else:
            raise TypeError("unknown symbol")

    def serialize(self):
        header_sb = self.header.serialize()
        symbol_buffers = [i.serialize() for i in self.symbols]

        sb = StringBuffer( len(header_sb) + self.header.total_size)
        sb.write(header_sb)
        for i in symbol_buffers:
            sb.write(i)
        return sb

    @classmethod
    def deserialize(cls, string_buffer):
        header = SymbolTableHeader.deserialize(string_buffer)
        return header.read_symbol_table(string_buffer)

    def __len__(self):
        return len(self.symbols)

    def __getitem__(self, i):
        return self.symbols[i]





