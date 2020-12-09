import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def load_dateset(dir, df_ ):
    if df_ is None:
        df_ = pd.DataFrame()
    f_name = "baseline/pktgen1.txt"
    df = pd.read_csv(f_name, header=None, names=['lat'])

    #df_[f'{dir}: {rate} Mpps: {size} Bytes'] = df['lat']
    df_[f'10Mpps'] = df['lat']

    df = df_

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
    elif args.lin:
        sns.lineplot(data=df)
    
    plt.savefig(f"pktgen1.pdf")
    plt.show()


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-kde', help='kde plot', action='store_true')
parser.add_argument('-cdf', help='cdf plot (default)', action='store_true')
parser.add_argument('-cat', help='cat plot', action='store_true')
parser.add_argument('-bar', help='bar plot', action='store_true')
parser.add_argument('-box', help='box plot', action='store_true')
parser.add_argument('-his', help='his plot', action='store_true')
parser.add_argument('-lin', help='lin plot', action='store_true')

args = parser.parse_args()

print(args)

dir2 = ['tree']
dir3 = ['flow']
dir1 = ['baseline']
#main(1, dir1, 'plot_rat_BL', [26244])
#main(1, dir2, 'plot_rat_TREE', [26244])
load_dateset(dir1, None)


