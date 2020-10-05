from scapy.all import *
import pandas as pd
import numpy as np
import subprocess
import argparse
from datetime import datetime


def new_df():
    return pd.DataFrame(columns=['hdr.ethernet.etherType', 'hdr.ipv4.protocol','hdr.ipv4.flags', 'src', 'dst', 'hdr.tcp.ecn', 'hdr.tcp.ctrl', 'UDPSrcPort', 'UDPDstPort', 'hdr.ipv4.totalLen', 'label', 'idx_fw', 'idx_bw','ipS', 'ipD' ])

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
    
def save_dataset(listA, ind, dfBenign, out):
    print ('Adding list into df')
    dfBenign = pd.DataFrame(listA, index=ind, columns=dfBenign.columns)
    print ('saving')
    dfBenign.to_csv("../results/dos_hulk88.csv".format(out),sep=',', encoding='utf-8', index=True)


def extract_features(f_in, list1, ind, dfBenign, max, label):
    scapy_cap = PcapReader(f_in)
    count = 0
    for packet in scapy_cap:
        tsp = 0
        tdp = 0
        usp = 0
        udp = 0
        if packet.haslayer(TCP):
            tsp = packet[TCP].sport
            tdp = packet[TCP].dport
        if packet.haslayer(UDP):
            usp = packet[UDP].sport
            udp = packet[UDP].dport


        l = [0] *len(dfBenign.columns)
        if packet.haslayer(IP):   

            #print ('{} {} - {} {}'.format(packet[Ether].dst, packet[IP].dst, packet[Ether].src,packet[IP].src)) 
            l[1] = packet[IP].proto
            l[9] = packet[IP].len  
            if packet[IP].flags == 'DF': 
                l[2] = 2
            elif packet[IP].flags == 'MF':
                l[2] = 1
            else:
                l[2] = 0
        else: 
            continue
            
        if packet.haslayer(TCP):
            l[5] = tcp_ecn(str(packet[TCP].flags))
            l[6] = tcp_ctrl(str(packet[TCP].flags))
            l[3] = tsp
            l[4] = tdp
        

        if packet.haslayer(UDP):
            l[7] = packet[UDP].sport
            l[8] = packet[UDP].dport

        l[0] = packet[Ether].type
        l[10] = label

        hf = hash('{}{}{}{}{}{}'.format(packet[IP].src, tsp, usp, packet[IP].dst, tdp, udp))
        hb = hash('{}{}{}{}{}{}'.format(packet[IP].dst, tdp, udp, packet[IP].src, tsp, usp))
        ind.append(hf)
        l[11] = hf
        l[12] = hb
        
        l[13] = packet[IP].src
        l[14] = packet[IP].dst

        list1.append(l)

        count += 1
        if count % 10000 == 0:
            print('processando {}={}'.format(label, count))
        if count % 50000 == 0:
            print('PKT {}'.format(len(list1)))
        if max == count and max != 0:
            break

    return ind, list1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process to extract features from pcap.')
    parser.add_argument('-i', help='input pcap file', default='../pcap/wed.pcap')
    parser.add_argument('-o', help='output identifier csv part name of file', default='wed')
    args = parser.parse_args()
    print ("Loading PCAP")
    pd.set_option('precision', 4)

    try: 
        dfBenign = new_df()
        
        listA1 = []
        ind = []
        ind,listA1 = extract_features("../pcap/dos_hulk88.pcap", listA1, ind, dfBenign, 0, 'dos_hulk')

        '''ind,listA1 = extract_features("../pcap/wedB.pcap", listA1, ind, dfBenign, 0,'benign')
        ind,listA1 = extract_features("../pcap/wed_dh.pcap", listA1, ind, dfBenign, 0, 'dos_hulk')
        ind,listA1 = extract_features("../pcap/wed_dge.pcap", listA1, ind, dfBenign, 0,'dos_goldeneye')
        ind,listA1 = extract_features("../pcap/wed_dsh.pcap", listA1, ind, dfBenign, 0, 'dos_slowhttptest')
        ind,listA1 = extract_features("../pcap/wed_dsl.pcap", listA1, ind, dfBenign, 0, 'dos_slowloris')
        #ind,listA1 = extract_features("../pcap/wedh.pcap", listA1, ind, dfBenign, 0, 'Heartblend')


        ind,listA1 = extract_features("../pcap/thu_wabf.pcap", listA1, ind, dfBenign, 0,'wa_brute_force')
        ind,listA1 = extract_features("../pcap/thu_wasi.pcap", listA1, ind, dfBenign, 0, 'wa_sql_injection')
        ind,listA1 = extract_features("../pcap/thu_waxss.pcap", listA1, ind, dfBenign, 0,'wa_xss')
        ind,listA1 = extract_features("../pcap/thu_idb2.pcap", listA1, ind, dfBenign, 0, 'i_portscan')'''
        #print ('init: {}'.format(len(scapy_cap))) # 
    except KeyboardInterrupt: # exit on control-c
        pass
        #save_dataset(listA1, listA2, listB, dfBenign)
    finally:
        save_dataset(listA1, ind, dfBenign, args.o)
