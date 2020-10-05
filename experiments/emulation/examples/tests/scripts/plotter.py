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
    #     Property  - Mean -  4 methods                 #
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


    #####################################################
    #     Property  - Mean -  3 methods                 #
    #####################################################
    @staticmethod
    def property_avg_3methods_bar(folder1, folder2, folder3, header, scenarios, labels, legends, finallegends, output, title, ylabel, xlabel, ylim, fullwidth=False):
             
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
                    
        result1 = process_average(folder1, scenarios, labels, header)              
        std1 = result1.std()
               
        result2 = process_average(folder2, scenarios, labels, header) 
        std2 = result2.std()
        
        result3 = process_average(folder3, scenarios, labels, header) 
        std3 = result3.std()
              
        
        x=scenarios  
        aa=dict(result1.mean())
        bb=dict(result2.mean())
        cc=dict(result3.mean())
        
        errorbar = [std1, std2, std3]
        
        colors = ['lightpink', 'lightblue', 'lightgreen']
        dfbar = pd.DataFrame({legends[0]: aa, legends[1]: bb, legends[2]: cc}, index=x)
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

    #####################################################
    #     Property  - Mean -  2 methods                 #
    #####################################################
    @staticmethod
    def property_avg_2methods_bar(folder1, folder2, header, scenarios, labels, legends, finallegends, output, title, ylabel, xlabel, ylim, fullwidth=False):
             
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
                    
        result1 = process_average(folder1, scenarios, labels, header)              
        std1 = result1.std()
               
        result2 = process_average(folder2, scenarios, labels, header) 
        std2 = result2.std()            
        
        x=scenarios  
        aa=dict(result1.mean())
        bb=dict(result2.mean())
        
        errorbar = [std1, std2]
        
        colors = ['red', 'darkblue']
        dfbar = pd.DataFrame({legends[0]: aa, legends[1]: bb}, index=x)
        ax4 = dfbar.plot.bar(yerr=errorbar, color=colors, rot=0) 
        
        
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major', labelsize=4)
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', axis='y')
        ax4.set_xticks([0,1,2,3,4,5,6,7,8,9])
        
        ax4.legend(finallegends);
        
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.tight_layout()
        plt.savefig(output) 


    #####################################################
    #     Property  - Mean -  2 methods                 #
    #####################################################
    @staticmethod
    def property_avg_2methods_bar_2(folder1, folder2, header, scenarios, labels, legends, finallegends, output, title, ylabel, xlabel, ylim, fullwidth=False):
             
        plt.figure()
        Plotter.latexify(fullwidth=fullwidth)
                    
        result1 = process_average(folder1, scenarios, labels, header)              
        std1 = result1.std()
               
        result2 = process_average(folder2, scenarios, labels, header) 
        std2 = result2.std()            
        
        x=scenarios  
        aa=dict(result1.mean())
        bb=dict(result2.mean())
        
        errorbar = [std1, std2]
        
        colors = ['red', 'darkblue']
        dfbar = pd.DataFrame({legends[0]: aa, legends[1]: bb}, index=x)
        ax4 = dfbar.plot.bar(yerr=errorbar, color=colors, rot=0) 
        
        
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major', labelsize=4)
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', axis='y')
        ax4.set_xticks([0,1,2,3,4])        
        ax4.legend(finallegends);
        
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.tight_layout()
        plt.savefig(output) 


    @staticmethod
    def multiflow(input_file, rangegraph, title, migrations, output, font_size):
		
        Plotter.latexify(fullwidth=False)
        columns = ['timestamp', 'interface', 'bytes_out/s', 'bytes_in/s', 
                    'bytes_total/s', 'bytes_in', 'bytes_out', 'packets_out/s', 
                    'packets_in/s', 'packets_total/s', 'packets_in', 'packets_out', 
                    'errors_out/s', 'errors_in/s', 'errors_in', 'errors_out']
                
        data_rx = {}   
        
        dfs = pd.read_csv(input_file, header=0, names=columns).drop(columns=['interface'])
        mean = dfs['bytes_in/s'] * 8 * 10**-6

        mean.name = ""

        # mean = dfs['packets_in/s']

        # time = (dfs['timestamp'] - dfs['timestamp'][0])
        # df_rx = pd.DataFrame.from_dict(data_rx)

        plt.figure()
        
        # ax = df_loss.plot()
        for xc,c, src, dst in migrations:
            plt.axvline(x=xc, label='Migration from Path 1 to Path 3'.format(src, dst), c=c, linewidth=1)

        #ax = mean.plot(figsize=(7, 8))
        ax = mean.plot()
    
        ax.set_xlim(rangegraph[0], rangegraph[1])
        ax.set_ylim(rangegraph[2], rangegraph[3])
        #ax.set_yticks(np.arange(0.0, 1100, 100), minor=True)
        #ax.get_yaxis().set_minor_locator(MultipleLocator(100))
        ax.tick_params(axis='both', which='major', labelsize= font_size)
        
        ax.grid(b=True, which='minor', linestyle='dashed', axis='y')
        ax.grid(b=True, which='major', linestyle='dashed', axis='y')
        ax.grid(b=True, which='major', linestyle='dashed', axis='x')

        plt.title(title)
        plt.ylabel('Throughput at H2\_1 (Mbps)', fontsize= font_size)
        plt.xlabel('Time (s)', fontsize= font_size)
        plt.legend(prop={'size':  font_size - 1})

        plt.tight_layout()
        plt.savefig(output)
 
        
    @staticmethod
    def throughput(input_file, is_input, rangegraph, title, migrations, output, ylabel, font_size, fullwidth):

        Plotter.latexify(fullwidth=fullwidth)
        plt.figure()
        
        columns = ['timestamp', 'interface', 'bytes_out/s', 'bytes_in/s', 
                    'bytes_total/s', 'bytes_in', 'bytes_out', 'packets_out/s', 
                    'packets_in/s', 'packets_total/s', 'packets_in', 'packets_out', 
                    'errors_out/s', 'errors_in/s', 'errors_in', 'errors_out']
                        
        dfs = pd.read_csv(input_file, header=0, names=columns).drop(columns=['interface'])
        
        if (is_input):
			mean = dfs['bytes_in/s'] * 8 * 10**-6
        else:
			mean = dfs['bytes_out/s'] * 8 * 10**-6
		
        mean.name = ""
        
        for xc,c, src, dst in migrations:
            plt.axvline(x=xc, label='Migration from Path 1 to Path 3'.format(src, dst), c=c, linewidth=1)

        #ax = mean.plot(figsize=(7, 8))
        ax = mean.plot()
    
        ax.set_xlim(rangegraph[0], rangegraph[1])
        ax.set_ylim(rangegraph[2], rangegraph[3])
        #ax.set_yticks(np.arange(0.0, 1100, 100), minor=True)
        #ax.get_yaxis().set_minor_locator(MultipleLocator(100))
        ax.tick_params(axis='both', which='major', labelsize= font_size)
        
        ax.grid(b=True, which='minor', linestyle='dashed', axis='y')
        ax.grid(b=True, which='major', linestyle='dashed', axis='y')
        ax.grid(b=True, which='major', linestyle='dashed', axis='x')

        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel('Time (s)')
        #plt.legend(prop={'size':  font_size - 1})
        plt.legend()

        plt.tight_layout()
        plt.savefig(output)        
        

    @staticmethod
    def calculate_loss(filerx, filetx):
		
        columns = ['timestamp', 'interface', 'bytes_out/s', 'bytes_in/s', 'bytes_total/s', 
			'bytes_in', 'bytes_out', 'packets_out/s', 'packets_in/s', 
			'packets_total/s', 'packets_in', 'packets_out', 
			'errors_out/s', 'errors_in/s', 'errors_in', 'errors_out']
        
        dfs_rx = pd.read_csv(filerx, header=0, names=columns).drop(columns=['interface'])
        dfs_tx = pd.read_csv(filetx, header=0, names=columns).drop(columns=['interface'])
        totalrx = dfs_rx['bytes_in/s'].sum()
        totaltx = dfs_tx['bytes_out/s'].sum()
        loss = (totaltx-totalrx)*100/totaltx
        #print "TotalTX %s: %d" %(filetx, totaltx)
        #print "TotalRX %s: %d" %(filerx, totalrx)
        #print "Loss: %d \n" %(totaltx-totalrx)
        
        return loss

    @staticmethod
    def calculate_packet_loss(filerx, filetx):
		
        columns = ['timestamp', 'interface', 'bytes_out/s', 'bytes_in/s', 'bytes_total/s', 
			'bytes_in', 'bytes_out', 'packets_out/s', 'packets_in/s', 
			'packets_total/s', 'packets_in', 'packets_out', 
			'errors_out/s', 'errors_in/s', 'errors_in', 'errors_out']
        
        dfs_rx = pd.read_csv(filerx, header=0, names=columns).drop(columns=['interface'])
        dfs_tx = pd.read_csv(filetx, header=0, names=columns).drop(columns=['interface'])
        #totalrx = dfs_rx['bytes_in/s'].sum()
        totalrx = dfs_rx['packets_in'].sum()
        #totaltx = dfs_tx['bytes_out/s'].sum()
        totaltx = dfs_tx['packets_out'].sum()
        loss = (totaltx-totalrx)
        #print "TotalTX %s: %d" %(filetx, totaltx)
        #print "TotalRX %s: %d" %(filerx, totalrx)
        #print "Loss: %d \n" %(totaltx-totalrx)
        
        return loss

    @staticmethod
    def process_loss(folder, scenarios, iterations):
		
        data = []
 
        for scenario in scenarios:
			testdir = folder + '/' + scenario
			for i in range (1,iterations+1):
				filerx = testdir+"/a_"+str(i)+"_rx.bwm"
				filetx = testdir+"/a_"+str(i)+"_tx.bwm"
				#print "filerx: "+filerx
				#print "filetx: "+filetx
				loss = Plotter.calculate_packet_loss(filerx, filetx)
				data += [[scenario, loss]]        
				
        df = pd.DataFrame(data, columns = ['Throughput', 'Loss'])  
        
        return df


    @staticmethod
    def loss(folder1, folder2, scenarios, legends, finallegends, iterations, ylim, title, output, ylabel, xlabel, fullwidth):

        Plotter.latexify(fullwidth=fullwidth)
        plt.figure()
       
        df1 = Plotter.process_loss(folder1, scenarios, iterations)
        result1 = df1.groupby('Throughput')['Loss'].mean()
        #print(result1)
        std1 = df1.groupby('Throughput')['Loss'].std()
        #print(std1)
        
        df2 = Plotter.process_loss(folder2, scenarios, iterations)
        result2 = df2.groupby('Throughput')['Loss'].mean()
        #print(result2)
        std2 = df2.groupby('Throughput')['Loss'].std()
        #print(std2)
                
        x=scenarios  
        aa=dict(result1)
        bb=dict(result2)
        
        errorbar = [std1, std2]
        
        colors = ['red', 'darkblue']
        dfbar = pd.DataFrame({legends[0]: aa, legends[1]: bb}, index=x)
        ax4 = dfbar.plot.bar(yerr=errorbar, color=colors, rot=0) 
             
        ax4.set_ylim(0, ylim)
        ax4.tick_params(axis='both', which='major')
        ax4.grid(b=True, which='major', linestyle='dashed', axis='x')
        ax4.grid(b=True, which='major', axis='y')
        ax4.legend(finallegends);
        
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.tight_layout()
        plt.savefig(output)       
 
        
        
        

		
		
				        
        

        
