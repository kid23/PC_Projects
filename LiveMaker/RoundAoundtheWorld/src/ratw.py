#encoding=gbk
#Round Aound the World Tools
#By KiD


import mmap
import os
import sys
import struct
import codecs
import zlib
import parse_lsb

class HeadIndex:
	def __init__(self, buf, len):
		self.name = buf
		self.len = len

def compress(buf, output):
	open(output, "wb+").write(zlib.compress(buf, 9))

def extract(buf, datafile, outputdir):
	if buf[0:3] != "vff" :
		print "Unknown file format."
		return
	num = struct.unpack("<I", buf[6:10])[0]
	file_indexs = []
	pos = 0xA
	for i in range(0, num):
		name_len = struct.unpack("<I", buf[pos:pos+4])[0]
		file_indexs.append(HeadIndex(buf[pos+4:pos+4+name_len], name_len))
		pos += 4 + name_len
	print "Total %d files." % len(file_indexs)
	key1,key2 = struct.unpack("<II", buf[pos:pos+8])
	t1,t2 = struct.unpack("<II", buf[pos:pos+8])
	txt = u''
	print "Decrypting index ..."
	for element in file_indexs:
		name_buf = ""
		for i in element.name:
			key2 = key1 + key2 + (key2 << 2)
			name_buf += chr(ord(i) ^ (key2&0xff))
		#element.name = name_buf.decode('cp932').encode('cp936','ignore')
		element.name = name_buf.decode('cp932').replace(u'\u30fb', u"·")
		#print element.name
		t2 = (t1 + t2 + (t2 << 2)) & 0xFFFFFFFF
		if t2 & 0x80000000 :
			x2 = 0xFFFFFFFF
		else :
			x2 = 0
		data1, data2 = struct.unpack("<II", buf[pos:pos+8])
		element.data1 = data1
		element.data2 = data2
		data1 = t2 ^ data1
		data2 = x2 ^ data2
		element.key = t2
		element.d_data1 = data1
		element.d_data2 = data2
		element.pos = data1
		pos += 8
	pos +=8 #skip end file flag
	datafile_size = os.path.getsize(datafile)
	fd = open(datafile, "rb")
	cnt = 1
	for element in file_indexs:
		fd.seek(element.pos, 0)
		file_name = u"%s\\%s" % (outputdir, element.name)
		path_name = os.path.split(file_name)[0]
		if not os.path.isdir(path_name) :
			os.makedirs(path_name)
		if (cnt >= num - 1) :
			size = datafile_size - element.pos
		else :
			size = file_indexs[cnt].pos - element.pos
		print "Write %d  %s  %x  %x" % (cnt, element.name, element.pos, size)
		if (buf[pos:pos+1] == '\x00') :
			open(file_name, "wb+").write(zlib.decompress(fd.read(size)))
		else :
			open(file_name, "wb+").write(fd.read(size))
		cnt += 1
		pos += 1
		txt += u"%s  %x  %x,  %x-%x(%x)\r\n" % (element.name, element.pos, size, element.data1, element.d_data1, element.key)
	fd.close()
	codecs.open("name.txt","w+",encoding="utf-16").write(txt)  

def extract_script_texts(buf, filename):
	ret = parse_lsb.parse_lsb(buf)
	if ret != '' :
		codecs.open(filename+".txt","w+",encoding="utf-16").write(ret)  

if __name__ == "__main__":
    print "Round Aound the World Tools By Kid, 2014\n"

    if len(sys.argv) < 3:
        print('Bad argv.')
        sys.exit(0)

    fd = os.open(sys.argv[2], os.O_RDONLY)
    size = os.fstat(fd).st_size
    buf = mmap.mmap(fd, size, access=mmap.ACCESS_READ)
    if sys.argv[1] == '-e':
        extract(buf, sys.argv[3], sys.argv[4])
    elif sys.argv[1] == '-c':
        compress(buf, sys.argv[3])
    elif sys.argv[1] == '-et':
        extract_script_texts(buf, sys.argv[2])
    else:
        print 'Bad argv.'
    os.close(fd)

    
