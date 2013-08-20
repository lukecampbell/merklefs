#!/usr/bin/env python

class BufferOverflow(RuntimeError):
    pass

class MFSException(Exception):
    pass

class SerializationError(MFSException):
    pass

