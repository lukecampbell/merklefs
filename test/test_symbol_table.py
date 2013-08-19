#!/usr/bin/env python
from test.test_case import MFSTestCase
from test.performance import PerformanceTestCase

from mfs.symbol_table import SymbolTable, SymbolTableHeader
from mfs.exceptions import SerializationError
from mfs.string_buffer import StringBuffer
from tempfile import TemporaryFile
import numpy as np

class TestSymbolTable(MFSTestCase):
    def test_symbol_table(self):
        st = SymbolTable()

        st.add('root')
        self.assertRaises(SerializationError, st.add, 1)

    def test_symbol_table_write(self):
        st = SymbolTable()
        st.add('root')
        st.add('') # Null symbol
        st.add('time')
        st.add('time.units:seconds since 1900-01-01')
        st.add('lat')
        st.add('lat.units:degrees_north')
        st.add('lon.units:degrees_east')

        with TemporaryFile('w+b') as f:
            sb = st.serialize()
            sb.fwrite(f.fileno())

            f.seek(0)

            sb = StringBuffer(256)
            sb.fread(f.fileno())
            
            sb.seek(0)

            st2 = SymbolTable.deserialize(sb)

        self.assertEquals(st2.table, st.table)


        # Make assertions about the size
        # It should be on a word boundary


class PerformanceSymbolTable(PerformanceTestCase):
    def create_symbol_tables(self):
        st = SymbolTable()
        st.add('root')
        st.add('time')
        st.add('time.long_name:universal time')
        st.add('time.reference:UTC')
        st.add('time.units:minutes since 2000-01-01 00:00')
        st.add('ncells')
        st.add('ncells.long_name:sequential cell count')
        st.add('lon')
        st.add('lon.long_name:Cell longitude')
        st.add('lon.units:degrees_east')
        st.add('lat')
        st.add('lat.long_name:Cell latitude')
        st.add('lat.units:degrees_north')
        st.add('U')
        st.add('U.long_name:eastward water velocity')
        st.add('V')
        st.add('V.long_name:northward water velocity')
        with TemporaryFile('w+b') as f:
            st.serialize().fwrite(f.fileno())

            f.seek(0)

            header_sbuf = StringBuffer(16)
            header_sbuf.fread(f.fileno())
            header_sbuf.seek(0)

            header = SymbolTableHeader.deserialize(header_sbuf)

            f.seek(0)

            sbuf = StringBuffer( 16 + header.total_size)
            sbuf.fread(f.fileno())
            sbuf.seek(0)
            st2 = SymbolTable.deserialize(sbuf)

            self.assertEquals(st.table, st2.table)

    def test_create(self):
        for i in xrange(1000):
            self.profile(self.create_symbol_tables)

        # The symbol table creation, serialization and deserialization MUST BE FAST
        # If it takes longer than half a second to read and write 1000 then it's too slow
        self.assertTrue( sum(self.profile_context.stat_list) < 0.5) # Hard performance standard


