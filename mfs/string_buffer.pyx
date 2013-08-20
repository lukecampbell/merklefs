from libc.stdlib cimport malloc, free
from libc.string cimport memset, strerror, memcpy
from libc.errno cimport errno, EAGAIN
from mfs.exceptions import BufferOverflow
from sha cimport SHA1, PySHA1
import sys

cdef extern from "unistd.h" nogil:
    ssize_t write(int filedes, void *buf, size_t nbyte)
    ssize_t read(int filedes, void *buf, size_t nbyte)

from struct import pack, unpack

cdef class StringBuffer:

    cdef char* buff
    cdef size_t size
    cdef size_t s_offset

    def __cinit__(self, initializer):
        cdef size_t size = 0
        string = None

        if isinstance(initializer, (basestring, StringBuffer)):
            string = initializer
            size = len(string)
        else:
            size = initializer

        # Align the size on a word boundary
        if size % 8 != 0:
            size += 8 - size % 8
        self.size = size
        self.buff = <char *> malloc(size)
        if self.buff == NULL:
            raise MemoryError(strerror(errno))
        memset(self.buff, 0x0, self.size)
        self.s_offset = 0x0

        if string is not None and isinstance(string,(basestring, StringBuffer)):
            self.write(string)
            self.seek(0)

    def __dealloc__(self):
        free(self.buff)

    cdef int check_offset(self, size_t offset):
        return (offset > self.size)

    def write(self, string):
        '''
        Copies the string argument into the buffer. The buffer offset is set to the end of the string.
        If the string is too long an IOError is raised indicating an overflow, no data is written in this case
        '''
        if self.check_offset(self.s_offset + len(string)):
            raise BufferOverflow("string length exceeds buffer size")
        if isinstance(string, basestring):
            memcpy(self.buff + self.s_offset, <char *> string, len(string))
        elif isinstance(string, StringBuffer):
            return self._write_sb(string)
        else:
            raise TypeError('unsupported type')
        self.s_offset += len(string)
        
    cdef _write_sb(self, StringBuffer string):
        if self.check_offset(self.s_offset + len(string)):
            raise BufferOverflow("string length exceeds buffer size")
        memcpy(self.buff + self.s_offset, string.buff + string.s_offset, string.size  - string.s_offset)
        self.s_offset += string.size - string.s_offset


    def seek(self, size_t offset):
        '''
        Sets the buffer offset
        '''
        if self.check_offset(offset):
            raise BufferOverflow("offset exceeds buffer size")
        self.s_offset = offset

    def read(self):
        '''
        Returns a python object that points to the buffer's offset (interpreted as null terminated)
        '''
        py_string = <bytes> (self.buff+self.s_offset)
        return py_string

    def raw_read(self, read_bytes=-1, strip_null=False):
        if read_bytes < 0:
            read_bytes = self.size - self.s_offset
        if self.check_offset(self.s_offset + read_bytes):
            raise BufferOverflow("offset exceeds buffer size")
        if strip_null:
            py_string = <bytes> (self.buff + self.s_offset)
        else:
            py_string = <bytes> self.buff[self.s_offset : self.s_offset + read_bytes]
        self.s_offset += read_bytes
        return py_string

    def pack(self, fmt, *args):
        '''
        See struct.pack
        '''
        self.write(pack(fmt, *args))

    def offset(self):
        '''
        Returns the current buffer offset
        '''
        return self.s_offset

    def set(self, string):
        '''
        Fills the buffer with 0 then writes the string
        the offset is set to 0 at the end of this operation.
        Ideal for clearing the buffer or reinitializing an existing buffer
        '''
        memset(self.buff, 0x0, self.size)
        self.seek(0)
        self.write(string)
        self.seek(0)

    def buffer_size(self):
        '''
        Returns the actual size of the buffer
        '''
        return self.size

    def fwrite(self, fd, bytes_to_write=-1):
        cdef ssize_t written = 0
        cdef size_t total = 0
        if bytes_to_write > 0:
            wb = bytes_to_write
        else:
            wb = self.size
        while total < wb:
            written = write(fd, self.buff + total, wb - total)
            if written < 0:
                if errno != EAGAIN:
                    raise IOError(strerror(errno))
            total += written

    def fread(self, fd, bytes_to_read=-1):
        cdef ssize_t bytes_read = -1
        cdef size_t total = 0
        cdef size_t br = self.size - self.s_offset
        if bytes_to_read > 0:
            br = bytes_to_read
        cdef int filedes = fd
        if self.check_offset(self.s_offset + br):
            raise BufferOverflow("read buffer exceeds string buffer size")

        while total < br:
            bytes_read = read(filedes, self.buff + self.s_offset + total, br - total)
            if bytes_read == 0: # EOF
                break
            if bytes_read < 0:
                if errno != EAGAIN:
                    raise IOError(strerror(errno))
            total += bytes_read
        self.seek(self.s_offset + total)

    @classmethod
    def from_file(cls, fd, bytes_to_read):
        sb = cls(bytes_to_read)
        sb.fread(fd, bytes_to_read)
        sb.seek(0)
        return sb


    def dump_buffer(self):
        cdef size_t i=0
        cdef size_t j=0
        cdef unsigned char c = 0x0
        for i in xrange(self.size / 8):
            sys.stdout.write('0x%08x ' % (i*8))
            for j in xrange(8):
                c = <unsigned char> self.buff[i*8 + j]
                sys.stdout.write('%02x ' % <unsigned char> self.buff[i * 8 + j])
            for j in xrange(8):
                c = <unsigned char> self.buff[i*8 + j]
                if (c >= 65 and c <= 90) or (c >= 97 and c <= 123):
                    sys.stdout.write('%c' % c)
                else:
                    sys.stdout.write('.')
            sys.stdout.write('\n')
        # It's always on a word boundary so I don't need to deal with the edge case :)

    def read_uint(self, byte_count):
        '''
        Reads an unsigned integer of a specified number of bytes
        '''
        if self.check_offset(self.s_offset + byte_count):
            raise BufferOverflow("Offset exceeds buffer size")
        buf = <bytes> self.buff[self.s_offset : self.s_offset + byte_count]
        self.s_offset += byte_count

        if byte_count == 1:
            return unpack('<B', buf)[0]
        if byte_count == 2:
            return unpack('<H', buf)[0]
        if byte_count == 4:
            return unpack('<I', buf)[0]
        if byte_count == 8:
            return unpack('<Q', buf)[0]

        raise IOError("Can't unpack unsigned integer of %s bytes" % byte_count)


    def __len__(self):
        return self.size

    def hash(self):
        cdef StringBuffer md = StringBuffer(20)
        cdef PySHA1 sha1 = PySHA1()
        cdef size_t bytes_hashed = 0
        cdef size_t bytes_to_hash
        while bytes_hashed < self.size:
            bytes_to_hash = min(self.size - bytes_hashed, 4096)
            sha1.update(self.buff + bytes_hashed, bytes_to_hash)
            bytes_hashed += bytes_to_hash
        sha1.final(<unsigned char *>md.buff)

        return md

