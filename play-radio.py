import opusdec
import lameshouter
import base64
import zlib
import wave
import time
import os
import random

songs_list = []
news_list = []

opusdec.initialize()
lameshouter.init()
start = time.time() - 0.1

old_hour = -1
pcm = b""

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
		txt = news_list.pop(0)
		filename = "news/" + txt
		lameshouter.setmeta("News :: " + txt)
	else:
		txt = songs_list.pop(0)
		filename = "songs/" + txt
		lameshouter.setmeta(txt)

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
				pcm += opusdec.decode(base64.b64decode(line))
				if len(pcm) >= 8192:
					lameshouter.shouter(pcm[:8192])
					pcm = pcm[8192:]
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
