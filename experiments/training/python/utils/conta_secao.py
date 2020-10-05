from scapy.all import *
import pandas as pd
import numpy as np
from decimal import Decimal

def new_df():
    return pd.DataFrame(columns=['hdr.ethernet.etherType', 'hdr.ipv4.protocol','ipS', 'ipD', 'src', 'dst', 'UDPSrcPort', 'UDPDstPort', 
                                 'df', 'mf', 
                                 'fin', 'syn', 'rst', 'psh', 'ack', 'urg', 'ece', 'cwr', 
                                 'hdr.ipv4.totalLen', 'first_pkt_time', 'flow_duration', 'min_pck_len', 
                                 'max_pkt_len', 'pkts', 'avg_len', 'ex', 'ex2', 'k', 'len_variance', 
                                 'df_f', 'mf_f', 
                                 'fin_f', 'syn_f', 'rst_f', 'psh_f', 'ack_f', 'urg_f', 'ece_f', 'cwr_f', 
                                 'hdr.ipv4.totalLen_f', 'first_pkt_time_f', 'flow_duration_f', 'min_pck_len_f', 
                                 'max_pkt_len_f', 'pkts_f', 'avg_len_f', 'ex_f', 'ex2_f', 'k_f', 'len_variance_f', 
                                 'df_b', 'mf_b', 
                                 'fin_b', 'syn_b', 'rst_b', 'psh_b', 'ack_b', 'urg_b', 'ece_b', 'cwr_b', 
                                 'hdr.ipv4.totalLen_b', 'first_pkt_time_b', 'flow_duration_b', 'min_pck_len_b', 
                                 'max_pkt_len_b', 'pkts_b', 'avg_len_b', 'ex_b', 'ex2_b', 'k_b', 'len_variance_b',                                                                 
                                 'label'])



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

def preenche(df, idx, end, packet):    
    first = df.at[idx, 'first_pkt_time{}'.format(end)]
    min = df.at[idx, 'min_pck_len{}'.format(end)]
    max = df.at[idx, 'max_pkt_len{}'.format(end)]

    totLen = df.at[idx, 'hdr.ipv4.totalLen{}'.format(end)]
    totLen += packet[IP].len
    df.at[idx, 'hdr.ipv4.totalLen{}'.format(end)] = totLen
    df.at[idx, 'flow_duration{}'.format(end)] = Decimal(packet.time) - Decimal(first)
    pkts = df.at[idx, 'pkts{}'.format(end)]
    pkts += 1
    df.at[idx, 'pkts{}'.format(end)] = pkts
    
    if min > packet[IP].len:
        df.at[idx, 'min_pck_len{}'.format(end)] = packet[IP].len
    if max < packet[IP].len:
        df.at[idx, 'max_pck_len{}'.format(end)] = packet[IP].len
    
    k = df.at[idx, 'k{}'.format(end)]
    y = (packet[IP].len - k) # -k  
    n = pkts

    ex = df.at[idx, 'ex{}'.format(end)] + y
    df.at[idx, 'ex{}'.format(end)] = ex
    ex2 = df.at[idx, 'ex2{}'.format(end)]+ (y * y)
    df.at[idx, ex2] = ex2 

    df.at[idx, 'len_variance{}'.format(end)] = (ex2 - (ex * ex)/n) / (n - 1)

    df.at[idx, 'avg_len{}'.format(end)] = totLen / n

    df.at[idx, 'df{}'.format(end)] += 1 if has_in_flag(packet[IP].flags, 'DF') else 0
    df.at[idx, 'mf{}'.format(end)] += 1 if has_in_flag(packet[IP].flags, 'MF') else 0

    if packet.haslayer(TCP):
        df.at[idx, 'fin{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'F') else 0
        df.at[idx, 'syn{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'S') else 0
        df.at[idx, 'rst{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'R') else 0
        df.at[idx, 'psh{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'P') else 0
        df.at[idx, 'ack{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'A') else 0
        df.at[idx, 'urg{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'U') else 0
        df.at[idx, 'ece{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'E') else 0
        df.at[idx, 'cwr{}'.format(end)] += 1 if has_in_flag(packet[TCP].flags, 'C') else 0

def preenche_primeiro(df, idx, end, packet, tsp, tdp, usp, udp):

    #df.at[idx, 'pkt_per_sec'] = 0
    #df.at[idx, 'bytes_per_sec'] = 0

    df.at[idx, 'hdr.ipv4.totalLen{}'.format(end)] = packet[IP].len 

    df.at[idx, 'df{}'.format(end)] = 1 if has_in_flag(packet[IP].flags, 'DF') else 0
    df.at[idx, 'mf{}'.format(end)] = 1 if has_in_flag(packet[IP].flags, 'MF') else 0

    if packet.haslayer(TCP):
        df.at[idx, 'fin{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'F') else 0
        df.at[idx, 'syn{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'S') else 0
        df.at[idx, 'rst{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'R') else 0
        df.at[idx, 'psh{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'P') else 0
        df.at[idx, 'ack{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'A') else 0
        df.at[idx, 'urg{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'U') else 0
        df.at[idx, 'ece{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'E') else 0
        df.at[idx, 'cwr{}'.format(end)] = 1 if has_in_flag(packet[TCP].flags, 'C') else 0
    else:
        df.at[idx, 'fin{}'.format(end)] = 0
        df.at[idx, 'syn{}'.format(end)] = 0
        df.at[idx, 'rst{}'.format(end)] = 0
        df.at[idx, 'psh{}'.format(end)] = 0
        df.at[idx, 'ack{}'.format(end)] = 0
        df.at[idx, 'urg{}'.format(end)] = 0
        df.at[idx, 'ece{}'.format(end)] = 0
        df.at[idx, 'cwr{}'.format(end)] = 0                
    
    df.at[idx, 'min_pck_len{}'.format(end)] = packet[IP].len
    df.at[idx, 'max_pkt_len{}'.format(end)] = packet[IP].len
    df.at[idx, 'first_pkt_time{}'.format(end)] = packet.time
    df.at[idx, 'flow_duration{}'.format(end)] = 0
    df.at[idx, 'pkts{}'.format(end)] = 1
    df.at[idx, 'k{}'.format(end)] = packet[IP].len
    df.at[idx, 'ex{}'.format(end)] = 0
    df.at[idx, 'ex2{}'.format(end)] = 0
    df.at[idx, 'avg_len{}'.format(end)] = packet[IP].len
    
    df.at[idx, 'len_variance{}'.format(end)] = 0


def extract_features(f_in, max_f, label):
    scapy_cap = PcapReader(f_in)
    count = 0
    df = new_df()
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

        if not packet.haslayer(IP):   
            continue

        hf = hash('{}{}{}{}{}{}'.format(packet[IP].src, tsp, usp, packet[IP].dst, tdp, udp))
        hb = hash('{}{}{}{}{}{}'.format(packet[IP].dst, tdp, udp, packet[IP].src, tsp, usp))
        row = None
        in_hf = hf in df.index
        in_hb = 0
        idx = 0
        if not in_hf: 
            in_hb = hb in df.index

        if in_hf:
            idx = hf
            preenche(df, idx, '_f', packet)  
        elif in_hb:
            idx = hb
            preenche(df, idx, '_b', packet)               
        else:
            idx = hf
            df.at[idx, 'hdr.ethernet.etherType'] = packet[Ether].type
            df.at[idx, 'hdr.ipv4.protocol'] = packet[IP].proto
            df.at[idx, 'ipS'] = packet[IP].src 
            df.at[idx, 'ipD'] = packet[IP].dst 
            df.at[idx, 'src'] = tsp
            df.at[idx, 'dst'] = tdp
            df.at[idx, 'UDPSrcPort'] = usp
            df.at[idx, 'UDPDstPort'] = udp

            preenche_primeiro(df, idx, '', packet, tsp, tdp, usp, udp)
            preenche_primeiro(df, idx, '_f', packet, tsp, tdp, usp, udp)
            preenche_primeiro(df, idx, '_b', packet, tsp, tdp, usp, udp)

        df.at[idx, 'label'] = label
        if max_f == df.shape[0]:
            print('breaking {} == {}'.format(max_f, df.shape[0]))
            break

        if count % 10000 == 0:
            print ('packets {}={} / Session {}'.format(label, count, df.shape))    
        count += 1
    #    if packet[IP].src == '40.83.143.209' and packet[IP].dst == '192.168.1000000.14' and tdp == 49461: 
    #        print (row.at['len_variance'])
    return df

df =  new_df()
try: 
    pd.set_option('precision', 4)

    df1 = extract_features("../pcap/wedB.pcap", 1000000,'benign')
    df2 = extract_features("../pcap/wed_dh.pcap", 1000000, 'dos_hulk')
    df3 = extract_features("../pcap/wed_dge.pcap", 1000000,'dos_goldeneye')
    df4 = extract_features("../pcap/wed_dsh.pcap", 1000000, 'dos_slowhttptest')
    df5 = extract_features("../pcap/wed_dsl.pcap", 1000000, 'dos_slowloris')
    #df6 = extract_features("../pcap/wedh.pcap", 1000000, 'Heartblend')

    df7 = extract_features("../pcap/thu_wabf.pcap", 1000000,'wa_brute_force')
    df8 = extract_features("../pcap/thu_wasi.pcap", 1000000, 'wa_sql_injection')
    df9 = extract_features("../pcap/thu_waxss.pcap", 1000000,'wa_xss')
    df1000000 = extract_features("../pcap/thu_idb2.pcap", 1000000, 'i_portscan')

    frames = [df1, df2, df3, df4, df5, df7, df8, df9, df1000000] #df6,
    df = pd.concat(frames)

except KeyboardInterrupt: # exit on control-c
    pass
finally:
    #df.drop(columns=['ipS', 'ipD', 'first_pkt_time', 'ex', 'ex2', 'k'], inplace=True)
    df.to_csv("../results/dataset_session2.csv",sep=',', encoding='utf-8', float_format='%.4f') #, index=True
                


    



