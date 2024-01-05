import pyshark, subprocess


# set an analyzer for handshakes/ http/s traffic/ password/username searching

capture = pyshark.LiveCapture(interface='Беспроводная сеть', display_filter='tcp')

for packet in capture.sniff_continuously(packet_count=1000):
    print('Just arrived:', packet)

