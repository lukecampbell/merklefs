#!/usr/bin/env python
'''
@author Luke Campbell
@file test/test_node.py
@description Merkle Node Test
'''

from test.test_case import MFSTestCase
from test.performance import PerformanceTestCase

from mfs.objects import MFSObjectHeader
from mfs.node import MerkleNode, MerkleNodeHeader
from hashlib import sha1
from tempfile import TemporaryFile
from mfs.string_buffer import StringBuffer

class TestNode(MFSTestCase):
    def test_merkle_node(self):
        buf = 'sample text'
        sha_bytes = sha1(buf).digest()

        o = MerkleNode(3, 0, 0, sha_bytes)
        mnode = MerkleNodeHeader()

        for i in xrange(5):
            mnode.add_child(o)

        with TemporaryFile('w+b') as f:
            mnode.serialize().fwrite(f.fileno())
            f.seek(0)

            sb = StringBuffer.from_file(f.fileno(), 16)
            mnode_header = MFSObjectHeader.deserialize(sb)

            sb = StringBuffer.from_file(f.fileno(), mnode_header.total_size)

            mnode_header.deserialize_children(sb)

        self.assertEquals(mnode.objects[-1].sha, mnode_header.objects[-1].sha)

            




        



