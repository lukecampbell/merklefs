#!/usr/bin/env python
from test.test_case import MFSTestCase
from test.performance import PerformanceTestCase

from mfs.objects import MFSObjectHeader
from mfs.symbol_table import SymbolTableHeader
from mfs.exceptions import SerializationError
from mfs.string_buffer import StringBuffer
from tempfile import TemporaryFile
from nose.plugins.attrib import attr
import random

@attr('unit')
class TestSymbolTable(MFSTestCase):
    def test_symbol_table(self):
        st = SymbolTableHeader()

        st.add('root')
        self.assertRaises(TypeError, st.add, 1)

    def test_symbol_table_write(self):
        st = SymbolTableHeader()
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

            sb = StringBuffer.from_file(f.fileno(), 16)
            header = MFSObjectHeader.deserialize(sb)

            symbol_buf = StringBuffer.from_file(f.fileno(), header.total_size)
            header.deserialize_table(symbol_buf)

        for i in xrange(len(st.symbols)):
            self.assertEquals(st.symbols[i].symbol, header.symbols[i].symbol)

@attr('perf')
class PerformanceSymbolTable(PerformanceTestCase):
    def create_symbol_tables(self):
        st = SymbolTableHeader()
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

            sb = StringBuffer.from_file(f.fileno(),16)

            header = MFSObjectHeader.deserialize(sb)
            symbol_buf = StringBuffer.from_file(f.fileno(), header.total_size)
            header.deserialize_table(symbol_buf)
            i = random.randint(0, len(st.symbols)-1)
            self.assertEquals(st.symbols[i].symbol, header.symbols[i].symbol)

    def test_create(self):
        for i in xrange(10): # Load the libraries and warm up the CPU
            self.create_symbol_tables()

        for i in xrange(1000):
            self.profile(self.create_symbol_tables)

        # The symbol table creation, serialization and deserialization MUST BE FAST
        # If it takes longer than half a second to read and write 1000 then it's too slow
        self.assertTrue( sum(self.profile_context.stat_list) < 0.5) # Hard performance standard


