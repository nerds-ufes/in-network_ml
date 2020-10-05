from plotter import Plotter

#####################################################
#           Main                                    #
#####################################################

if __name__ == '__main__':
            


################################################################################################################

	#test_folder= '../server/linear'	
	#ylim = 16	
   	#Plotter.property_avg_4methods_bar(folder1=test_folder + '/latency_test/sourcey_bw10',
		#folder2=test_folder + '/latency_test/polka_bw10',
		#folder3=test_folder + '/latency_test/sourcey-fabric_bw10',
		#folder4=test_folder + '/latency_test/polka-fabric_bw10',
		#header=4,
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		#finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		#title='RTT (Frame size 98 bytes, Links 10Mbps)',
		#ylabel = 'RTT (ms)',
		#xlabel = 'Number of hops in the core network', 
		#output= test_folder + '/plot/linear_latency_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)

	#test_folder= '../server/linear'	
	#ylim = 16	
   	#Plotter.property_avg_4methods_bar(folder1=test_folder + '/latency_test_bigpacket/sourcey_bw10',
		#folder2=test_folder + '/latency_test_bigpacket/polka_bw10',
		#folder3=test_folder + '/latency_test_bigpacket/sourcey-fabric_bw10',
		#folder4=test_folder + '/latency_test_bigpacket/polka-fabric_bw10',
		#header=4,
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		#finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		#title='RTT (Frame size 1242 bytes, Links 10Mbps)',
		#ylabel = 'RTT (ms)',
		#xlabel = 'Number of hops in the core network', 
		#output= test_folder + '/plot/linear_latency_bigpacket_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)

	#test_folder= '../server/linear'	
	#ylim = 16	
   	#Plotter.property_avg_4methods_bar(folder1=test_folder + '/latency_test_btraffic/sourcey_bw10',
		#folder2=test_folder + '/latency_test_btraffic/polka_bw10',
		#folder3=test_folder + '/latency_test_btraffic/sourcey-fabric_bw10',
		#folder4=test_folder + '/latency_test_btraffic/polka-fabric_bw10',
		#header=4,
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		#finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		#title='RTT (Frame size 98 bytes, Background Traffic 5Mbps, Links 10Mbps)',
		#ylabel = 'RTT (ms)',
		#xlabel = 'Number of hops in the core network', 
		#output= test_folder + '/plot/linear_latency_btraffic_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)
		
	#test_folder= '../server/linear'	
	#ylim = 120	
   	#Plotter.property_avg_4methods_bar(folder1=test_folder + '/fct_test/sourcey_bw10',
		#folder2=test_folder + '/fct_test/polka_bw10',
		#folder3=test_folder + '/fct_test/sourcey-fabric_bw10',
		#folder4=test_folder + '/fct_test/polka-fabric_bw10',
		#header=0,
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		#finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		#title='FCT (File Size 100Mb and Links 10Mbps)',
		#ylabel = 'Flow Completion Time (s)',
		#xlabel = 'Number of hops in the core network', 
		#output= test_folder + '/plot/linear_fct_f100m_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)
		
	#test_folder= '../server/linear'	
	#ylim = 0.3	
   	#Plotter.property_avg_4methods_bar(folder1=test_folder + '/jitter_test/sourcey_bw10',
		#folder2=test_folder + '/jitter_test/polka_bw10',
		#folder3=test_folder + '/jitter_test/sourcey-fabric_bw10',
		#folder4=test_folder + '/jitter_test/polka-fabric_bw10',
		#header=4,
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
		#legends = ['(1)Sourcey', '(2)PolKA', '(3)Sourcey Fabric','(4)PolKA Fabric'],
		#finallegends = ['Sourcey', 'PolKA', 'Sourcey Fabric','PolKA Fabric'],
		#title='Jitter (Throughput 5Mbps and Links 10Mbps)',
		#ylabel = 'Jitter (ms)',
		#xlabel = 'Number of hops in the core network', 
		#output= test_folder + '/plot/linear_jitter_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)
	
	#test_folder= '../server/sfc'	
	#ylim = 30	
   	#Plotter.property_avg_2methods_bar(folder1=test_folder + '/latency_test/sourcey-fabric_bw10',
		#folder2=test_folder + '/latency_test/polka-fabric_bw10',
		#header=4,		
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],            
		#title='RTT for SFC (Frame size 98 bytes, Links 10Mbps)',
		#ylabel = 'RTT (ms)',
		#xlabel = 'Chain length', 		
		#output= test_folder + '/plot/sfc_latency_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)	

	#test_folder= '../server/sfc'	
	#ylim = 120	
   	#Plotter.property_avg_2methods_bar(folder1=test_folder + '/fct_test/sourcey-fabric_bw10',
		#folder2=test_folder + '/fct_test/polka-fabric_bw10',
		#header=0,		
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],            
		#title='FCT for SFC (File Size 100Mb and Links 10Mbps)',
		#ylabel = 'Flow Completion Time (s)',
		#xlabel = 'Chain length', 
		#output= test_folder + '/plot/sfc_fct_f100m_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)	
	
	#test_folder= '../server/sfc'	
	#ylim = 0.3	
   	#Plotter.property_avg_2methods_bar(folder1=test_folder + '/jitter_test/sourcey-fabric_bw10',
		#folder2=test_folder + '/jitter_test/polka-fabric_bw10',
		#header=4,
		#scenarios=['0', '1', '2', '3', '4', '5', '6', '7', '8'],
		#labels=['0', '1', '2', '3', '4', '5', '6', '7', '8'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],    
		#title='Jitter for SFC (Throughput 5Mbps and Links 10Mbps)',
		#ylabel = 'Jitter (ms)',
		#xlabel = 'Chain length', 
		#output= test_folder + '/plot/sfc_jitter_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)


	#test_folder= '../server/sfc'	
	#ylim = 15	
   	#Plotter.property_avg_2methods_bar_2(folder1=test_folder + '/latency_test_2/sourcey-fabric_bw10',
		#folder2=test_folder + '/latency_test_2/polka-fabric_bw10',
		#header=4,		
		#scenarios=['1', '2', '3', '4'],
		#labels=['1', '2', '3', '4'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],            
		#title='RTT for SFC (Frame size 98 bytes, Links 10Mbps)',
		#ylabel = 'RTT (ms)',
		#xlabel = 'Number of hops in the core network per SFC segment', 		
		#output= test_folder + '/plot/sfc2_latency_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)	

	#test_folder= '../server/sfc'	
	#ylim = 120	
   	#Plotter.property_avg_2methods_bar_2(folder1=test_folder + '/fct_test_2/sourcey-fabric_bw10',
		#folder2=test_folder + '/fct_test_2/polka-fabric_bw10',
		#header=0,		
		#scenarios=['1', '2', '3', '4'],
		#labels=['1', '2', '3', '4'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],            
		#title='FCT for SFC (File Size 100Mb and Links 10Mbps)',
		#ylabel = 'Flow Completion Time (s)',
		#xlabel = 'Number of hops in the core network per SFC segment', 
		#output= test_folder + '/plot/sfc2_fct_f100m_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)	
	
	#test_folder= '../server/sfc'	
	#ylim = 0.2	
   	#Plotter.property_avg_2methods_bar_2(folder1=test_folder + '/jitter_test_2/sourcey-fabric_bw10',
		#folder2=test_folder + '/jitter_test_2/polka-fabric_bw10',
		#header=4,
		#scenarios=['1', '2', '3', '4'],
		#labels=['1', '2', '3', '4'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],    
		#title='Jitter for SFC (Throughput 5Mbps and Links 10Mbps)',
		#ylabel = 'Jitter (ms)',
		#xlabel = 'Number of hops in the core network per SFC segment', 
		#output= test_folder + '/plot/sfc2_jitter_b10m.eps',
		#ylim=ylim,
		#fullwidth=False)

	#test_folder= '../server/topo'
	#Plotter.multiflow(test_folder +'/pmigration_test/polka_bw10/throughput.bwm', 
		#rangegraph=(0, 70, 0, 12),
		#title="Path Migration PolKA (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_pmigration_polka_b10m.eps')	
		
	#test_folder= '../server/topo'
	#Plotter.multiflow(test_folder +'/pmigration_test/sourcey_bw10/throughput.bwm', 
		#rangegraph=(0, 70, 0, 12),
		#title="Path Migration Sourcey (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_pmigration_sourcey_b10m.eps')	
				
	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/polka_bw10/5000/a_1_tx.bwm', 
		#is_input =0,
		#rangegraph=(0, 70, 0, 10),
		#ylabel = 'Throughput at H1\_1 (Mbps)',
		#title="Traffic at Source for Path Migration Polka (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_tx_5M_polka_b10m.eps',
		#fullwidth=False)	

	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/polka_bw10/4000/a_1_rx.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#ylabel = 'Throughput at H2\_1 (Mbps)',
		#title="Traffic at Destination for Path Migration Polka (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_rx__4M_polka_b10m.eps',
		#fullwidth=False)
		
	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/polka_bw10/5000/a_1_s1-eth1.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#title="Path Migration Polka (Links 10Mbps)",
		#ylabel = 'Throughput at S1\_eth1 (Mbps)',
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_s1_eth1_5M_polka_b10m.eps',
		#fullwidth=False)
		
	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/polka_bw10/5000/a_1_s2-eth1.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#title="Path Migration Polka (Links 10Mbps)",
		#ylabel = 'Throughput at S2\_eth1 (Mbps)',
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_s2_eth1__5M_polka_b10m.eps',
		#fullwidth=False)		

	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/sourcey_bw10/5000/a_1_tx.bwm', 
		#is_input =0,
		#rangegraph=(0, 70, 0, 10),
		#ylabel = 'Throughput at H1\_1 (Mbps)',
		#title="Traffic at Source for Path Migration Sourcey (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_tx_5M_sourcey_b10m.eps',
		#fullwidth=False)	

	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/sourcey_bw10/5000/a_1_rx.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#ylabel = 'Throughput at H2\_1 (Mbps)',
		#title="Traffic at Destination for Path Migration Sourcey (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_rx__5M_sourcey_b10m.eps',
		#fullwidth=False)
		
	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/sourcey_bw10/5000/a_1_s1-eth1.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#title="Path Migration Sourcey (Links 10Mbps)",
		#ylabel = 'Throughput at S1\_eth1 (Mbps)',
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_s1_eth1_5M_sourcey_b10m.eps',
		#fullwidth=False)
		
	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss/sourcey_bw10/5000/a_1_s2-eth1.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#title="Path Migration Sourcey (Links 10Mbps)",
		#ylabel = 'Throughput at S2\_eth1 (Mbps)',
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_s2_eth1__5M_sourcey_b10m.eps',
		#fullwidth=False)		

		
	#test_folder= '../server/topo'
	#ylim = 0.01
	#Plotter.loss(
		#folder1=test_folder +'/pmigration_test_loss/sourcey_bw10', 
		#folder2=test_folder +'/pmigration_test_loss/polka_bw10',
		#scenarios=['1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],  
		#iterations=3,
		#ylim=ylim,
		#title="Path Migration (Links 10Mbps)",
		#ylabel = 'Loss (\%)',
		#xlabel = 'Throughput at source', 		
		#output=test_folder + '/plot/topo_loss_b10m.eps',
		#fullwidth=False)


	test_folder= '../server/topo'
	ylim = 100
	Plotter.loss(
		folder1=test_folder +'/pmigration_test_loss_packet1200/sourcey_bw10', 
		folder2=test_folder +'/pmigration_test_loss_packet1200/polka_bw10',
		scenarios=['1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000'],
		legends = ['(1)Sourcey', '(2)PolKA'],
		finallegends = ['Sourcey', 'PolKA'],  
		iterations=3,
		ylim=ylim,
		title="Path Migration (Links 10Mbps)",
		ylabel = 'Loss (Packets)',
		xlabel = 'Throughput at source', 		
		output=test_folder + '/plot/topo_pkt1200_loss_b10m.eps',
		fullwidth=False)


	#test_folder= '../server/topo'
	#ylim = 50
	#Plotter.loss(
		#folder1=test_folder +'/pmigration_test_loss_packet100/sourcey_bw10', 
		#folder2=test_folder +'/pmigration_test_loss_packet100/polka_bw10',
		#scenarios=['1000', '2000', '3000', '4000'],
		#legends = ['(1)Sourcey', '(2)PolKA'],
		#finallegends = ['Sourcey', 'PolKA'],  
		#iterations=3,
		#ylim=ylim,
		#title="Path Migration (Links 10Mbps)",
		#ylabel = 'Loss (packets)',
		#xlabel = 'Throughput at source', 		
		#output=test_folder + '/plot/topo_pkt100_loss_b10m.eps',
		#fullwidth=False)

	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss_packet100/polka_bw10/3000/a_1_rx.bwm', 
		#is_input =1,
		#rangegraph=(0, 70, 0, 10),
		#ylabel = 'Throughput at H2\_1 (Mbps)',
		#title="Traffic at Destination for Path Migration Polka (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_rx_pkt100_3M_polka_b10m.eps',
		#fullwidth=False)
		
	#test_folder= '../server/topo'
	#Plotter.throughput(
		#input_file = test_folder +'/pmigration_test_loss_packet100/polka_bw10/4000/a_1_tx.bwm', 
		#is_input =0,
		#rangegraph=(0, 70, 0, 10),
		#ylabel = 'Throughput at H1\_1 (Mbps)',
		#title="Traffic at Source for Path Migration Polka (Links 10Mbps)",
		#font_size=5,
		#migrations=[(40, 'r', '1', '3')],
		#output=test_folder + '/plot/topo_tx_pkt100_4M_polka_b10m.eps',
		#fullwidth=False)
