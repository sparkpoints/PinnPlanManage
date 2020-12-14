import gzip
import tarfile
import StringIO

# Depending on how your tar file is constructed, you might need to specify
# './README' as your magic_file

magic_file = 'README'

f = gzip.open('corrupt', 'rb')

t = StringIO.StringIO()

try:
    while 1:
        block = f.read(1024)
        t.write(block)
except Exception as e:
    print str(e)
    print '%d bytes decompressed' % (t.tell())

t.seek(0)
tarball = tarfile.TarFile.open(name=None, mode='r', fileobj=t)

try:
    magic_data = tarball.getmember(magic_file).tobuf()
    # I didn't actually try this part, but in theory
    # getmember returns a tarinfo object which you can
    # use to extract the file

    # search magic data for serial number or print out the
    # file
    print magic_data
except Exception as e:
    print e
