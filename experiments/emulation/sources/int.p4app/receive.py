#!/usr/bin/env python
import sys
import struct

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import PacketListField, ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR


class SwitchTrace(Packet):
    fields_desc = [ BitField("swid", 0, 32),
                    BitField("port", 0, 32),
                    BitField("ini", 0, 64),
                    BitField("fim", 0, 64)]
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



def handle_pkt(pkt):
    #print ("got a packet")
    ini = 0
    fim = 0
    for x in pkt[IP]['INT'].int_headers:
        if fim == 0:
            fim = x.fim
        ini = x.ini

    print (fim-ini)    
    #pkt.show2()
    #hexdump(pkt)
    sys.stdout.flush()


def main():
    iface = 'eth0'
    print ("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()