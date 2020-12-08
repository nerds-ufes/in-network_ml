import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

pd.options.display.float_format = '{:.2f}'.format

def identify_unique():
    df = pd.read_csv(f'flow/flow.txt', header=None, names=['idx', 'lat'], sep=',')
    df['pkt'] = 0
    count = 0
    ant = ''
    df = df.sort_index(axis = 0)
    for i in range(0, len(df)):
        #print(df.iloc[i]['idx'])
        if ant != df.iloc[i]['idx']:
            ant = df.iloc[i]['idx']
            count+=1

        if (i % 10000 == 0):
            print(f'Processando {count} fluxos e {i} pacotes')

        df.loc[i, 'pkt'] = count   
    df = df.drop(columns=['idx'])
    df.to_csv("flow/flow2.txt",sep=',', encoding='utf-8', index=False)

def sumarize():
    df = pd.read_csv(f'flow/flow.txt', header=None, names=['idx', 'lat'], sep=',')
    df = df[df['lat'] < 100000]  
    #df = pd.read_csv(f'flow/flow.txt', sep=',')

    avg = df.groupby(['idx'])['lat'].mean().reset_index()
    '''max = df.groupby(['idx'])['lat'].max().reset_index()
    min = df.groupby(['idx']).min().reset_index()
    std = df.groupby('idx').agg(np.std, ddof=0).reset_index()
    avg['max'] = max['lat']
    avg['min'] = min['lat']
    avg['std'] = std['lat']'''

    print(avg)
    #avg = avg.drop(columns=['idx'])

    avg.to_csv("flow/flow3.txt",sep=',', encoding='utf-8', index=True, float_format="%.2f")

def graph():
    df = pd.read_csv(f'flow/flow3.txt', sep=',')
    #df = df.head(20000)
    #g = sns.histplot(data=df)  
    g = sns.relplot(y='lat', x='Unnamed: 0', kind="line", data=df)
    #g.set(xlabel = 'Flows', ylabel = 'Latency ($u$s)')
    plt.savefig(f"flow2.pdf")
    plt.show()



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-i', help='identify_unique', action='store_true')
parser.add_argument('-s', help='sumarize', action='store_true')
parser.add_argument('-g', help='graph', action='store_true')

args = parser.parse_args()



if args.i:
    identify_unique()
if args.s:
    sumarize()
if args.g:
    graph()
if not args.i and not args.s and not args.g:
    parser.print_help()

