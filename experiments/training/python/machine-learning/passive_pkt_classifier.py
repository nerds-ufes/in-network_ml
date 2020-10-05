from scapy.all import *
import pandas as pd
import numpy as np
import subprocess
import argparse
from datetime import datetime
from sklearn.externals import joblib


from decimal import Decimal
import time

def new_df(col):
    return pd.DataFrame(columns=col)



print ("Loading PCAP")


def get_ip_flag(flags):
    if flags == 'DF': 
        return 1
    elif flags == 'MF':
        return 2
    else:
        return 0

def tcp_ecn(flag):
    count = 0
    if ('E' in flag):
        count += 1   
    if ('C' in flag):
        count += 2
    if ('N' in flag):
        count += 4
    return count 

def tcp_ctrl(flag):
    count = 0
    if ('F' in flag):
        count += 1      
    if ('S' in flag):
        count += 2     
    if ('R' in flag):
        count += 4     
    if ('P' in flag):
        count += 8  
    if ('A' in flag):
        count += 16    
    if ('U' in flag):
        count += 32    
    return count 

def has_in_flag(flag, s):
    return True if s in str(flag) else False


def pkt_classifier(label, model):
    df = pd.read_csv("../results/dos_hulk88.csv")

    df = df[df['label']==label]
    idx = df['idx_fw']
    df = df.drop(columns=['Unnamed: 0', 'src', 'UDPSrcPort','UDPDstPort', 'label','idx_fw','idx_bw','ipS','ipD'])
    predicted = model.predict(df)
    df['label'] = predicted
    #df = df.drop(columns=['hdr.ethernet.etherType','hdr.ipv4.protocol','hdr.ipv4.flags','dst','hdr.tcp.ecn','hdr.tcp.ctrl','UDPDstPort','hdr.ipv4.totalLen'])
    df['idx'] = idx
    df.to_csv("../results/pkt_88{}_passiva.csv".format(label),sep=',', encoding='utf-8', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process to extract features from pcap.')
    parser.add_argument('-i', help='input pcap file')
    args = parser.parse_args()
    print ("Loading PCAP")

    try: 

        loaded_model = joblib.load('../results/tmp/finalized_model_DT.sav')
        '''pkt_classifier('benign',  loaded_model)

        pkt_classifier('dos_hulk',  loaded_model)
        pkt_classifier('dos_goldeneye',  loaded_model)
        pkt_classifier('dos_slowhttptest',  loaded_model)
        pkt_classifier('wa_brute_force',  loaded_model)
        pkt_classifier('dos_slowloris',  loaded_model)
        pkt_classifier('i_portscan',  loaded_model)'''
        pkt_classifier('dos_hulk',  loaded_model)


    except KeyboardInterrupt: # exit on control-c
        pass
