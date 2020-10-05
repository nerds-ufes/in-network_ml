import glob
import math

import brewer2mpl
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

SPINE_COLOR = 'gray'

#####################################################
#     Process average from files                    #
#####################################################
def process_average(folder, scenarios, labels, header):
	columns = ['property']
	dfs1 = []
	for scenario in scenarios:
		file = glob.glob(folder + '/' + scenario + '/a1*')
		df = pd.read_csv(file[0], header=header, names=columns)['property']
		df.name = labels[scenarios.index(scenario)]
		dfs1 += [df]
	
	result = pd.concat(dfs1, axis=1)               
	
	return result

class Plotter():

    #####################################################
    #           Latexify                                #
    #####################################################
    @staticmethod
    def latexify(fig_width=None, fig_height=None, columns=1, fullwidth=False):
        """Set up matplotlib's RC params for LaTeX plotting.
        Call this before plotting a figure.

        Parameters
        ----------
        fig_width : float, optional, inches
        fig_height : float,  optional, inches
        columns : {1, 2}
        """

        # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

        # Width and max height in inches for IEEE journals taken from
        # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

        assert(columns in [1,2])

        if fig_width is None:
            if fullwidth:
                fig_width = 3.39*2 if columns==1 else 6.9 # width in inches
            else:
                fig_width = 3.39 if columns==1 else 6.9 # width in inches

        if fig_height is None:
            golden_mean = (math.sqrt(5)-1.0)/2.0    # Aesthetic ratio
            if fullwidth:
                fig_height = fig_width*golden_mean/2.0 # height in inches
            else:
                fig_height = fig_width*golden_mean # height in inches
                

        MAX_HEIGHT_INCHES = 8.0
        if fig_height > MAX_HEIGHT_INCHES:
            print("WARNING: fig_height too large:" + fig_height + 
                "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
            fig_height = MAX_HEIGHT_INCHES

        params = {
                'backend': 'ps',
                'text.latex.preamble': ['\\usepackage{amssymb}'],
                'axes.labelsize': 5, # fontsize for x and y labels (was 10)
                'axes.titlesize': 5,
                'lines.markersize' : 3,
                'lines.markeredgewidth': 0.3,
                'legend.fontsize': 4, # was 10
                'text.usetex': True,
                'legend.edgecolor': 'w', 
                'figure.figsize': [fig_width, fig_height],
                'font.family': 'serif',
                'grid.linestyle': 'dashed',
                'grid.color': 'grey',
                'lines.dashed_pattern' : [150, 150],
                'xtick.color': 'k',
                'ytick.color': 'k',
                'xtick.direction': 'in',
                'ytick.direction': 'in',
                'xtick.minor.width': 0.05,
                'ytick.minor.width': 0.05,   
                'xtick.major.width': 0.1,
                'ytick.major.width': 0.1,           
                'xtick.labelsize': 4,
                'ytick.labelsize': 4,
                'lines.linewidth' : 0.2,
                'grid.linewidth': 0.01,       
                'axes.linewidth': 0.2,
                'errorbar.capsize' : 1,
                'xtick.minor.visible': False,  # visibility of minor ticks on x-axis
                #   'ytick.minor.visible': False,  # visibility of minor ticks on x-axis

                'boxplot.notch': False,
                'boxplot.vertical': True,
                'boxplot.whiskers': 1.5,
                'boxplot.bootstrap': None,
                'boxplot.patchartist': False,
                'boxplot.showmeans': False,
                'boxplot.showcaps': True,
                'boxplot.showbox': True,
                'boxplot.showfliers': True,
                'boxplot.meanline': False,

                'boxplot.flierprops.color': 'lightgrey',
                'boxplot.flierprops.marker': 'o',
                'boxplot.flierprops.markerfacecolor': 'none',
                'boxplot.flierprops.markeredgecolor': 'lightgrey',
                'boxplot.flierprops.markersize': 1,
                'boxplot.flierprops.linestyle': 'none',
                'boxplot.flierprops.linewidth': 0.1,

                'boxplot.boxprops.color': 'C2',
                'boxplot.boxprops.linewidth': 0.2,
                'boxplot.boxprops.linestyle': '-',

                'boxplot.whiskerprops.color': 'C2',
                'boxplot.whiskerprops.linewidth': 0.2,
                'boxplot.whiskerprops.linestyle': '-',

                'boxplot.capprops.color': 'C2',
                'boxplot.capprops.linewidth': 0.2,
                'boxplot.capprops.linestyle': '-',

                'boxplot.medianprops.color': 'C2',
                'boxplot.medianprops.linewidth': 0.20,
                'boxplot.medianprops.linestyle': '-',

                'boxplot.meanprops.color': 'C2',
                'boxplot.meanprops.marker': '^',
                'boxplot.meanprops.markerfacecolor': 'C2',
                'boxplot.meanprops.markeredgecolor': 'C2',
                'boxplot.meanprops.markersize':  6,
                'boxplot.meanprops.linestyle': 'none',
                'boxplot.meanprops.linewidth': 0.20,
        }

        matplotlib.rcParams.update(params)

        # for spine in ['top', 'right']:
        #     ax.spines[spine].set_visible(False)

        # for spine in ['left', 'bottom']:
        #     ax.spines[spine].set_color(SPINE_COLOR)
        #     ax.spines[spine].set_linewidth(0.1)

        # ax.xaxis.set_ticks_position('bottom')
        # ax.yaxis.set_ticks_position('left')

        # # Or if you want different settings for the grids:
        # ax.grid(which='minor', alpha=0.2)
        # ax.grid(which='major', alpha=0.5)

        # for axis in [ax.xaxis, ax.yaxis]:
        #     axis.set_tick_params(direction='out', color=SPINE_COLOR)

        # return ax



    #####################################################
    #     Latency  - Mean -  4 methods                  #
    #####################################################
    @staticmethod
    def latency_avg_4methods(folder1, folder2, folder3, folder4, scenarios, labels, output, title, ylim, fullwidth=False):
        
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
        
        columns = ['latency']

        dfs1 = []

        for scenario in scenarios:
            file = glob.glob(folder1 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=4, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs1 += [df]
                
        result1 = pd.concat(dfs1, axis=1)
        
        #print('result1\n', result1.describe())
        #print('result1\n', result1.to_string())
               
        std1 = result1.std()
        ax1 = result1.mean().plot(label="Sourcey", legend = True, yerr=std1, color="red")
        ax1.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
        
        
        dfs2 = []
        for scenario in scenarios:
            file = glob.glob(folder2 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs2 += [df]
                
        result2 = pd.concat(dfs2, axis=1)
        
        #print('result2\n', result2.describe())
        #print('result2\n', result2.to_string())
        
        std2 = result2.std()
        ax2 = result2.mean().plot(label="Sourcey Fabric", legend = True, yerr=std2, color="orange")
        ax2.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
        

        dfs3 = []
        for scenario in scenarios:
            file = glob.glob(folder3 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs3 += [df]
                
        result3 = pd.concat(dfs3, axis=1)
        
        #print('result3\n', result3.describe())
        #print('result3\n', result3.to_string())
        
        std3 = result3.std()
        ax3 = result3.mean().plot(label="PolKA", legend = True, yerr=std3, color="blue")
        ax3.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
        
        
        dfs4 = []
        for scenario in scenarios:
            file = glob.glob(folder4 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs4 += [df]
                
        result4 = pd.concat(dfs4, axis=1)
        
        #print('result4\n', result4.describe())
        #print('result4\n', result4.to_string())
        
        std4 = result4.std()
        ax4 = result4.mean().plot(label="PolKA Fabric", legend = True, yerr=std4, color="green")
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major', labelsize=5)
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', linestyle='dashed', axis='y')
        ax4.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
                
                
        plt.title(title)
        plt.ylabel('RTT Latency (s)')
        plt.xlabel('Number of Hops')
        plt.tight_layout()
        plt.savefig(output) 
        
        
    #####################################################
    #     Latency  - Mean -  4 methods                  #
    #####################################################
    @staticmethod
    def latency_avg_4methods_bar(folder1, folder2, folder3, folder4, scenarios, labels, output, title, ylim, fullwidth=False):
             
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
        
        columns = ['latency']

        dfs1 = []
        for scenario in scenarios:
            file = glob.glob(folder1 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=4, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs1 += [df]
                
        result1 = pd.concat(dfs1, axis=1)               
        std1 = result1.std()
      
        
        dfs2 = []
        for scenario in scenarios:
            file = glob.glob(folder2 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs2 += [df]
               
        result2 = pd.concat(dfs2, axis=1)
        std2 = result2.std()
        

        dfs3 = []
        for scenario in scenarios:
            file = glob.glob(folder3 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs3 += [df]              
        result3 = pd.concat(dfs3, axis=1)
        std3 = result3.std()
        
        dfs4 = []
        for scenario in scenarios:
	        file = glob.glob(folder4 + '/' + scenario + '/a1*')
	        df = pd.read_csv(file[0], header=None, names=columns)['latency']
	        df.name = labels[scenarios.index(scenario)]
	        dfs4 += [df]
        
        result4 = pd.concat(dfs4, axis=1)        
        std4 = result4.std()      
        
        x=scenarios  #since the date are the same in both tables I only have 1 x
        aa=dict(result1.mean())
        bb=dict(result2.mean())
        cc=dict(result3.mean())
        dd=dict(result4.mean())
        
        errorbar = [std1, std2, std3, std4]
        
        colors = ['lightpink', 'lightblue', 'red', 'darkblue']
        dfbar = pd.DataFrame({'(1)Sourcey': aa, '(3)Sourcey Fabric': bb, '(2)PolKA': cc,'(4)PolKA Fabric': dd}, index=x)
        ax4 = dfbar.plot.bar(yerr=errorbar, color=colors, rot=0) 
        
        
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major', labelsize=4)
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', axis='y')
        ax4.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
                
        plt.title(title)
        plt.ylabel('RTT Latency (s)')
        plt.xlabel('Number of Hops')
        plt.tight_layout()
        plt.savefig(output) 

    #####################################################
    #     Latency  - Mean -  3 methods                  #
    #####################################################
    @staticmethod
    def latency_avg_3methods_bar(folder1, folder2, folder3, scenarios, labels, output, title, ylim, fullwidth=False):
             
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
        
        columns = ['latency']

        dfs1 = []
        for scenario in scenarios:
            file = glob.glob(folder1 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=4, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs1 += [df]
                
        result1 = pd.concat(dfs1, axis=1)               
        std1 = result1.std()
      
        
        dfs2 = []
        for scenario in scenarios:
            file = glob.glob(folder2 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs2 += [df]
               
        result2 = pd.concat(dfs2, axis=1)
        std2 = result2.std()
        

        dfs3 = []
        for scenario in scenarios:
            file = glob.glob(folder3 + '/' + scenario + '/a1*')
            df = pd.read_csv(file[0], header=None, names=columns)['latency']
            df.name = labels[scenarios.index(scenario)]
            dfs3 += [df]              
        result3 = pd.concat(dfs3, axis=1)
        std3 = result3.std()  
        
        x=scenarios  #since the date are the same in both tables I only have 1 x
        aa=dict(result1.mean())
        bb=dict(result2.mean())
        cc=dict(result3.mean())
        
        errorbar = [std1, std2, std3]
        
        colors = ['lightpink', 'lightgreen', 'lightblue']
        dfbar = pd.DataFrame({'1 PolKA': aa, '2 PolKA Var Header': bb, '3 PolKA Fabric': cc}, index=x)
        ax4 = dfbar.plot.bar(yerr=errorbar, color=colors, rot=0) 
        
        
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major', labelsize=4)
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', axis='y')
        ax4.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
        
        
        plt.title(title)
        plt.ylabel('RTT Latency (s)')
        plt.xlabel('Number of Hops')
        plt.tight_layout()
        plt.savefig(output) 


    #####################################################
    #     Latency  - Mean -  4 methods                  #
    #####################################################
    @staticmethod
    def property_avg_4methods_bar(folder1, folder2, folder3, folder4, header, scenarios, labels, legends, finallegends, output, title, ylabel, xlabel, ylim, fullwidth=False):
             
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
                    
        result1 = process_average(folder1, scenarios, labels, header)              
        std1 = result1.std()
               
        result2 = process_average(folder2, scenarios, labels, header) 
        std2 = result2.std()
        
        result3 = process_average(folder3, scenarios, labels, header) 
        std3 = result3.std()
               
        result4 = process_average(folder4, scenarios, labels, header)         
        std4 = result4.std()      
        
        x=scenarios  
        aa=dict(result1.mean())
        bb=dict(result2.mean())
        cc=dict(result3.mean())
        dd=dict(result4.mean())
        
        errorbar = [std1, std2, std3, std4]
        
        colors = ['lightpink', 'lightblue', 'red', 'darkblue']
        dfbar = pd.DataFrame({legends[0]: aa, legends[1]: bb, legends[2]: cc, legends[3]: dd}, index=x)
        ax4 = dfbar.plot.bar(yerr=errorbar, color=colors, rot=0) 
        
        
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major', labelsize=4)
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', axis='y')
        ax4.set_xticks([0,1,2,3,4,5,6,7,8,9,10])
        
        ax4.legend(finallegends);
        
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.tight_layout()
        plt.savefig(output) 


