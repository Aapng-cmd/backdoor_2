import socket
import requests

s = socket.socket(2, 1)
ip = requests.get("http://api.ipify.org").text
port = 8809
print((ip, port))
s.bind(('', port))
s.listen(5)
client, addr = s.accept()

while True:
    com = input(">> ")
    client.send(com.encode())
    if com == "exit":
        break
        
s.close()
