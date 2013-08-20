#!/usr/bin/env python
'''
@author Luke Campbell
@file test/test_datatype.py
@description Datatype block tests
'''

from test.test_case import MFSTestCase
from test.performance import PerformanceTestCase
from mfs.datatype import DatatypeHeader, MFSUByteType, MFSByteType, MFSUShortType
from mfs.datatype import MFSShortType, MFSUIntType, MFSIntType, MFSUInt64Type, MFSInt64Type
from mfs.datatype import MFSFloat32Type, MFSDoubleType, MFSStringType
from mfs.objects import MFSObjectHeader
from mfs.string_buffer import StringBuffer
from tempfile import TemporaryFile
from nose.plugins.attrib import attr


@attr('unit')
class TestDatatype(MFSTestCase):

    def header_check(self, f, dtype_h, datatype, flags, size, total_size):
        sb = dtype_h.serialize()
        sb.fwrite(f.fileno())
        f.seek(0)

        sb = StringBuffer(16)
        sb.fread(f.fileno())
        sb.seek(0)

        dtype_h = MFSObjectHeader.deserialize(sb)

        self.assertIsInstance(dtype_h, DatatypeHeader)
        self.assertEquals(dtype_h.datatype, datatype)
        self.assertEquals(dtype_h.flags, flags)
        self.assertEquals(dtype_h.size, size)
        self.assertEquals(dtype_h.total_size, total_size)

    def test_datatype(self):
        with TemporaryFile('w+b') as f:
            dtype_h = DatatypeHeader(1,2,3,0)
            self.header_check(f, dtype_h, 1, 2, 3, 0)

    def test_ubyte_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSUByteType()
            self.header_check(f, dtype_h, 0, 0, 1, 0)

    def test_byte_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSByteType()
            self.header_check(f, dtype_h, 1, 1, 1, 0)

    def test_ushort_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSUShortType()
            self.header_check(f, dtype_h, 2, 0, 2, 0)

    def test_short_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSShortType()
            self.header_check(f, dtype_h, 3, 1, 2, 0)

    def test_uint_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSUIntType()
            self.header_check(f, dtype_h, 4, 0, 4, 0)

    def test_int_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSIntType()
            self.header_check(f, dtype_h, 5, 1, 4, 0)
        
    def test_uint64_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSUInt64Type()
            self.header_check(f, dtype_h, 6, 0, 8, 0)

    def test_int64_header(self):
        with TemporaryFile('w+b') as f:
            dtype_h = MFSInt64Type()
            self.header_check(f, dtype_h, 7, 1, 8, 0)

@attr('perf')
class DatatypePerformance(PerformanceTestCase):
    def create_datatype(self, dtype_class):
        with TemporaryFile('w+b') as f:
            dtype_h = dtype_class()
            sb = dtype_h.serialize()
            sb.fwrite(f.fileno())
            f.seek(0)

            sb = StringBuffer(16)
            sb.fread(f.fileno())
            sb.seek(0)

            dtype_h = MFSObjectHeader.deserialize(sb)
            self.assertIsInstance(dtype_h, DatatypeHeader)

    def test_ubyte_profile(self):
        for i in xrange(10): # Warm up
            self.create_datatype(MFSUByteType)
        for i in xrange(1000):
            self.profile(self.create_datatype, MFSUByteType)

        self.assertTrue(sum(self.profile_context.stat_list) < 0.5)


