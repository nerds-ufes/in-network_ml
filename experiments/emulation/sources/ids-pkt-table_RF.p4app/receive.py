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


dic = {'eth0': 'benigno', 'h2-eth1': 'dos_hulk', 'h2-eth2': 'dos_goldeneye', 'h2-eth3': 'dos_slowhttptest', 'h2-eth4': 'wa_brute_force', 'h2-eth5': 'dos_slowloris', 'h2-eth6': 'i_portscan', 'h2-eth7': 'nao_classificado'}


pkts = 0

def handle_pkt(x, clazz):
    global pkts
    pkts +=1 
    print('pkt {} - {}'.format(pkts, clazz))
    #print(x[IP].options[0].int_headers)

    sys.stdout.flush()


def main():
    sniff(iface = ["eth0","h2-eth1","h2-eth2","h2-eth3","h2-eth4","h2-eth5","h2-eth6", "h2-eth7"], prn = lambda x: handle_pkt(x, dic[x.sniffed_on]))


if __name__ == '__main__':
    main()