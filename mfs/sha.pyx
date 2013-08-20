
from sha cimport SHA1_Init, SHA1_Update, SHA1_Final, SHA1, SHA1_Transform, SHA1

cdef class PySHA1:
    def __cinit__(self):
        cdef int retval = SHA1_Init(&self.ctx)
        if retval != 1:
            raise RuntimeError("failed to initialize sha1 context")

    cdef int update(self,char *block, size_t blocksize) except 0:
        cdef int retval = SHA1_Update(&self.ctx, block, blocksize)
        return retval

    cdef int final(self, unsigned char *md) except 0:
        cdef int retval = SHA1_Final(md, &self.ctx)
        return retval


