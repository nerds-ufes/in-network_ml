from plotter import Plotter

#####################################################
#           Main                                    #
#####################################################

if __name__ == '__main__':
	
	#test_folder= '../local_latency_e2e'	
	#ylim = 25          
	#Plotter.latency_avg_4methods(folder1=test_folder + '/sourcey/data',
			#folder2=test_folder + '/sourcey-fabric/data',
			#folder3=test_folder + '/polka/data',
			#folder4=test_folder + '/polka-fabric/data',
            #scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #title='RTT Latency comparison between PolKA and Sourcey',
            #output= test_folder + '/plot/remote_latency_e2e_4methods.eps',
            #ylim=ylim,
            #fullwidth=False)
            
	#test_folder= '../remote_latency_e2e'	
	#ylim = 40	
   	#Plotter.latency_avg_4methods_bar(folder1=test_folder + '/sourcey/data',
			#folder2=test_folder + '/sourcey-fabric/data',
			#folder3=test_folder + '/polka/data',
			#folder4=test_folder + '/polka-fabric/data',
            #scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #title='RTT Latency comparison between PolKA and Sourcey',
            #output= test_folder + '/plot/remote_latency_e2e_4methods_bar.eps',
            #ylim=ylim,
            #fullwidth=False)
            
	#test_folder= '../remote_latency_e2e_nologs'	
	#ylim = 22	
   	#Plotter.latency_avg_4methods_bar(folder1=test_folder + '/sourcey/data',
			#folder2=test_folder + '/sourcey-fabric/data',
			#folder3=test_folder + '/polka/data',
			#folder4=test_folder + '/polka-fabric/data',
            #scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #title='RTT Latency comparison between PolKA and Sourcey',
            #output= test_folder + '/plot/remote_latency_e2e_4methods_bar_nologs.eps',
            #ylim=ylim,
            #fullwidth=False)
            
	#test_folder= '../remote_latency_e2e_nologs_160b'	
	#ylim = 22	
   	#Plotter.latency_avg_3methods_bar(folder1=test_folder + '/polka/data',
			#folder2=test_folder + '/polka-varheader/data',
			#folder3=test_folder + '/polka-fabric/data',
            #scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #title='RTT Latency comparison between different PolKA implementations',
            #output= test_folder + '/plot/remote_latency_e2e_3methods_bar_nologs_160b.eps',
            #ylim=ylim,
            #fullwidth=False)
            
	#test_folder= '../remote_latency_e2e_nologs_160b'	
	#ylim = 22	
   	#Plotter.latency_avg_4methods_bar(folder1=test_folder + '/sourcey/data',
			#folder2=test_folder + '/sourcey-fabric/data',
			#folder3=test_folder + '/polka/data',
			#folder4=test_folder + '/polka-fabric/data',
            #scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            #title='RTT Latency comparison between PolKA and Sourcey',
            #output= test_folder + '/plot/remote_latency_e2e_4methods_bar_nologs_160b.eps',
            #ylim=ylim,
            #fullwidth=False)
            
	test_folder= '../remote_linear_f100m_b1m _test'	
	ylim = 25	
   	Plotter.property_avg_4methods_bar(folder1=test_folder + '/latency_test/sourcey_bw1',
		folder2=test_folder + '/latency_test/polka_bw1',
		folder3=test_folder + '/latency_test/sourcey-fabric_bw1',
		folder4=test_folder + '/latency_test/polka-fabric_bw1',
		header=4,
		scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
		labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
		legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		title='RTT Latency comparison (Bandwidth 1Mbps)',
		ylabel = 'RTT Latency (ms)',
		xlabel = 'Number of Hops', 
		output= test_folder + '/plot/latency_remote_linear_f100m_b1m _test.eps',
		ylim=ylim,
		fullwidth=False)
            
            
	test_folder= '../remote_linear_f100m_b1m _test'	
	ylim = 1300	
   	Plotter.property_avg_4methods_bar(folder1=test_folder + '/fct_test/sourcey_bw1',
		folder2=test_folder + '/fct_test/polka_bw1',
		folder3=test_folder + '/fct_test/sourcey-fabric_bw1',
		folder4=test_folder + '/fct_test/polka-fabric_bw1',
		header=0,
		scenarios=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
		labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
		legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		title='FCT comparison (File Size 100Mb and Bandwidth 1Mbps)',
		ylabel = 'Flow Completion Time (s)',
		xlabel = 'Number of Hops', 
		output= test_folder + '/plot/fct_remote_linear_f100m_b1m _test.eps',
		ylim=ylim,
		fullwidth=False)
            
