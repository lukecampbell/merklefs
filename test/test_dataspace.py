#!/usr/bin/env python
'''
@author Luke Campbell
@file test/test_dataspace.py
@description Dataspace Tests
'''

from test.test_case import MFSTestCase, attr
from test.performance import PerformanceTestCase
from mfs.objects import MFSObjectHeader
from mfs.dataspace import Dataspace, DataspaceHeader
from mfs.string_buffer import StringBuffer
from tempfile import TemporaryFile

@attr('unit')
class TestDataspace(MFSTestCase):
    def test_dataspace_header(self):
        with TemporaryFile('w+b') as f:
            dataspace = DataspaceHeader(2)
            sb = dataspace.serialize()
            sb.fwrite(f.fileno())
            f.seek(0)
            
            sb = StringBuffer.from_file(f.fileno(), 16)
            
            dataspace = MFSObjectHeader.deserialize(sb)
            self.assertIsInstance(dataspace,DataspaceHeader)
            self.assertEquals(dataspace.ver, 0)
            self.assertEquals(dataspace.dims, 2)
            self.assertEquals(dataspace.flags, 0)
            self.assertEquals(dataspace.total_size, 0)



@attr('perf')
class DataspacePerformance(PerformanceTestCase):
    pass

