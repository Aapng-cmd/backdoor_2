import socket
# from legend import server_legacy


s = socket.socket(2, 1)
s.bind(("127.0.0.1", 8800))
s.listen(5)
client, addr = s.accept()

print("Got client")

while True:
    com = input(">> ")
    client.send(com.encode())
    print(client.recv(1024).decode())
    print(client.recv(1024).decode(), end="")