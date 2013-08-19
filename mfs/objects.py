#!/usr/bin/env python
'''
@author Luke Campbell
@file mfs/objects.py
@description Definitions for the basic objects
'''

class MFSObjectHeader:
    '''
    MFS Object Header
    +-----------------------------------------------------------------------------------+
    |     mfs_type       |    res             |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |     res            |    res             |       res          |       res          |
    +-----------------------------------------------------------------------------------+
    |                               total_size                                          |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    '''
    mfs_type = None



class MFSObject:
    pass


