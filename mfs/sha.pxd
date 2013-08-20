
cdef extern from "openssl/sha.h":
    ctypedef struct SHA_CTX:
        unsigned int h0
        unsigned int h1
        unsigned int h2
        unsigned int h3
        unsigned int h4
        unsigned int Nl
        unsigned int Nh
        unsigned int data[16]
        unsigned int num

    int SHA1_Init(SHA_CTX *c) 
    int SHA1_Update(SHA_CTX *c, void *data, size_t len) 
    int SHA1_Final(unsigned char *md, SHA_CTX *c) 
    unsigned char *SHA1(unsigned char *d, size_t n, unsigned char *md) 
    void SHA1_Transform(SHA_CTX *c, unsigned char *data) 


cdef class PySHA1:
    cdef SHA_CTX ctx
    cdef int update(self,char *block, size_t blocksize) except 0
    cdef int final(self, unsigned char *md) except 0

