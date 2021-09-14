import sys,os
import struct
from PIL import Image
with open(sys.argv[1],'rb') as f:
	data=f.read()

def encode_header(length,chunk_number):
	return struct.pack('<8sLL',b'bin2png\1', length, chunk_number)

# encode a dummy header so we know how big it is
HEADER_LENGTH = len(encode_header(0,0))

W,H=900,900
CHUNKSIZE=(W*H)-HEADER_LENGTH
chunks=[]
for i in range((len(data)+CHUNKSIZE)//CHUNKSIZE):
	chunks.append(data[i*CHUNKSIZE:(i+1)*CHUNKSIZE])

print ('{} chunks'.format(len(chunks)))
for i,rawchunk in enumerate(chunks):
	if len(rawchunk)<CHUNKSIZE:
		rawchunk=rawchunk+(b'\0'*(CHUNKSIZE-len(rawchunk)))
	chunk = encode_header(len(data),i)+rawchunk
	im=Image.frombuffer('L',(W,H),chunk)
	im.save('bin{:04d}.png'.format(i))
