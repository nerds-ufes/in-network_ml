import pandas as pd
import numpy as np
import random
import argparse

def new_df_pkt(cols):
    return pd.DataFrame(columns=cols)

def new_df_flow():
    return pd.DataFrame(columns=['hdr.ethernet.etherType', 'hdr.ipv4.protocol','ipS', 'ipD', 'df', 'mf', 'fin', 'syn', 'rst', 'psh', 'ack', 'urg', 'ece', 'cwr', 'src', 'dst',  
                                 'UDPSrcPort', 'UDPDstPort', 'hdr.ipv4.totalLen', 'first_pkt_time', 'flow_duration', 
                                 'min_pkt_len', 'max_pkt_len', 'pkts', 'avg_len', 'ex', 'ex2', 'k', 'len_variance', 'label', 'idx_bw'])


amostras = ['treino', 'teste']


def amostra(qt, div, label, df_s, df_p): 
    print('amostra de {}'.format(label))
    df = new_df_pkt(df_p.columns)

    labeled = df_s[df_s['label'] == label]
    n = (int) (qt/div)
    if n > labeled.shape[0]:
        n = labeled.shape[0]    
    r = labeled.sample(n=n) # Quatro pacotes de cada seção, se possível
    
    tmp1 = labeled[labeled['idx_fw'].isin(r['idx_fw'])]
    print (tmp1.shape)
    tmp2 = labeled[labeled['idx_fw'].isin(r['idx_bw'])]
    frames = [tmp1, tmp2]
    tmp =  pd.concat(frames) # seleciona pacotes forward e backward aleatóriamente
    print(tmp.shape)
    sample = tmp.sample(n=qt)
    df = sample

    return df

def amostra_flow(qt, div, label, df_s, df_p): 

    labeled = df_p[df_p['label'] == label]
    n = (int) (qt/div)
    if n > labeled.shape[0]:
        n = labeled.shape[0]

    r = labeled.sample(n=n) # Quatro pacotes de cada seção, se possível
    tmp1 = labeled[labeled['idx_fw'].isin(r['idx_fw'])]

    print(tmp1.shape)
  
    n = qt
    if n > tmp1.shape[0]:
        n = tmp1.shape[0]
    sample = tmp1.sample(n=n)
    return sample

def amostra_flow_age(qt, div, label, df_s, df_p): 

    labeled = df_p[df_p['label'] == label]
    n = (int) (qt/div)
    if n > labeled.shape[0]:
        n = labeled.shape[0]

    r = labeled.sample(n=n) # Quatro pacotes de cada seção, se possível
    tmp1 = labeled[labeled['idx_bw'].isin(r['idx_bw'])]

    print(tmp1.shape)
  
    n = qt
    if n > tmp1.shape[0]:
        n = tmp1.shape[0]
    sample = tmp1.sample(n=n)
    return sample


def prepara_sec(df_s, l):
    print('Reading dataset_flow')
    df_p = df_s
     
    div = 0.8    
    df1 = amostra_flow(l[0], div, 'benign', df_s, df_p)
    df2 = amostra_flow(l[1], div, 'dos_hulk', df_s, df_p)
    df3 = amostra_flow(l[2], div, 'dos_goldeneye', df_s, df_p)
    df4 = amostra_flow(l[3], div, 'dos_slowhttptest', df_s, df_p)
    df5 = amostra_flow(l[4], div, 'dos_slowloris', df_s, df_p)
    df6 = amostra_flow(l[5], div, 'wa_brute_force', df_s, df_p)
    #df7 = amostra_flow(10, div, 'wa_sql_injection', df_s, df_p) # poucos pacotes
    df8 = amostra_flow(l[6], div, 'i_portscan', df_s, df_p)

    frames = [df1, df2, df3, df4, df5, df6, df8] #df6,
    df = pd.concat(frames)

    df.to_csv("../results/dataset_sec_treino.csv",sep=',', encoding='utf-8', index=False)

    df1 = amostra_flow(l[0], div, 'benign', df_s, df_p)
    df2 = amostra_flow(l[1], div, 'dos_hulk', df_s, df_p)
    df3 = amostra_flow(l[2], div, 'dos_goldeneye', df_s, df_p)
    df4 = amostra_flow(l[3], div, 'dos_slowhttptest', df_s, df_p)
    df5 = amostra_flow(l[4], div, 'dos_slowloris', df_s, df_p)
    df6 = amostra_flow(l[5], div, 'wa_brute_force', df_s, df_p)
    #df7 = amostra_flow(10, div, 'wa_sql_injection', df_s, df_p) # poucos pacotes
    df8 = amostra_flow(l[6], div, 'i_portscan', df_s, df_p)

    frames = [df1, df2, df3, df4, df5, df6, df8] #df6,
    df = pd.concat(frames)

    df.to_csv("../results/dataset_sec_teste.csv",sep=',', encoding='utf-8', index=False)    

def exec(df_s, df_p, param, func, list):
    print('Reading dataset_pkt')
     
    div = 0.8    
    for x in amostras:
        df1 = func(list[0], div, 'benign', df_s, df_p) # 0
        df2 = func(list[1], div, 'dos_hulk', df_s, df_p) # 1
        df3 = func(list[2], div, 'dos_goldeneye', df_s, df_p) # 2
        df4 = func(list[3], div, 'dos_slowhttptest', df_s, df_p) # 3
        df5 = func(list[4], div, 'dos_slowloris', df_s, df_p) # 4
        df6 = func(list[5], div, 'wa_brute_force', df_s, df_p) # 5
        #df7 = amostra_flow(10, div, 'wa_sql_injection', df_s, df_p) # poucos pacotes
        df8 = func(list[6], div, 'i_portscan', df_s, df_p)  # 6

        frames = [df1, df2, df3, df4, df5, df6, df8] #df6,
        df = pd.concat(frames)

        df.to_csv("../results/dataset_{}_{}.csv".format(param, x),sep=',', encoding='utf-8', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process to prepare samples.')
    parser.add_argument('-pkt', help='Evaluate packet dataset', action='store_true', default=False, dest='pkt')
    parser.add_argument('-flow', help='Evaluate flow dataset', action='store_true', default=False, dest='flow')
    parser.add_argument('-flow_age', help='Evaluate flow dataset with age of flow', action='store_true', default=False, dest='flow_age')
    parser.add_argument('-sec', help='Evaluate flow dataset', action='store_true', default=False, dest='sec')
    args = parser.parse_args()
 
    print('Reading dataset_session')
    df_s = pd.read_csv("../results/dataset_session2.csv", index_col="idx")





    l = [964232, 12518, 1000, 800, 581, 800, 1229]
    #l = [10, 10, 10, 10, 10, 10, 10]

    if args.pkt:
        df_p = pd.read_csv("../results/dataset_pkt2.csv")
        exec(df_s, df_p, 'pkt', amostra, l)
        #prepara_pkt(df_s, l)

    if args.flow:
        df_p = pd.read_csv("../results/dataset_flow.csv")
        exec(df_s, df_p, 'flow', amostra_flow, l)
        #prepara_flow(df_s, l)

     if args.flow_age:
        df_p = pd.read_csv("../results/dataset_flow.csv")
        exec(df_s, df_p, 'flow_age', amostra_flow, l)
        #prepara_flow(df_s, l)
        #        
    if args.sec:
        prepara_sec(df_s, l)
    

