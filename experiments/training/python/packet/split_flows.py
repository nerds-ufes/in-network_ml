
from scapy.all import *
import numpy as np
from decimal import Decimal
import time
import pandas as pd

scapy_cap = PcapReader("../../pcap/wed2.pcap")
count = 0
for packet in scapy_cap:
    if not packet.haslayer(IP):
        continue

    src = 0
    dst = 0
    if packet.haslayer(TCP):
        src = packet[TCP].sport
        dst = packet[TCP].dport
    elif packet.haslayer(UDP):
        src = packet[UDP].sport
        dst = packet[UDP].dport
    hf = f'{packet[IP].src}_{packet[IP].dst}_{src}_{dst}.pcap' 
    count +=1

    pcap = PcapWriter(f"../../pcap/flow/{hf}",append=True)
    pcap.write(packet)
    pcap.close()

print(count)

