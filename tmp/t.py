import pyshark, subprocess


capture = pyshark.LiveCapture(interface='loop')

for packet in capture.sniff_continuously(packet_count=5):
    print('Just arrived:', packet)

