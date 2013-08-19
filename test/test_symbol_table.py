#!/usr/bin/env python
from test.test_case import MFSTestCase

from mfs.symbol_table import SymbolTable
from mfs.exceptions import SerializationError
from mfs.string_buffer import StringBuffer
from tempfile import TemporaryFile

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


