import wave
import struct
import subprocess
import sys
import opusenc
import base64
import zlib

if len(sys.argv) != 2:
	sys.exit(0)

print(sys.argv[1])
subprocess.Popen(["ffmpeg", "-i", sys.argv[1], "-ar", "48000", "-ac", "2", "-y", "temp.wav"], stderr=subprocess.PIPE, stdout=subprocess.PIPE).wait()

fname = "songs/" + input("Song File Name >> ")
f = open(fname, "wb")
e = zlib.compressobj(9)
c = 0
b = ""

opusenc.initialize(256000)

wf = wave.open("temp.wav")
while True:
	rc = wf.readframes(480)
	if len(rc) != 1920:
		break
	
	opus = opusenc.encode(rc)
	b += base64.b64encode(opus).decode("utf-8") + "\n"
	c += 1
	if c >= 100:
		c = 0
		f.write(e.compress(b.encode()) + e.flush(zlib.Z_SYNC_FLUSH))
		b = ""

f.write(e.compress(b.encode()) + e.flush(zlib.Z_SYNC_FLUSH))
f.close()
wf.close()
