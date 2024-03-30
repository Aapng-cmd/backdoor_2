import socketserver
from threading import Thread
# from legend import server_legacy
import requests
import os, subprocess
import string, random
import socket, base64
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import unquote
from ast import literal_eval


def from_req_to_smth(data):
	dt = []
	for i in range(len(data)):
		q = data[i].split("=")
		q[0] = "'" + q[0] + "'"
		q[1] = "'" + q[1] + "'"
		q = ": ".join(q)
		dt.append(q)

	dt = "{" + ", ".join(dt) + "}"
	dt = literal_eval(dt)
	
	return dt




class Server(BaseHTTPRequestHandler):
	# def __init__(self):
	# 	self.nickname = ""
	# 	self.command = ""
	# 	self.data = ""
		
	def do_POST(self):
		cookies = SimpleCookie(self.headers.get('Cookie'))
		if cookies == "":
		    C = SimpleCookie()
		    self.wfile.write(C.output)
		
		req = str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1]
		req = req.split("&")
		req = from_req_to_smth(req)
		global nickname
		global command
		global data
		nickname = req['nickname']
		command = req['command']
		data = req['data']
		
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
    	
    
	def do_GET(self):
		global nickname
		global command
		global data
		
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		
		
		self.wfile.write((nickname + " " + command + " " + data).encode())


    
	def log_message(self, format, *args):
		return
		
        
        
host = socket.getaddrinfo(socket.gethostname(), None)
ipv4_addresses = [i[4][0] for i in host if i[0] == socket.AF_INET]
bot_serv_addr = ("0.0.0.0", 65000)
print(bot_serv_addr)

httpd = socketserver.TCPServer(bot_serv_addr, Server)
server = Thread(target=httpd.serve_forever, args=())
server.start()
