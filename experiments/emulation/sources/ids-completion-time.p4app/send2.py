#!/usr/bin/env python

#h1 python3 send2.py 10.1.1.1 hello 1

import argparse
import sys
import socket
import random
import struct

from scapy.all import sendp, send, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import Ether, IP, UDP, TCP
from scapy.all import IntField, FieldListField, FieldLenField, ShortField, PacketListField, BitField
from scapy.layers.inet import _IPOption_HDR

from time import sleep

class SwitchTrace(Packet):
    fields_desc = [ BitField("swid", 0, 13),
                    BitField("qdepth", 0,13),
                    BitField("portid",0,6)]
    def extract_padding(self, p):
                return "", p

class IPOption_INT(IPOption):
    name = "INT"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="int_headers",
                                  adjust=lambda pkt,l:l*2+4),
                    ShortField("count", 0),
                    PacketListField("int_headers",
                                   [],
                                   SwitchTrace,
                                   count_from=lambda pkt:(pkt.count*1)) ]


def main():

    if len(sys.argv)<3:
        print ('pass 2 arguments: <destination> "<message>"')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = 'eth0'
    opt = IPOption_INT(count=0, int_headers=[])
    ip = IP(dst=addr, options=opt, ihl=0)
    udp = UDP(dport=1234, sport=4321)
    ether = Ether(src=get_if_hwaddr(iface), dst="ff:ff:ff:ff:ff:ff")
    pkt =  ether / ip / udp / sys.argv[2]

    pkt.show2()
    try:
      for i in range(int(sys.argv[3])):
        sendp(pkt, iface=iface)
        sleep(1)
    except KeyboardInterrupt:
        raise


if __name__ == '__main__':
    main()