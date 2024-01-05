import pyshark, subprocess
from prettytable import PrettyTable
answer = PrettyTable()
answer.field_names = ["Src ip", "Dest ip"]


# set an analyzer for handshakes/ http/s traffic/ password/username searching

capture = pyshark.LiveCapture(interface='Беспроводная сеть', display_filter='tcp')

for packet in capture.sniff_continuously(packet_count=6):
    # if "TLS" in packet:
    print('Just arrived:', packet)
    answer.add_row([packet.ip.src, packet.ip.dst])

print(answer)
