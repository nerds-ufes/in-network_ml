import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_dateset(dir, rate, size, df_ ):

    f_name = "{f}/exp_rate{t}_size{s}.txt".format(
        f=dir, s=size, t=rate
    )
    df = pd.read_csv(f_name, header=None, names=['lat'])

    df['scenario'] = dir
    df['throwput'] = rate
    df['pkts'] = size #(1000000*rate)/(size+20)
    
    return pd.concat([df_, df])

def load_rate(dir, rate, df_ ):
    for dir in dir:
        for x in [1024, 512, 256, 128, 64]:
            df_ = load_dateset(dir, rate, x, df_)
    return df_    
def load_rate2(dir, rate, df_ ):
    for dir in dir:
        for x in [9000, 8192, 4096, 2048]:
            df_ = load_dateset(dir, rate, x, df_)
    return df_   

def main(rel, dir, name):
    if rel == 1:
        df = load_rate(dir, 1, pd.DataFrame())
        df = load_rate(dir, 10, df)
    elif rel == 2:    
        df = load_rate(dir, 102, pd.DataFrame())
        df = load_rate(dir, 1024, df)
    elif rel == 3:    
        df = load_rate2(dir, 1, pd.DataFrame())
        df = load_rate2(dir, 10, df)
    elif rel == 4:    
        df = load_rate2(dir, 102, pd.DataFrame())
        df = load_rate2(dir, 1024, df)

    g = sns.relplot(x='pkts', y='lat', hue="scenario", style="throwput", markers=True, err_style="bars", sort=False, kind="line", data=df)
    g.set(xlabel = 'Packet Size (Bytes)', ylabel = 'Latency ($u$s)')
    plt.savefig(f"{name}_{rel}.pdf")
    plt.show()

dir1 = ['baseline', 'tree']
dir2 = ['baseline_e', 'tree_e']
main(1, dir1, 'plot_rat')
main(2, dir1, 'plot_rat')
main(3, dir2, 'plot_elephant')
main(4, dir2, 'plot_elephant')