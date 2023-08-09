import mysql.connector
from ast import literal_eval
import socketserver
from threading import Thread
from legend import server_legacy
import requests

import socket, base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote

global req_head, flag
flag = False
"""
mydb = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="net"
)"""

class Server(BaseHTTPRequestHandler):
    # def __init__(self, user='', pid='', pwd=''):
        # super(Server, self).__init__()

    def do_POST(self):
        creds = 'user:pass'.encode()
        creds1 = 'user:pas'.encode()
        ping_creds = 'ping:credentials'.encode()

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
            """self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            try:
                s = socket.socket(2, 1)
                s.connect(('127.0.0.1', 9099))
            except ConnectionRefusedError:
                self.wfile.write(b"Smth went wrong with connect")
            else:
                self.wfile.write(b"Well done")
                del s

            s = socket.socket(2, 1)
            s.bind(('', 8081))
            s.listen(5)
            print("Well done")"""

            if port == 3214:
                alias = data[-1].split("=")[-1]
                if alias == "all":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    with open("temp.db", "r", encoding="utf-8") as f:
                        data = f.read()
                    self.wfile.write(data.encode("utf-8"))
                    # self.wfile.close()

                    # mycursor = mydb.cursor()
                    # mycursor.execute("SELECT * FROM ]")
                    # myresult = mycursor.fetchall()
                else:
                    pass
                    # mycursor = mydb.cursor()
                    # mycursor.execute(f"SELECT * FROM ] where alias='{alias}'")
                    # myresult = mycursor.fetchall()

        else:

            self.send_response(200)
            self.end_headers()

    def log_message(self, format, *args):
        return

host = socket.getaddrinfo(socket.gethostname(), None)
ipv4_addresses = [i[4][0] for i in host if i[0] == socket.AF_INET]
bot_serv_addr = ("127.0.0.1", 65000)
print(bot_serv_addr)

httpd = socketserver.TCPServer(bot_serv_addr, Server)
server = Thread(target=httpd.serve_forever, args=())
server.start()
