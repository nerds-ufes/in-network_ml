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

'''fields_desc = [ BitField("class", 0, 8),
                BitField("df", 0,16),
                BitField("mf", 0,16),
                BitField("fin", 0,16),
                BitField("syn", 0,16),
                BitField("rst", 0,16),
                BitField("psh", 0,16),
                BitField("ack", 0,16),
                BitField("urg", 0,16),
                BitField("ece", 0,16),
                BitField("cwr", 0,16),
                BitField("totalLen", 0,32),
                BitField("flow_duration", 0,48),
                BitField("min_pkt_len", 0,32),
                BitField("max_pkt_len", 0,32),
                BitField("pkts", 0,32)]'''


class SwitchTrace(Packet):
    fields_desc = [ BitField("class", 0, 8),
                BitField("df", 0,16),
                BitField("mf", 0,16),
                BitField("fin", 0,16),
                BitField("syn", 0,16),
                BitField("rst", 0,16),
                BitField("psh", 0,16),
                BitField("ack", 0,16),
                BitField("urg", 0,16),
                BitField("ece", 0,16),
                BitField("cwr", 0,16),
                BitField("totalLen", 0,32),
                BitField("flow_duration", 0,48),
                BitField("min_pkt_len", 0,32),
                BitField("max_pkt_len", 0,32),
                BitField("pkts", 0,32)]
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
def get_if():
    ifs=get_if_list()
    iface="eth0"
    for i in get_if_list():
        print(i)
        if "eth0" in i:
            iface=i
            break
    if not iface:
        print ("Cannot find eth0 interface")
        exit(1)
    return iface


def main():

    parser = argparse.ArgumentParser(description='Process to evaluate datasets.')
    parser.add_argument('-f', help='PCAP file', default='f')
    args = parser.parse_args()

    scapy_cap = PcapReader(args.f)
    count = 0

    opt = IPOption_INT(count=0, int_headers=[])

    for p in scapy_cap:

        p[IP].ihl = 0

        p[IP].options = opt
        print(p[TCP].flags)
        count += 1
        print ("sending pkt {}".format(count))
        #pkt.show2()
        sendp(p, iface="eth0", verbose=False)
        time.sleep(0.3)

if __name__ == '__main__':
    main()