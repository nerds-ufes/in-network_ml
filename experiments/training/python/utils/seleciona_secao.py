from scapy.all import *
import pandas as pd
import numpy as np
from decimal import Decimal
import hashlib
import time
import argparse

def hash_md5(ips, tsp, tdp, ipd, usp, udp):
    hf = '{}{}{}{}{}{}'.format(ips, tsp, tdp, ipd, usp, udp)
    return hashlib.md5(hf.encode("utf-8")).hexdigest()


df = pd.read_csv("../results/dataset_session2.csv")
labeled = df[df['label'] == 'dos_slowloris']

print(int(labeled['pkts_f'].mean(axis=0)))

qt = int(labeled['pkts_f'].mean(axis=0)) +3
sec = labeled[labeled['pkts_f'] == qt]
sample = sec.sample(n=1)
print(sample)   
row = sample.iloc[0]
h = '{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort'])
h1 = row['idx_fw']
print('pkts {} pkts_f {}'.format(row['pkts'], row['pkts_f']))
scapy_cap = PcapReader("../pcap/wed_dsl.pcap")
scapy_cap_w = PcapWriter("../pcap/dos_sl{}.pcap".format(qt))
count = 0
c2 = 0
h2 = ''



def has_in_flag(flag, s):
    return True if s in str(flag) else False


rst = 0
min = 10000
max = 0

for packet in scapy_cap:
    tsp = 0
    tdp = 0
    usp = 0
    udp = 0
    if packet.haslayer(TCP):
        tsp = packet[TCP].sport
        tdp = packet[TCP].dport
    if packet.haslayer(UDP):
        usp = packet[UDP].sport
        udp = packet[UDP].dport

    if not packet.haslayer(IP):   
        continue

    #hf = '{}{}{}{}{}{}'.format(packet[IP].src, tsp, usp, packet[IP].dst, tdp, udp)

    #h2 = hashlib.md5(hf.encode("utf-8")).hexdigest()



    if packet[IP].src == row['ipS'] \
        and tsp == row['src'] \
        and usp == row['UDPSrcPort'] \
        and packet[IP].dst == row['ipD'] \
        and tdp == row['dst'] \
        and udp == row['UDPDstPort']: 
        
        rst += 1 if has_in_flag(packet[TCP].flags, 'F') else 0
        if min > packet[IP].len:
            min = packet[IP].len
        if max < packet[IP].len:
            max = packet[IP].len
        if c2 == 0:
            h = '{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort'])
            h2 = hashlib.md5(h.encode("utf-8")).hexdigest()

        #if h1 == h2:
        scapy_cap_w.write(packet)
        c2+=1
        #packet.show2()

    if count % 30000 == 0:
        print('pkt {} h1 == h2 {} = {}'.format(count, c2, h2))

    count += 1
print('pkt {} h1 == h2 {} = {} // rst {}  min {}   max {}'.format(count, c2, h2, rst, min, max))
