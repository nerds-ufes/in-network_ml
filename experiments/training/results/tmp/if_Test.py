import numpy as np
import pandas as pd


path = 'results'
df1 = pd.read_csv("{}/iris.csv".format(path))

columns = {}
for c in df1.columns:
    columns[c] = c.replace(" ", "")

df1.rename(columns=columns, inplace=True)   
X = df1.drop(columns=['target'])
y = df1['target'].values

for index, row in df1.iterrows():
    if (TcpDstPort <= 86) 
        if (TcpDstPort <= 23) 
            meta.class = 0;
        else 
            if (PacketSize <= 50) 
                if (hdr.tcp.ctrl <= 10) 
                    meta.class = 1;
                else 
                    meta.class = 0;
            else 
                if (PacketSize <= 468) 
                    meta.class = 1;
                else 
                    meta.class = 0;
    else 
        if (hdr.tcp.ctrl <= 3) 
            if (hdr.ipv4.flags <= 0) 
                meta.class = 6;
            else 
                meta.class = 0;
        else 
            meta.class = 0;
