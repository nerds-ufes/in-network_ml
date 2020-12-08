import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def load_dateset(dir, rate, size, df_ ):
    if df_ is None:
        df_ = pd.DataFrame()
    f_name = "{f}/exp_rate{t}_size{s}.txt".format(
        f=dir, s=size, t=rate
    )
    df = pd.read_csv(f_name, header=None, names=['lat'])

    #df_[f'{dir}: {rate} Mpps: {size} Bytes'] = df['lat']
    df_[f'{rate} Mpps'] = df['lat']

    return df_

def load_rate(dir, rate, df_, size):
    for dir in dir:
        for x in size:
            df_ = load_dateset(dir, rate, x, df_)
    return df_    
def load_rate2(dir, rate, df_, size ):
    for dir in dir:
        for x in size:
            df_ = load_dateset(dir, rate, x, df_)
    return df_   

def main(rel, dir, name, size):
    df = pd.DataFrame()
    if rel == 1:
        df = load_rate(dir, 1, df, size)
        #df = load_rate(dir, 10, df, size)
        df = load_rate(dir, 1000, df, size)
        df = load_rate(dir, 5000, df, size)
        df = load_rate(dir, 10000, df, size)
        df = load_rate(dir, 15000, df, size)
        df = load_rate(dir, 20000, df, size)
    elif rel == 2:    
        df = load_rate(dir, 100, df, size)
        df = load_rate(dir, 1000, df, size)
    elif rel == 3:    
        df = load_rate2(dir, 1, df, size)
        #df = load_rate2(dir, 10, df, size)
    elif rel == 4:    
        #df = load_rate2(dir, 102, pd.DataFrame(), size)
        df = load_rate2(dir, 1000, df, size)


    print(df)
    nm = ''
    if args.kde:
        g = sns.kdeplot(data=df, cumulative=True)
        nm = 'kde'
    elif args.cdf:
        g = sns.ecdfplot(data=df)
        g.set(xlabel = 'Latency ($u$s)', ylabel = 'Cumulative Distribution Function')
        nm = 'cdf'
    elif args.cat:    
        g = sns.catplot(data=df)
        nm = 'cat'
    elif args.bar:
        sns.catplot(data=df, kind="bar")
        nm = 'bar'
    elif args.box:
        sns.boxplot(data=df)    
        nm = 'box'
    elif args.his:
        sns.histplot(data=df)        
        nm = 'his'
    plt.savefig(f"{name}_{nm}.pdf")
    plt.show()


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-kde', help='kde plot', action='store_true')
parser.add_argument('-cdf', help='cdf plot (default)', action='store_true')
parser.add_argument('-cat', help='cat plot', action='store_true')
parser.add_argument('-bar', help='bar plot', action='store_true')
parser.add_argument('-box', help='box plot', action='store_true')
parser.add_argument('-his', help='his plot', action='store_true')

args = parser.parse_args()

print(args)

dir2 = ['tree']
dir3 = ['flow']
dir1 = ['baseline']
#main(1, dir1, 'plot_rat_BL', [26244])
#main(1, dir2, 'plot_rat_TREE', [26244])
main(1, dir3, 'plot_rat_FLOW', [26244])


