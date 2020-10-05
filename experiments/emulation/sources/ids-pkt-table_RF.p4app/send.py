#!/usr/bin/env python
import argparse
import sys
import socket
import struct

from scapy.all import sendp, send, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption, PcapReader
from scapy.all import Ether, IP, UDP, TCP
from scapy.all import IntField, FieldListField, FieldLenField, ShortField, PacketListField, BitField
from scapy.layers.inet import _IPOption_HDR
import time

def main():

    parser = argparse.ArgumentParser(description='Process to evaluate datasets.')
    parser.add_argument('-f', help='PCAP file', default='f')
    args = parser.parse_args()

    scapy_cap = PcapReader(args.f)
    count = 0

    for p in scapy_cap:

        #p[IP].ihl = 0

        #p[IP].options = opt
        #print(p[TCP].flags)
        count += 1
        print ("sending pkt {}".format(count))
        p.show2()
        sendp(p, iface="eth0", verbose=False)
        time.sleep(0)

if __name__ == '__main__':
    main()