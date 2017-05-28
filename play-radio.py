import opusdec
import base64
import zlib
import wave
import subprocess
import time
import os
import random

songs_list = []
news_list = []

wf = subprocess.Popen(["ffmpeg", "-f", "s16le", "-ar", "48000", "-ac", "2", "-i", "pipe:0", "-acodec", "libmp3lame", "-qscale:a", "1", "-f", "mp3", "icecast://source:hackme@127.0.0.1:8000/radio.mp3"], stdin=subprocess.PIPE)
opusdec.initialize()
start = time.time() - 0.1

old_hour = -1

while True:
	if time.localtime()[3] != old_hour:
		old_hour = time.localtime()[3]
		for file in os.listdir("news/"):
			news_list.append(file)
		random.shuffle(news_list)

	if len(songs_list) == 0:
		for file in os.listdir("songs/"):
			songs_list.append(file)
		random.shuffle(songs_list)

	if len(news_list) >= 1:
		filename = "news/" + news_list.pop(0)
	else:
		filename = "songs/" + songs_list.pop(0)
	print(filename)

	f = open(filename, "rb")
	e = zlib.decompressobj()
	buf = b""
	pos = 0
	line = b""

	while True:
		rc = f.read(2048)
		if len(rc) != 2048:
			break
		
		buf += e.decompress(rc)
		
		while True:
			if buf[pos:pos+1] == b"\n":
				wf.stdin.write(opusdec.decode(base64.b64decode(line)))
				line = b""
				buf = buf[pos+1:]
				pos = 0
				start += 0.01
				if start > time.time():
					time.sleep(0.01)
			else:
				line += buf[pos:pos+1]
				pos += 1
			
			if len(buf) - pos < 1024:
				break
	f.close()

wf.close()
