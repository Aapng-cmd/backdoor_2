import socket
import threading, requests


def extract_host_port_from_request(request):
    host_string_start = request.find(b'Host: ') + len(b'Host: ')

    host_string_end = request.find(b'\r\n', host_string_start)

    host_string = request[host_string_start:host_string_end].decode('utf-8')

    webserver_pos = host_string.find("/")

    if webserver_pos == -1:
        webserver_pos = len(host_string)
    
    port_pos = host_string.find(":")

    if port_pos == -1 or webserver_pos < port_pos:
        port = 80
        host = host_string[:webserver_pos]

    else:
        port = int((host_string[(port_pos + 1):])[:webserver_pos - port_pos - 1])

        host = host_string[:port_pos]

    return host, port


def recv(req):
    site_host, site_port = extract_host_port_from_request(req)
    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    destination_socket.connect((site_host, site_port))
    destination_socket.sendall(req)
    data = destination_socket.recv(4096)
    destination_socket.close()
    
    return data

s = socket.socket(2, 1)

port = 65001

s.bind(('127.0.0.1', port))
s.listen(10)

client, addr = s.accept()
c2c_server = "http://127.0.0.1:65000/"

sess = request.Session()

while True:
    try:
        req = client.recv(4096)
        #TODO: открой основной сервак и сделай хуки через него на прокси страницу/порт, что зазочешь
        s.post(c2c_server, data={"req": req})
        # print(req.decode())
        req = requests.get(c2c_server + "ans")
        data = recv(req)
        
        if len(data) > 0: client.sendall(data)
        
    except Exception as e:
        print(e)
        client.close()
        s.close()
        break
