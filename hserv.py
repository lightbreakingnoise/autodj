from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import time
import cgi
import os
import sys
import subprocess

if len(sys.argv) != 2:
	print("python3 hserv.py password")
	sys.exit(0)

class WebServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.html_out("startseite.html")

	def do_POST(self):
		if self.path == "/start":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]})
			if form["pass"].value == sys.argv[1]:
				self.html_out_dir("files.html")
			else:
				self.html_out("startseite.html")
		elif self.path == "/deletesong":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]})
			if form["pass"].value == sys.argv[1]:
				os.remove("songs/" + form["delete"].value)
				self.html_out_dir("files.html")
			else:
				self.html_out("startseite.html")
		elif self.path == "/deletenews":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]})
			if form["pass"].value == sys.argv[1]:
				os.remove("news/" + form["delete"].value)
				self.html_out_dir("files.html")
			else:
				self.html_out("startseite.html")
		elif self.path == "/upsong":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]})
			if form["pass"].value == sys.argv[1]:
				f = open(form["file"].filename, "wb")
				f.write(form["file"].file.read())
				f.close()
				subprocess.Popen(["/usr/bin/python3", "convert.py", form["file"].filename, "songs/" + form["title"].value]).wait()
				os.remove(form["file"].filename)
				self.html_out_dir("files.html")
			else:
				self.html_out("startseite.html")
		elif self.path == "/upnews":
			form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers["Content-Type"]})
			if form["pass"].value == sys.argv[1]:
				f = open(form["file"].filename, "wb")
				f.write(form["file"].file.read())
				f.close()
				subprocess.Popen(["/usr/bin/python3", "convert.py", form["file"].filename, "news/" + form["title"].value]).wait()
				os.remove(form["file"].filename)
				self.html_out_dir("files.html")
			else:
				self.html_out("startseite.html")

	def html_out(self, filename):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		
		ltime = time.localtime()
		nowtime = ("%2.2d" % ltime[3]) + ":" + ("%2.2d" % ltime[4])
		
		f = open(filename)
		out = f.read()
		f.close()
		
		out = out.replace("<TIME>", nowtime)
		
		self.wfile.write(out.encode())

	def html_out_dir(self, filename):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		
		ltime = time.localtime()
		nowtime = ("%2.2d" % ltime[3]) + ":" + ("%2.2d" % ltime[4])
		
		lshtml = ""
		for fn in os.listdir("songs/"):
			lshtml += "<form class=\"afile\" method=\"POST\" action=\"/deletesong\">" + fn + "<input type=\"hidden\" name=\"delete\" value=\"" + fn + "\"> <input type=\"password\" name=\"pass\" class=\"passwd\"> <input type=\"submit\" value=\"delete\"></form><br>"
		lshtml += "<form class=\"afile\" method=\"POST\" action=\"/upsong\" enctype=\"multipart/form-data\"> Titel: <input type=\"text\" name=\"title\" class=\"passwd\"> <input type=\"file\" name=\"file\" accept=\"audio/*\"> Passwort: <input type=\"password\" name=\"pass\" class=\"passwd\"> <input type=\"submit\" value=\"hochladen\"></form><br><br><br>"
		for fn in os.listdir("news/"):
			lshtml += "<form class=\"anews\" method=\"POST\" action=\"/deletenews\">" + fn + "<input type=\"hidden\" name=\"delete\" value=\"" + fn + "\"> <input type=\"password\" name=\"pass\" class=\"passwd\"> <input type=\"submit\" value=\"delete\"></form><br>"
		lshtml += "<form class=\"anews\" method=\"POST\" action=\"/upnews\" enctype=\"multipart/form-data\"> Titel: <input type=\"text\" name=\"title\" class=\"passwd\"> <input type=\"file\" name=\"file\" accept=\"audio/*\"> Passwort: <input type=\"password\" name=\"pass\" class=\"passwd\"> <input type=\"submit\" value=\"hochladen\"></form><br><br><br>"
		
		f = open(filename)
		out = f.read()
		f.close()
		
		out = out.replace("<TIME>", nowtime)
		out = out.replace("<FILES>", lshtml)
		
		self.wfile.write(out.encode())

	def log_message(self, format, *args):
		return

def webserverloop():
	hsrv = HTTPServer(('0.0.0.0', 8100), WebServer)
	hsrv.serve_forever()
Thread(target=webserverloop).start()
