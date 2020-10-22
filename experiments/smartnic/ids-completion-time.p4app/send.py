#!/usr/bin/env python3


# h1 python3 send.py 10.0.0.1 hello 1
#sendpfast(pkt, mbps=1000, loop=10, parse_results=1)

import argparse
import sys
import socket

from scapy.utils import rdpcap, wrpcap
from scapy.all import *
from scapy.layers.inet import _IPOption_HDR
from multiprocessing import Pool, TimeoutError

from time import sleep

class SwitchTrace(Packet):
    fields_desc = [ BitField("swid", 0, 32),
                    BitField("port", 0, 32)]
    def extract_padding(self, p):
                return "", p

class IPOption_INT(IPOption):
    name = "INT"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="int_headers",
                                  adjust=lambda pkt,l:l*2+8),
                    ShortField("count", 0),
                    PacketListField("int_headers",
                                   [],
                                   SwitchTrace,
                                   count_from=lambda pkt:(pkt.count*1)) ]


#wrpcap("pcap/benigno1000.pcap", packets)

def add_int(f_name, pkt):
    print ('Here')
    for p in pkt:

        pkt = Ether(src=p[Ether].src, dst=p[Ether].dst) / IP(ihl = 0,
        dst=p[IP].dst, options = IPOption_INT(count=0,
            int_headers=[])) / TCP(dport=p[TCP].dport, sport=p[TCP].sport) / Raw(load='X'*1408)
        wrpcap(f_name, pkt, append=True)
    return

def main(pkts):

    addr = socket.gethostbyname(sys.argv[1])
    iface = 'eth0'
    pps=10000*(2**20)/8/1500
    
    sendpfast(pkts, pps=1, loop=1, iface=iface)
    #sendp(pkts, count=2, inter=1./30)
if __name__ == '__main__':
    if len(sys.argv)<3:
        print ('pass 2 arguments: <destination> "<message>"')
        exit(1)
    try:
        if not os.path.isfile('./pcap/benigno_int.pcap'):
            packets = rdpcap("pcap/benigno.pcap")
            add_int("./pcap/benigno_int.pcap", packets)

        packets = rdpcap("./pcap/benigno_int.pcap")
        main(packets)
        os.remove("./pcap/benigno_int.pcap")
        exit(1)

        with Pool(processes=100) as pool:
            pool.map(main, range(int(sys.argv[3])) , chunksize=2)

    except KeyboardInterrupt:
        raise