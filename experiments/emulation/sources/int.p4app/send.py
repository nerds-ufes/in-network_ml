#!/usr/bin/env python3


# h1 python3 send.py 10.0.0.1 hello 1


import argparse
import sys
import socket
import random
import struct

from scapy.all import sendp, send, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import Ether, IP, UDP
from scapy.all import IntField, FieldListField, FieldLenField, ShortField, PacketListField, BitField
from scapy.layers.inet import _IPOption_HDR

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


def main():

    if len(sys.argv)<3:
        print ('pass 2 arguments: <destination> "<message>"')
        exit(1)

    addr = socket.gethostbyname(sys.argv[1])
    iface = 'eth0'

    pkt = Ether(src=get_if_hwaddr(iface), dst="ff:ff:ff:ff:ff:ff") / IP(ihl = 0,
        dst=addr, options = IPOption_INT(count=0,
            int_headers=[])) / UDP(
            dport=1234, sport=4321) / sys.argv[2]

 #   pkt = Ether(src=get_if_hwaddr(iface), dst="ff:ff:ff:ff:ff:ff") / IP(
 #       dst=addr, options = IPOption_MRI(count=2,
 #           swtraces=[SwitchTrace(swid=0,qdepth=0), SwitchTrace(swid=1,qdepth=0)])) / UDP(
 #           dport=4321, sport=1234) / sys.argv[2]
    pkt.show2()
    #hexdump(pkt)
    try:
      for i in range(int(sys.argv[3])):
        sendp(pkt, iface=iface)
        sleep(0)
    except KeyboardInterrupt:
        raise


if __name__ == '__main__':
    main()