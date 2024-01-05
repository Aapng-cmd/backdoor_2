import pyshark, subprocess, base64
from prettytable import PrettyTable
answer = PrettyTable()
answer.field_names = ["Src ip", "Dest ip", "based http_req_data", "server answer"]
# answer.field_names = ["Src ip", "Dest ip", "server answer"]


# set an analyzer for handshakes/ http/s traffic/ password/username searching

capture = pyshark.LiveCapture(interface='Беспроводная сеть', display_filter='http')

for packet in capture.sniff_continuously(packet_count=2):
    server_ans = ""
    # if "" in packet:
    # print('Just arrived:', packet)
    # print(dir(packet.http))
    # exit()
    # print(dir(packet))
    try: server_ans = packet['data-text-lines']
    except KeyError: pass
    # print(packet)
    answer.add_row([packet.ip.src, packet.ip.dst, base64.b64encode(str(packet.http).encode()).decode(), base64.b64encode(":".join(str(server_ans).split(":")[1:]).encode()).decode()])
    # answer.add_row([packet.ip.src, packet.ip.dst, base64.b64encode(":".join(str(server_ans).split(":")[1:]).encode()).decode()])

print(answer)
