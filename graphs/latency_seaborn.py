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

def load_rate(rate, df_ ):
    for dir in ["baseline", "tree"]:
        for x in [1024, 512, 256, 128, 64]:
            df_ = load_dateset(dir, rate, x, df_)
    return df_    

def main(rel):
    if rel == 1:
        df = load_rate(1, pd.DataFrame())
        df = load_rate(10, df)
    elif rel == 2:    
        df = load_rate(102, pd.DataFrame())
        df = load_rate(1024, df)

    g = sns.relplot(x='pkts', y='lat', hue="scenario", style="throwput", markers=True, err_style="bars", sort=False, kind="line", data=df)
    g.set(xlabel = 'Packet Size (Bytes)', ylabel = 'Latency ($u$s)')
    plt.savefig(f"plot_{rel}.pdf")
    plt.show()

main(1)
main(2)