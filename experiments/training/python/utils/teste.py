from scapy.all import *
import pandas as pd
import numpy as np
from decimal import Decimal
import hashlib
import time


def count_flag(val, bit):
    binar = '{0:06b}'.format(val)
    return binar[bit]

df = pd.read_csv("../results/dataset_flow_treino.csv")
df_pkt = pd.read_csv("../results/dataset_pkt2.csv")

df['20%'] = df['pkts'] *0.2
labeled = df[df['label'] == 'benign']
df_pkt_l = df_pkt[df_pkt['label'] == 'benign']

#print ('{} % {} = {}'.format(df['pkts'], df['20%']))



df_flow = pd.DataFrame(columns=[df.columns])
count_ = 0
print ('Dataset loaded')
for index, rowA in labeled.iterrows():
    df_pkt_l2 = df_pkt_l[df_pkt_l['idx_fw'] == rowA['idx_fw']]

    count = 0

    time_pkt = rowA['flow_duration'] / (rowA['pkts']-1)
    #print('pkt {} idx {}'.format(rowA['pkts'], rowA['']))
    for index, rowB in df_pkt_l2.iterrows():
        idx = rowA['idx_fw']
        
        df_flow.at[idx, 'hdr.ethernet.etherType'] = rowB['hdr.ethernet.etherType']
        df_flow.at[idx, 'hdr.ipv4.protocol'] = rowB['hdr.ipv4.protocol']
        df_flow.at[idx, 'ipS'] = rowB['ipS']
        df_flow.at[idx, 'src'] = rowB['src']
        df_flow.at[idx, 'dst'] = rowB['dst']
        df_flow.at[idx, 'UDPSrcPort'] = rowB['UDPSrcPort']
        df_flow.at[idx, 'UDPDstPort'] = rowB['UDPDstPort']
        df_flow.at[idx, 'label'] = rowB['label']
        df_flow.at[idx, 'idx_fw'] = rowB['idx_fw']
        df_flow.at[idx, 'idx_bw'] = rowB['idx_bw']
        df_flow.at[idx, 'label'] = rowB['label']
        
        if count == 0:
            df_flow.at[idx, 'df'] = count_flag(rowB['hdr.ipv4.flags'], 1)
            df_flow.at[idx, 'mf'] = count_flag(rowB['hdr.ipv4.flags'], 2)
            df_flow.at[idx, 'fin'] = count_flag(rowB['hdr.tcp.ctrl'], 0)
            df_flow.at[idx, 'syn'] = count_flag(rowB['hdr.tcp.ctrl'], 1)
            df_flow.at[idx, 'rst'] = count_flag(rowB['hdr.tcp.ctrl'], 2)
            df_flow.at[idx, 'psh'] = count_flag(rowB['hdr.tcp.ctrl'], 3)
            df_flow.at[idx, 'ack'] = count_flag(rowB['hdr.tcp.ctrl'], 4)
            df_flow.at[idx, 'urg'] = count_flag(rowB['hdr.tcp.ctrl'], 5)
            df_flow.at[idx, 'ece'] = count_flag(rowB['hdr.tcp.ecn'], 0)
            df_flow.at[idx, 'cwr'] = count_flag(rowB['hdr.tcp.ecn'], 1)
            df_flow.at[idx, 'hdr.ipv4.totalLen'] = rowB['hdr.ipv4.totalLen']
            df_flow.at[idx, 'flow_duration'] = 0
            df_flow.at[idx, 'min_pkt_len'] = rowB['hdr.ipv4.totalLen']
            df_flow.at[idx, 'max_pkt_len'] = rowB['hdr.ipv4.totalLen']
            df_flow.at[idx, 'pkts'] = 1

        else:
            df_flow.at[idx, 'df'] += count_flag(rowB['hdr.ipv4.flags'], 1)
            df_flow.at[idx, 'mf'] += count_flag(rowB['hdr.ipv4.flags'], 2)
            df_flow.at[idx, 'fin'] += count_flag(rowB['hdr.tcp.ctrl'], 0)
            df_flow.at[idx, 'syn'] += count_flag(rowB['hdr.tcp.ctrl'], 1)
            df_flow.at[idx, 'rst'] += count_flag(rowB['hdr.tcp.ctrl'], 2)
            df_flow.at[idx, 'psh'] += count_flag(rowB['hdr.tcp.ctrl'], 3)
            df_flow.at[idx, 'ack'] += count_flag(rowB['hdr.tcp.ctrl'], 4)
            df_flow.at[idx, 'urg'] += count_flag(rowB['hdr.tcp.ctrl'], 5)
            df_flow.at[idx, 'ece'] += count_flag(rowB['hdr.tcp.ecn'], 0)
            df_flow.at[idx, 'cwr'] += count_flag(rowB['hdr.tcp.ecn'], 1)
            df_flow.at[idx, 'hdr.ipv4.totalLen'] += rowB['hdr.ipv4.totalLen']
            df_flow.at[idx, 'flow_duration'] += time_pkt*count
            df_flow.at[idx, 'min_pkt_len'] += rowB['hdr.ipv4.totalLen']
            df_flow.at[idx, 'max_pkt_len'] += rowB['hdr.ipv4.totalLen']
            df_flow.at[idx, 'pkts'] += 1
        if count % 1000 == 0:
            print ('packets{} / flows {} '.format(count, df_flow.shape))    

        count += 1
    count_ +=1
    print('{}/{}'.format(count_, labeled.shape[0]))
df_flow.to_csv("../results/dataset_flow_treino4.csv",sep=',', encoding='utf-8', index=True)
                
