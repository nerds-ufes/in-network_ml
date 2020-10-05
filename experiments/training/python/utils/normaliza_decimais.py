from scapy.all import *
import pandas as pd
import numpy as np
from decimal import Decimal
import argparse

def flow():
    df = pd.read_csv("../results/dataset_flow.csv")
    pd.set_option('precision', 4)
    #pd.options.display.float_format = "{:,.4f}".format

    df.to_csv("../results/dataset_flow1.csv",sep=',', encoding='utf-8', index=False, columns=['hdr.ethernet.etherType', 'hdr.ipv4.protocol', 'dst','UDPSrcPort', 'UDPDstPort','df', 'mf', 'fin', 'syn', 'psh', 'ack', 'urg', 'ece', 'cwr',   
                                 'hdr.ipv4.totalLen', 'flow_duration', 'min_pck_len', 'max_pkt_len', 'pkts', 'avg_len', 'len_variance', 'label'], float_format='%.4f')

def pkt():
    df = pd.read_csv("../results/dataset_pkt.csv")
    pd.set_option('precision', 4)
    #pd.options.display.float_format = "{:,.4f}".format

    df.to_csv("../results/dataset_pkt1.csv",sep=',', encoding='utf-8', index=False, columns=['hdr.ethernet.etherType', 'hdr.ipv4.protocol','hdr.ipv4.flags','dst', 'hdr.tcp.ecn', 'hdr.tcp.ctrl', 'UDPSrcPort', 'UDPDstPort', 'hdr.ipv4.totalLen', 'label'], float_format='%.4f')




pd.set_option('precision', 4)
parser = argparse.ArgumentParser(description='Process to evaluate datasets.')
parser.add_argument('-pkt', help='Evaluate packet dataset', action='store_true', default=False, dest='pkt')
parser.add_argument('-flow', help='Evaluate flow dataset', action='store_true', default=False, dest='flow')
args = parser.parse_args()

if args.pkt:
    print ('Transforme packet dataset')
    pkt()
if args.flow:
    print ('Transforme flow dataset')
    flow()