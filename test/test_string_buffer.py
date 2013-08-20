from test.test_case import MFSTestCase, attr

from mfs.string_buffer import StringBuffer, BufferOverflow
from tempfile import TemporaryFile

@attr('unit')
class TestStringBuffer(MFSTestCase):
    def test_buffer(self):
        sb = StringBuffer(128)
        sb.write('hello world')
        sb.seek(0)
        self.assertEquals(sb.read(), 'hello world')

        self.assertEquals(sb.offset(), 0)
        sb.write('jello')
        self.assertEquals(sb.offset(), 5)
        sb.seek(0)
        self.assertEquals(sb.read(), 'jello world')

        sb.set('hi')
        self.assertEquals(sb.offset(), 0)
        self.assertEquals(sb.read(), 'hi')

        sb = StringBuffer("Hello World")
        self.assertEquals(sb.read(), 'Hello World')

        sb = StringBuffer(sb)
        self.assertEquals(sb.read(), 'Hello World')


    
    def test_overflow(self):
        sb = StringBuffer(24)
        with self.assertRaises(BufferOverflow):
            sb.write('this string is definitely longer than 24 characters and should raise an error')

        self.assertRaises(OverflowError, sb.seek, -1)

        sb = StringBuffer(8)
        sb.set('01234567')
        sb.seek(0)
        buf = sb.raw_read(8)
        self.assertEquals(buf, '01234567')
        self.assertRaises(BufferOverflow, sb.raw_read, 1)


    def test_word_align(self):
        sb = StringBuffer(12)
        self.assertEquals(sb.buffer_size(), 16)

    def test_fwrite(self):
        sb = StringBuffer(24)
        sb.set('hello world\n')
        with TemporaryFile('w+b') as f:
            fd = f.fileno()
            sb.fwrite(fd)
            f.seek(0)
            buf = f.readline()
            self.assertEquals(buf, 'hello world\n')

    def test_fread(self):
        sb = StringBuffer(16)
        with TemporaryFile('w+b') as f:
            fd = f.fileno()
            f.write('hello world\n')
            f.seek(0)
            sb.fread(fd, 8)
            sb.seek(0)
            self.assertEquals(sb.raw_read(8), 'hello wo')
            

    def test_read_uint(self):
        sb = StringBuffer(16)
        sb.pack('<H', 16)

        sb.seek(0)
        i = sb.read_uint(2)
        self.assertEquals(i, 16)

        self.assertEquals(sb.offset(), 2)
        sb.pack('<Q', 1024)
        sb.seek(2)
        i = sb.read_uint(8)
        self.assertEquals(1024, i)

    def test_write_sb(self):
        container = StringBuffer(24)
        el = StringBuffer(16)
        el.set('hello world')

        container.write(el)

        container.seek(0)
        self.assertEquals(container.read(), 'hello world')


    def test_from_file(self):
        with TemporaryFile('w+b') as f:
            b = 'hello world'
            f.write(b)
            f.seek(0)

            sb = StringBuffer.from_file(f.fileno(), len(b)+1)
            self.assertEquals(sb.read(), b)

    def test_hash(self):
        buf = StringBuffer("Hello World")
        buf_sha = buf.hash()
        from hashlib import sha1
        outside = StringBuffer(sha1(buf.raw_read()).digest())
        self.assertEquals(outside.raw_read(), buf_sha.raw_read())
        
    def test_large_hash(self):
        with open('/dev/urandom', 'r+b') as f:
            buf = StringBuffer.from_file(f.fileno(), 4096 * 3)
        buf_sha = buf.hash()
        from hashlib import sha1
        outside = StringBuffer(sha1(buf.raw_read()).digest())
        self.assertEquals(outside.raw_read(), buf_sha.raw_read())

