#!/usr/bin/python

from p4app import P4Mininet
from p4app import P4Mininet, P4Program
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg
from mininet.util import dumpNodeConnections, custom
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

from util.monitor import monitor_devs_ng, monitor_cpu

import shlex
import sys
import os, shutil


class TwoTierTopo(Topo):
	def __init__(self, nspine, nleaf, nports, core_file, edge_file, **opts):
		Topo.__init__(self, **opts)

		spines = []
		core_prog = P4Program(core_file)
		edge_prog = P4Program(edge_file)        
		nhost = nports - nspine 
		
		for s in xrange(1, nspine+1):
			spine = self.addSwitch('s%d' % s, program=core_prog)
			spines.append(spine)			
		
		for l in xrange(1, nleaf+1):
			leaf = self.addSwitch('l%d' % l, program=core_prog)
			
			for i in xrange(0, nspine):
				spine = spines[i]
				self.addLink( spine, leaf)			
				
			for i in xrange(1, nhost+1):
				ip = "10.0.%d.%d" %(l,  i)
				mac = '00:00:00:00:%02x:%02x' %(l,  i)
				host = self.addHost('h%d_%d' %(l,  i), ip = ip, mac = mac)
				edge = self.addSwitch('e%d_%d' %(l,  i), program=edge_prog)		
				self.addLink(edge, leaf)
				self.addLink(host, edge)
				


def config_network(bw, method, nspine, nleaf, nports):

	core_file = method+"-core.p4"
	edge_file = method+"-edge.p4"
	
	topo = TwoTierTopo(nspine, nleaf, nports, core_file, edge_file)
	link = custom(TCLink, bw=bw)
	net = P4Mininet(program=core_file, topo=topo, link=link)
	net.start()
	
	nhost = nports - nspine

	print 'Switches Configuration'
	
	for s in xrange(1, nspine+1):
		spine = net.get('s%d'% s)
		fname = 'cfg/'+method+'-fabric/s%d'% s+'-commands.txt'
		print 'Configuring switch: '+'s%d'% s
		print 'Config filename: '+fname
		with open(fname, 'r') as file:
			cmd = file.read()
		spine.command(cmd)

	for l in xrange(1, nleaf+1):
		leaf = net.get('l%d'% l)
		fname = 'cfg/'+method+'-fabric/l%d'% l+'-commands.txt'
		print 'Configuring switch: '+'l%d'% l
		print 'Config filename: '+fname
		with open(fname, 'r') as file:
			cmd = file.read()
		leaf.command(cmd)
		for i in xrange(1, nhost+1):
			edge = net.get('e%d_%d' %(l,  i))
			fname = 'cfg/'+method+'-fabric/e%d_%d' %(l,  i)+'-commands.txt'
			print 'Configuring switch: '+'e%d_%d' %(l,  i)
			print 'Config filename: '+fname
			with open(fname, 'r') as file:
				cmd = file.read()
			edge.command(cmd)			

		
	return net


def run_path_migration_test_tcp(net, bw, testdir, method):

	print "Starting path migration test - TCP"	
	

	pmigrationdir = testdir+"/pmigration_test"
	path = os.getcwd()+"/"+pmigrationdir
	
	if(not(os.path.exists(path))):
		os.mkdir(path)

	outputfolder = "%s_bw%s" %(method, bw)
	path = path + "/"+outputfolder		
	
	if(os.path.exists(path)):
		shutil.rmtree(path)

	os.mkdir(path)
	

	#Source of TCP traffic
	h1_1 = net.get('h1_1')
	#Destination of TCP traffic
	h2_1 = net.get('h2_1')	
	#Source of TCP concurrent traffic	
	h1_2 = net.get('h1_2')
	#Destination of TCP concurrent traffic
	h3_1 = net.get('h3_1')	
	#Edge switch
	e1_1 = net.get('e1_1')

	#Start servers
	#h3_1.cmd('iperf -s -u -l 1200 > /dev/null &')
	h3_1.cmd('iperf -s -M 1200 > /dev/null &')
	h2_1.cmd('iperf -s -M 1200 > /dev/null &')
	
	## Start the bandwidth monitor in the background for destination interface
	filenamerx = path+"/rx.bwm"
	h2_1.cmd("bwm-ng -t 1000 -I eth0 -o csv -u bytes -T rate -C ',' > %s &" %filenamerx)
	
	#filenametx = path+"/tx.bwm"
	#h1_1.cmd("bwm-ng -t 1000 -I eth0 -o csv -u bytes -T rate -C ',' > %s &" %filenametx)
	
	result = h1_1.cmd("netstat -s -t")
	print result
		
	sleep(10)
	
	#monitor = Process(target=monitor_devs_ng, args=('%s/%s.bwm' % (path,filename), 1.0))
	#monitor.start()
	
	#Start TCP concurrent traffic
	#h1_2.cmd('iperf -c 10.0.3.1 -u -b 500k -l 1200 -t 75 > /dev/null &')
	h1_2.cmd('iperf -c 10.0.3.1 -M 1200 -t 70 > /dev/null &')
	#Start TCP flow
	h1_1.cmd('iperf -c 10.0.2.1 -M 1200 -t 70 > /dev/null &')
	
	sleep(30)

	#https://github.com/p4lang/behavioral-model
	#table_set_default <table name> <action name> <action parameters>
	#table_add <table name> <action name> <match fields> => <action parameters> [priority]
	#table_delete <table name> <entry handle>
	#https://github.com/p4lang/PI/blob/master/CLI/table_add.c
	#"table_add <table name> <match fields> [priority] => ""[<action name> <action parameters> | <indirect handle>]";
	#https://github.com/p4lang/p4factory/blob/master/cli/pd_cli.py
	
	#https://github.com/p4lang/behavioral-model/blob/master/tools/runtime_CLI.py#L1103
	#"Add entry to a match table: table_modify <table name> <action name> <entry handle> [action parameters]"
	
	#Migration
	#result = e1_1.command('table_delete tunnel_encap_process_sr 1')
	#print result
	if (method == "sourcey"):
		#cmd = 'table_add tunnel_encap_process_sr add_header_3hops 10.0.2.1/32 => 1 1 00:00:00:00:02:01 0 2 0 2 1 3'
		cmd = 'table_modify tunnel_encap_process_sr add_header_3hops 1 => 1 1 00:00:00:00:02:01 0 2 0 2 1 3'
	else:
		#cmd = 'table_add tunnel_encap_process_sr add_sourcerouting_header 10.0.2.1/32 => 1 1 00:00:00:00:02:01 179902035595884'
		cmd = 'table_modify tunnel_encap_process_sr add_sourcerouting_header 1 => 1 1 00:00:00:00:02:01 179902035595884'
	result = e1_1.command(cmd)
	#print result
	
	sleep(50)
	
	result = h1_1.cmd("netstat -s -t")
	print result
	
	#monitor.terminate()
	
	os.system("killall -9 iperf")
	sleep(10)
	os.system("killall -9 bwm-ng")

	#Return original rules for next iteration
	if (method == "sourcey"):
		cmd = 'table_modify tunnel_encap_process_sr add_header_3hops 1 => 1 1 00:00:00:00:02:01 0 1 0 2 1 3'
	else:
		cmd = 'table_modify tunnel_encap_process_sr add_sourcerouting_header 1 => 1 1 00:00:00:00:02:01 71955628459531'
	result = e1_1.command(cmd)
	
	#https://stackoverflow.com/questions/21309020/remove-odd-or-even-lines-from-a-text-file
	#keep odd lines: sed 'n; d' infile > outfile
	#keep even lines: sed '1d; n; d' infile > outfile
	#Remove total lines
	outputrx = path+"/throughput.bwm"
	h2_1.cmd("sed 'n; d' %s > %s " %(filenamerx,outputrx))
	
	#outputtx = path+"/tx.bwm"
	#h1_1.cmd("sed 'n; d' %s > %s " %(filenametx,outputtx))


def run_path_migration_test_loss(net, bw, testdir, method):

	print "Starting path migration test - Loss"	
	
	pmigrationdir = testdir+"/pmigration_test_loss"
	path = os.getcwd()+"/"+pmigrationdir
	
	if(not(os.path.exists(path))):
		os.mkdir(path)

	outputfolder = "%s_bw%s" %(method, bw)
	path = path + "/"+outputfolder		
	
	if(os.path.exists(path)):
		shutil.rmtree(path)

	os.mkdir(path)
	
	it = 3
	step = int(bw*1000/10)
	#limit = 9*step
	limit = 3*step
	for btraffic in range (step, limit, step):
	
		itdir = path+"/"+str(btraffic)	
		
		if(os.path.exists(itdir)):
			shutil.rmtree(itdir)

		os.mkdir(itdir)		
	
		for i in range(1,it+1):
			run_path_migration_test_loss_it(net, itdir, method, i, btraffic)
		
	

def run_path_migration_test_loss_it(net, path, method, i, btraffic):

	print "Iteration %d of traffic %d Kbps" %(i,btraffic)	

	#Source of UDP traffic
	h1_1 = net.get('h1_1')
	#Destination of UDP traffic
	h2_1 = net.get('h2_1')	
	#Edge switch
	e1_1 = net.get('e1_1')
	#Spine switches
	s1 = net.get('s1')
	s2 = net.get('s2')

	#Start servers
	h2_1.cmd('iperf -s -u -l 1200 > /dev/null &')
	
	## Start the bandwidth monitor in the background for destination interface
	filenamerx = path+"/rx.bwm"
	h2_1.cmd("bwm-ng -t 1000 -I eth0 -o csv -u bytes -T rate -C ',' > %s &" %filenamerx)
	
	filenametx = path+"/tx.bwm"
	h1_1.cmd("bwm-ng -t 1000 -I eth0 -o csv -u bytes -T rate -C ',' > %s &" %filenametx)
		
	filenames1 = path+"/s1-eth1.bwm"
	s1.cmd("bwm-ng -t 1000 -I s1-eth1 -o csv -u bytes -T rate -C ',' > %s &" %filenames1)

	filenames2 = path+"/s2-eth1.bwm"
	s2.cmd("bwm-ng -t 1000 -I s2-eth1 -o csv -u bytes -T rate -C ',' > %s &" %filenames2)	
		
	result = h1_1.cmd("netstat -s")
	print result
		
	sleep(10)
		
	#Start UDP flow
	h1_1.cmd('iperf -c 10.0.2.1 -u -b %sk -l 1200 -t 75 > /dev/null &' % (str(btraffic)))
	
	sleep(30)

	#https://github.com/p4lang/behavioral-model
	#table_set_default <table name> <action name> <action parameters>
	#table_add <table name> <action name> <match fields> => <action parameters> [priority]
	#table_delete <table name> <entry handle>
	#https://github.com/p4lang/PI/blob/master/CLI/table_add.c
	#"table_add <table name> <match fields> [priority] => ""[<action name> <action parameters> | <indirect handle>]";
	#https://github.com/p4lang/p4factory/blob/master/cli/pd_cli.py

	#https://github.com/p4lang/behavioral-model/blob/master/tools/runtime_CLI.py#L1103
	#"Add entry to a match table: table_modify <table name> <action name> <entry handle> [action parameters]"
	
	#Migration
	#result = e1_1.command('table_delete tunnel_encap_process_sr 1')
	#print result
	if (method == "sourcey"):
		cmd = 'table_modify tunnel_encap_process_sr add_header_3hops 1 => 1 1 00:00:00:00:02:01 0 2 0 2 1 3'
		#cmd = 'table_add tunnel_encap_process_sr add_header_3hops 10.0.2.1/32 => 1 1 00:00:00:00:02:01 0 2 0 2 1 3'
	else:
		cmd = 'table_modify tunnel_encap_process_sr add_sourcerouting_header 1 => 1 1 00:00:00:00:02:01 179902035595884'
		#cmd = 'table_add tunnel_encap_process_sr add_sourcerouting_header 10.0.2.1/32 => 1 1 00:00:00:00:02:01 179902035595884'
	result = e1_1.command(cmd)
	#print result
	
	sleep(50)
	
	result = h1_1.cmd("netstat -s")
	print result
		
	os.system("killall -9 iperf")
	sleep(10)
	os.system("killall -9 bwm-ng")
	
	#Return original rules for next iteration
	if (method == "sourcey"):
		cmd = 'table_modify tunnel_encap_process_sr add_header_3hops 1 => 1 1 00:00:00:00:02:01 0 1 0 2 1 3'
	else:
		cmd = 'table_modify tunnel_encap_process_sr add_sourcerouting_header 1 => 1 1 00:00:00:00:02:01 71955628459531'
	result = e1_1.command(cmd)
	
	#https://stackoverflow.com/questions/21309020/remove-odd-or-even-lines-from-a-text-file
	#keep odd lines: sed 'n; d' infile > outfile
	#keep even lines: sed '1d; n; d' infile > outfile
	#Remove total lines
	outputrx = path+"/a_"+str(i)+"_rx.bwm"
	h2_1.cmd("sed 'n; d' %s > %s " %(filenamerx,outputrx))
	
	outputtx = path+"/a_"+str(i)+"_tx.bwm"
	h1_1.cmd("sed 'n; d' %s > %s " %(filenametx,outputtx))
	
	outputs1 = path+"/a_"+str(i)+"_s1-eth1.bwm"
	s1.cmd("sed 'n; d' %s > %s " %(filenames1,outputs1))
	outputs2 = path+"/a_"+str(i)+"_s2-eth1.bwm"
	s2.cmd("sed 'n; d' %s > %s " %(filenames2,outputs2))	


def main():
	lg.setLogLevel('info')  
	
	if len(sys.argv) > 1:
		method = sys.argv[1]
	else:
		method = "method"

	nspine=2
	nleaf=4
	nports=4
	
	print "Setting-up a %d spine %d leaf %d port two-tier topology" % (nspine, nleaf, nports)
		
	testdir="test" # output directory

	bw=10
	
	net = config_network(bw, method, nspine, nleaf, nports)

	os.system("killall -9 iperf")
	os.system("killall -9 ping")
	os.system("killall -9 bwm-ng")

	start = time()
	print "Starting experiment"
		
	#run_path_migration_test_tcp(net, bw, testdir, method)
	#sleep(60)
	
	#run_path_migration_test_loss(net, bw, testdir, method)
	#sleep(60)		
		
	print('Please wait until the experiment is complete...')    
		
	CLI(net)
	net.stop()
	end = time()
	print("Experiment took %.3f seconds" % (end - start))


if __name__ == '__main__':
    main()
