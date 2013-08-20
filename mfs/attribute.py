#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/attribute.py
@description Attribute block
'''

from mfs.objects import MFSObjectHeader, MFSObject

class AttributeHeader(MFSObjectHeader):
    '''
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    res             |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |                               res                                                 |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    mfs_type   - The MFSObject Type
    total_size - The size in bytes of the entire attribute block
    '''
    pass

class Attribute(MFSObject):
    '''
    +-----------------------------------------------------------------------------------+
    |     ver            |     res            |              name_size                  |
    +-----------------------------------------------------------------------------------+
    |              datatype_size              |              dataspace_size             |
    +-----------------------------------------------------------------------------------+
    |                              name*                                                |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |                              datatype*                                            |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |                              dataspace*                                           |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    |                              data*                                                |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
      * - Variable size

    ver            - Version number
    res            - reserved
    name_size      - size in bytes of attribute name including the null terminator (aligned to word boundary)
    datatype_size  - size in bytes of the datatype block
    dataspace_size - size in bytes of dataspace block
    data           - the raw data for this attribute
    '''

    pass

