import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def identify_unique():
    df = pd.read_csv(f'flow/flow.txt', header=None, names=['idx', 'lat'], sep=',')
    df['pkt'] = 0
    count = 0
    ant = ''
    for i in range(0, len(df)):
        #print(df.iloc[i]['idx'])
        if ant != df.iloc[i]['idx']:
            ant = df.iloc[i]['idx']
            count+=1
        df.loc[i, 'pkt'] = count   
    df = df.drop(columns=['idx'])
    df.to_csv("flow/flow2.txt",sep=',', encoding='utf-8', index=False)



#identify_unique()

df = pd.read_csv(f'flow/flow2.txt', sep=',')

g = sns.relplot(x='pkt', y='lat', kind="line", data=df)
g.set(xlabel = 'Packet Size (Bytes)', ylabel = 'Latency ($u$s)')
#plt.savefig(f"{name}_{rel}2.pdf")
plt.show()