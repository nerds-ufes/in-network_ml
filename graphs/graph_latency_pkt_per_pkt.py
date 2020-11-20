import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import os

import matplotlib as mpl
print(plt.style.available)

plt.grid(True, linestyle="-", alpha=0.5, linewidth=0.5)
# mpl.rcParams["figure.figsize"] = [3.2, 1.98]
mpl.rcParams["xtick.labelsize"] = 7
mpl.rcParams["ytick.labelsize"] = 7
mpl.rcParams["font.size"] = 7
mpl.rcParams["figure.autolayout"] = True
# mpl.rcParams["figure.figsize"] = [3.0, 1.85]
mpl.rcParams["figure.figsize"] = [3.0, 3.1]
mpl.rcParams["axes.titlesize"] = 8
mpl.rcParams["axes.labelsize"] = 8
mpl.rcParams["lines.linewidth"] = 0.5
mpl.rcParams["lines.markersize"] = 6
mpl.rcParams["legend.fontsize"] = 8
mpl.rcParams["mathtext.fontset"] = "stix"
mpl.rcParams["font.family"] = "STIXGeneral"

scenario_list = ["Baseline", "ML/if-then-else"]

root_folder = "./"
experiment_folders = [
    # "sourcey-unicast-fabric_bw10",
    "baseline",
    "tree",
]
my_palette = {
    "ML/if-then-else": "#e74c3c",
    "Baseline": "#3498db",
    # "Sourcey-U": "#3498db",
}

#64, 96, 128, 256, 512, 1024, 1400
def get_values(folder_name, scenario, traffic=1, pkt_size=96):
    values_ping = []
    f_name = "{f}/exp_rate{t}_size{s}.txt".format(
        f=root_folder + folder_name, s=pkt_size, t=traffic
    )
    print(f_name)
    with open(f_name) as f:
        count = 0
        for line in f:
            ping_time = float(line)
            value = {
                "Scenario": scenario,
                "Topic": count,
                "Latency": ping_time / 1000.0,
            }
            values_ping.append(value)
            count += 1
    return values_ping


def generate_chart(name, traffic=1, pkt_size=96):
    df = pd.DataFrame(columns=["Scenario", "Topic", "Latency"])

    for i in range(len(scenario_list)):
        print("Experiment: {}".format(scenario_list[i]))
        df = df.append(
            get_values(
                experiment_folders[i],
                scenario_list[i],
                traffic=traffic,
                pkt_size=pkt_size,
            ),
            ignore_index=True,
        )
    print(df)

    # flierprops = dict(
    #     marker=".",
    #     markerfacecolor="k",
    #     markersize=0.5,
    #     linestyle="none",
    #     markeredgecolor="k",
    # )

    ax = sns.pointplot(
        x="Topic",
        y="Latency",
        hue="Scenario",
        data=df,
        # markers=True,
        # dashes=False,
        # ci=68,
        palette=my_palette,
    )

    # ax = sns.boxplot(
    #     x="Topic",
    #     y="Latency",
    #     hue="Scenario",
    #     linewidth=1.0,
    #     data=df,
    #     whis=1.5,
    #     orient="v",
    #     palette=my_palette,
    #     flierprops=flierprops,
    #     width=0.5,
    # )

    # xlabels = ["Single Path\nfSTA1", "Single Path\nfSTA2", "Multiple Paths\nfSTA1/fSTA2"]
    # ax.set_xticklabels(xlabels)
    ax.set_axisbelow(True)


    xmin, xmax = ax.get_xlim()
    custom_ticks = np.linspace(xmin, xmax, 10, dtype=int)
    ax.set_xticks(custom_ticks)
    ax.set_xticklabels(custom_ticks)


    plt.ylabel("Average core latency ($u$s)")
    # plt.ylim(11, 14)
    # plt.xlim(1, 9)
    plt.xlabel("Packet Size")
    plt.legend(loc="upper left", ncol=1)
    sns.despine()
    plt.savefig(f"{root_folder}{name}.pdf")
    # plt.show()
    del df


if __name__ == "__main__":
    # generate_chart(name="exp_smartnics_lowtraffic_smallpkt")
    # generate_chart(name="exp_smartnics_lowtraffic_bigpkt", pkt_size=1400)
    # generate_chart(name="exp_smartnics_hightraffic_smallpkt", traffic=1024)
    # generate_chart(
    #     name="exp_smartnics_hightraffic_bigpkt", traffic=1024, pkt_size=1400
    # )
    generate_chart(name="PKT_Tree_HC_20480_9000 ", traffic=20480, pkt_size=9000)
    # experiment_folders = [
    #     # "sourcey-unicast-fabric_bw10",
    #     "exp01-mpolka-resubmit/results",
    #     "exp01-mpolka/results",
    # ]
    # generate_chart(name="smartnics", traffic=10240, pkt_size=1400)