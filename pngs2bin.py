import sys,os
import struct
from PIL import Image

output_filename = sys.argv[1]
png_filenames = sys.argv[2:]

chunks={}

lengths=set()
for png in png_filenames:
	im=Image.open(png).convert('L')
	
	data=im.tobytes()
	signature,length,chunk_number=struct.unpack('<8sLL',data[:16])
	if signature!=b'bin2png\1':
		print('Invalid signature in {}: {}'.format(png,repr(signature)))
		sys.exit(1)
	lengths.add(length)
	chunks[chunk_number]=data[16:]


if len(lengths)!=1:
	print('Multiple lengths in images! Are you mixing different volumes?')
	print('Lengths: {}'.format(lengths))
	sys.exit(2)
output_length=list(lengths)[0]
with open(output_filename,'wb') as f:
	for i in range(len(chunks)):
		f.write(chunks[i])
	f.seek(output_length,os.SEEK_SET)
	f.truncate() # this is not the smart way to do this but I am lazy
