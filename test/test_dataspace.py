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
            dataspace = DataspaceHeader((2,10))
            sb = dataspace.serialize()
            sb.fwrite(f.fileno())
            f.seek(0)
            
            sb = StringBuffer.from_file(f.fileno(), 16)
            
            dataspace = MFSObjectHeader.deserialize(sb)
            self.assertIsInstance(dataspace,DataspaceHeader)
            self.assertEquals(dataspace.ver, 0)
            self.assertEquals(dataspace.dims, 2)
            self.assertEquals(dataspace.flags, 0)
            self.assertEquals(dataspace.total_size, 16)

            sb = StringBuffer.from_file(f.fileno(), dataspace.total_size)
            dataspace.deserialize_dataspaces(sb)

            self.assertEquals(dataspace.dataspaces[0].dim_size, 2)
            self.assertEquals(dataspace.dataspaces[1].dim_size, 10)



@attr('perf')
class DataspacePerformance(PerformanceTestCase):
    def create_dataspace(self):
        ds = DataspaceHeader((40,40,40))
        sb = ds.serialize()
        with TemporaryFile('w+b') as f:

            sb.fwrite(f.fileno())

            f.seek(0)

            sb = StringBuffer.from_file(f.fileno(), 16)
            ds_header = MFSObjectHeader.deserialize(sb)
            sb = StringBuffer.from_file(f.fileno(), ds_header.total_size)
            ds_header.deserialize_dataspaces(sb)

            for i in xrange(3):
                self.assertEquals(ds_header.dataspaces[i].dim_size, 40)

    def test_dataspace_performance(self):
        for i in xrange(10):
            self.create_dataspace()

        for i in xrange(1000):
            self.profile(self.create_dataspace)

        self.assertTrue( sum(self.profile_context.stat_list) < 0.5) # Hard performance standard

