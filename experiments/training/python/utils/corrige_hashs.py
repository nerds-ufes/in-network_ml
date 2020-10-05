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


def converte_hash_secao2():
    df = pd.read_csv("../results/dataset_session.csv")
   
    df['idx_fw'] = df.apply(lambda row: hash_md5(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort']), axis = 1)
    df['idx_bw'] = df.apply(lambda row: hash_md5(row['ipD'], row['dst'], row['UDPDstPort'], row['ipS'], row['src'], row['UDPSrcPort']), axis = 1)
    df['pkts'] = df.apply(lambda row: row['pkts_f']+ row['pkts_b'], axis = 1)
    
    df.to_csv("../results/dataset_session2.csv",sep=',', encoding='utf-8', index=False)



def converte_hash_secao():
    df = pd.read_csv("../results/dataset_session.csv")

    df['idx_fw'] = None
    df['idx_bw'] = None

    for index, row in df.iterrows():
        hf = '{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort'])
        hb = '{}{}{}{}{}{}'.format(row['ipD'], row['dst'], row['UDPDstPort'], row['ipS'], row['src'], row['UDPSrcPort'])

        df.at[index,'idx_fw'] = hashlib.md5(hf.encode("utf-8")).hexdigest()
        df.at[index,'idx_bw'] = hashlib.md5(hb.encode("utf-8")).hexdigest()

        df.at[index,'pkts'] = df.at[index,'pkts_f'] + df.at[index,'pkts_b']

        print('pkts {} /// sum {}'.format(df.at[index,'pkts'], df.at[index,'pkts_f'] + df.at[index,'pkts_b']))

        count += 1
        if count % 10000 == 0:
            print('session transform count: {}'.format(count))
            
    df.to_csv("../results/dataset_session2.csv",sep=',', encoding='utf-8', index=False)

def converte_hash_pkt():
    df = pd.read_csv("../results/dataset_pkt.csv")
    df.drop(columns=['idx_fw', 'idx_bw'])

    df['idx_fw'] = None
    df['idx_bw'] = None
    count = 0
    for index, row in df.iterrows():
        hf = '{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort'])
        hb = '{}{}{}{}{}{}'.format(row['ipD'], row['dst'], row['UDPDstPort'], row['ipS'], row['src'], row['UDPSrcPort'])

        df.at[index,'idx_fw'] = hashlib.md5(hf.encode("utf-8")).hexdigest()
        df.at[index,'idx_bw'] = hashlib.md5(hb.encode("utf-8")).hexdigest()
        count += 1
        if count % 10000 == 0:
            print('pkt transform count: {}'.format(count))
            
    df.to_csv("../results/dataset_pkt2.csv",sep=',', encoding='utf-8', index=False)

def converte_hash_flow():
    df = pd.read_csv("../results/dataset_flow.csv")
    df.drop(columns=['idx_bw'])

    df['idx_fw'] = None
    df['idx_bw'] = None
    count = 0
    for index, row in df.iterrows():
        hf = '{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort'])
        hb = '{}{}{}{}{}{}'.format(row['ipD'], row['dst'], row['UDPDstPort'], row['ipS'], row['src'], row['UDPSrcPort'])

        df.at[index,'idx_fw'] = hashlib.md5(hf.encode("utf-8")).hexdigest()
        df.at[index,'idx_bw'] = hashlib.md5(hb.encode("utf-8")).hexdigest()
        count += 1
        if count % 10000 == 0:
            print('flow transform count: {}'.format(count))
            
    df.to_csv("../results/dataset_flow2.csv",sep=',', encoding='utf-8', index=False)

if __name__ == "__main__":

    pd.set_option('precision', 4)
    parser = argparse.ArgumentParser(description='Process to evaluate datasets.')
    parser.add_argument('-sec', help='Converte hash of session dataset', action='store_true', default=False, dest='sec')
    parser.add_argument('-flow', help='Converte hash of flow dataset', action='store_true', default=False, dest='flow')
    parser.add_argument('-pkt', help='Converte hash of packet dataset', action='store_true', default=False, dest='pkt')
    args = parser.parse_args()

    if args.sec:
        converte_hash_secao2()
    
    if args.pkt:
        converte_hash_pkt()

    if args.flow:
        converte_hash_flow()