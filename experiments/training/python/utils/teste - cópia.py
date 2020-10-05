from scapy.all import *
import pandas as pd
import numpy as np
from decimal import Decimal
import time

df = pd.read_csv("../results/dataset_session_teste.csv")
df2 = pd.DataFrame(df)
start_time = time.time()
for index, row in df2.iterrows():

    in_hf = index in df.index
    row2 = None
    if in_hf:
        row2 = df.loc[index]
    
    row2.at['psh'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10
    row2.at['label'] = 10

print("Ex1.1 --- %s seconds ---" % (time.time() - start_time))    

start_time = time.time()
for index, row in df2.iterrows():
    in_hf = index in df.index
    row2 = None
    
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10
    df.at[index, 'label'] = 10



print("Ex1.2 --- %s seconds ---" % (time.time() - start_time))    

start_time = time.time()
for index, row in df2.iterrows():
    hf = hash('{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort']))
    hb = hash('{}{}{}{}{}{}'.format(row['ipD'], row['dst'], row['UDPDstPort'], row['ipS'], row['src'], row['UDPSrcPort']))

    in_hf = hf in df.index
    in_hb = hb in df.index

    if in_hf:
        row = df.iloc[hf]
    elif in_hb:
        row = df.iloc[hb]



print("Ex2 --- %s seconds ---" % (time.time() - start_time))    


start_time = time.time()
for index, row in df2.iterrows():
    hf = hash('{}{}{}{}{}{}'.format(row['ipS'], row['src'], row['UDPSrcPort'], row['ipD'], row['dst'], row['UDPDstPort']))
    hb = hash('{}{}{}{}{}{}'.format(row['ipD'], row['dst'], row['UDPDstPort'], row['ipS'], row['src'], row['UDPSrcPort']))

    in_hf = hf in df.index
    in_hb = hb in df.index

    if in_hf:
        row = df.ix[hf]
    elif in_hb:
        row = df.ix[hb]



print("Ex3 --- %s seconds ---" % (time.time() - start_time))    

