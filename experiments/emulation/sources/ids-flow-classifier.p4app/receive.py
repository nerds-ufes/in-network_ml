#!/usr/bin/env python

'''
h1 python3 send.py -f pcap/dos_sl12.pcap    
'''

import sys
import struct

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import PacketListField, ShortField, IntField, LongField, BitField, FieldListField, FieldLenField
from scapy.all import IP, UDP, Raw
from scapy.layers.inet import _IPOption_HDR


dic = {'eth0': 'benigno', 'h2-eth1': 'dos_hulk', 'h2-eth2': 'dos_goldeneye', 'h2-eth3': 'dos_slowhttptest', 'h2-eth4': 'wa_brute_force', 'h2-eth5': 'dos_slowloris', 'h2-eth6': 'i_portscan'}


pkts = 0
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
def handle_pkt(x, clazz):
    global pkts
    pkts +=1 
    print('pkt {} - {}'.format(pkts, clazz))
    #print(x[IP].options[0].int_headers)

    sys.stdout.flush()


def main():
    sniff(iface = ["eth0","h2-eth1","h2-eth2","h2-eth3","h2-eth4","h2-eth5","h2-eth6"], prn = lambda x: handle_pkt(x, dic[x.sniffed_on]))


'''    for iface, clazz in dic.items():
        print('{} - {}'.format(iface, clazz)) 
        sniff(iface = iface, prn = lambda x: print(x.sniffed_on))
'''
if __name__ == '__main__':
    main()