import socket

s_r = socket.socket(2, 1)
s_r.bind(("127.0.0.1", 65000))
s_r.listen(5)
client, addr = s_r.accept()
print("Got client")

s_s = socket.socket(2, 1)
s_s.connect(("127.0.0.1", 8800))

print("connected")

while True:
    com = s_s.recv(1024)
    client.send(com)
    ans = client.recv(1024)
    s_s.send(ans)
    cd = client.recv(1024)
    s_s.send(cd)