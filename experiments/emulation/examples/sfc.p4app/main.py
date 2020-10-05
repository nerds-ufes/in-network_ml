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



class FabricTopo(Topo):
    def __init__(self, n, core_file, edge_file, **opts):
        Topo.__init__(self, **opts)

        switches = []
        core_prog = P4Program(core_file)
        edge_prog = P4Program(edge_file)        

        for i in xrange(1, n+1):
			# Instantiate hosts
			ip = "10.0.%d.%d" %( i,  i)
			mac = '00:00:00:00:%02x:%02x' %( i,  i)
			host = self.addHost('h%d' % i, ip = ip, mac = mac)
			# Instantiate vnfs
			ip = "10.0.%d.%d" %( i,  i+1)
			mac = '00:00:00:00:%02x:%02x' %( i,  i+1)
			vnf = self.addHost("vnf%s" % str(i), ip = ip, mac = mac)
			# Instantiate switches and links
			edge = self.addSwitch('e%d' % i, program=edge_prog)		
			switch = self.addSwitch('s%d' % i, program=core_prog) 
			self.addLink(host, edge)			
			self.addLink(vnf, edge)	
			self.addLink(edge, switch)
			switches.append(switch)
	 
        # Connection between core switches
        lastSwitch = None
        for i in xrange(0,n):
			switch = switches[i]			
			if lastSwitch:
				self.addLink( lastSwitch, switch)
			lastSwitch = switch		
							

def config_network(bw, method, n, cfgdir):
		
	core_file = method+"-core.p4"
	edge_file = method+"-edge.p4"
	
	topo = FabricTopo(n, core_file, edge_file)
	link = custom(TCLink, bw=bw)
	net = P4Mininet(program=core_file, topo=topo, link=link)
	net.start()

	print 'Switches Configuration'

	for i in range(1, n+1):
		sw = net.get('s%d'% i)	
		ed = net.get('e%d'% i)	
		fname = cfgdir+'/'+method+'-fabric/s%d'% i+'-commands.txt'
		print 'Configuring switch: '+'s%d'% i
		print 'Config filename: '+fname
		with open(fname, 'r') as file:
			cmd = file.read()
		sw.command(cmd)
		
		fname = cfgdir+'/'+method+'-fabric/e%d'% i+'-commands.txt'
		print 'Configuring edge: '+'e%d'% i
		print 'Config filename: '+fname
		with open(fname, 'r') as file:
			cmd = file.read()
		ed.command(cmd)
				
	return net


def start_vnfs(net):
		
	#start L2 forwarding SF at all VNFs
	for vnf in net.hosts:
		vnfname = vnf.name
		if(vnfname.startswith('vnf')):
			print ('Starting VNF %s on IP %s:' %(vnf.name, vnf.IP()))
			vnf.cmd("chmod +x scripts/forward.py")
			result = vnf.cmd('./scripts/forward.py &')
			print result  


def test_sfc_conectivity(net):
	
	print "Starting conectivity test"

	# h1 ping all
	h1 = net.get('h1')		
	for client in net.hosts:
		if(client.name.startswith('h')):
			result = h1.cmd('ping -c 1 %s' % client.IP())
			print result  


def run_latency_test(net, bw, testdir, method, testnumber):
	
	latencydir = testdir+"/latency_test_"+str(testnumber)
	path = os.getcwd()+"/"+latencydir
	
	if(not(os.path.exists(path))):
		os.mkdir(path)

	outputfolder = "%s_bw%s" %(method, bw)
	path = path + "/"+outputfolder		
	
	if(os.path.exists(path)):
		shutil.rmtree(path)

	os.mkdir(path)
	
	scriptdir = "scripts"
	scriptname = "gen_latency_"+str(testnumber)+".sh"
	shutil.copyfile(scriptdir+"/"+scriptname, path+"/"+scriptname)
			
	h1 = net.get('h1')

	command = "cd /p4app/"+latencydir+"/"+outputfolder
	print command
	result = h1.cmd(command)
	print result
	result = h1.cmd("chmod +x "+scriptname)
	print result
	result = h1.cmd("./"+scriptname)
	print result

	os.system("killall -9 ping")


def run_fct_test(net, bw, testdir, method, testnumber):
	
	fctdir = testdir+"/fct_test_"+str(testnumber)
	path = os.getcwd()+"/"+fctdir
	
	if(not(os.path.exists(path))):
		os.mkdir(path)

	outputfolder = "%s_bw%s" %(method, bw)
	path = path + "/"+outputfolder		
	
	if(os.path.exists(path)):
		shutil.rmtree(path)

	os.mkdir(path)
	
	scriptdir = "scripts"
	scriptname = "gen_fct_"+str(testnumber)+".sh"
	shutil.copyfile(scriptdir+"/"+scriptname, path+"/"+scriptname)
			
	h1 = net.get('h1')
	
	for h in net.hosts:
		if (h != h1 and h.name.startswith('h')):
			h.cmd("iperf -s -M 1200 > /dev/null &")	
	
	command = "cd /p4app/"+fctdir+"/"+outputfolder
	print command
	result = h1.cmd(command)
	print result
	result = h1.cmd("chmod +x "+scriptname)
	print result
	result = h1.cmd("./"+scriptname)
	print result

	os.system("killall -9 iperf")


def run_jitter_test(net, bw, testdir, method, testnumber):
	
	print "Starting jitter test"
	
	jitterdir = testdir+"/jitter_test_"+str(testnumber)
	path = os.getcwd()+"/"+jitterdir
	
	if(not(os.path.exists(path))):
		os.mkdir(path)

	outputfolder = "%s_bw%s" %(method, bw)
	path = path + "/"+outputfolder		
	
	if(os.path.exists(path)):
		shutil.rmtree(path)

	os.mkdir(path)
			
	h1 = net.get('h1')

	#Generate traffic that is half of the link capacity
	btraffic = bw*1000/2
	
	
	steps=1	
	duration = 70
	
	if(testnumber==1):
	
		i=0	
	
		for server in net.hosts:
			if (server != h1 and server.name.startswith('h')):
				logdir = path+"/"+str(i)
				os.mkdir(logdir)
				command = "cd /p4app/"+jitterdir+ "/"+outputfolder+"/"+str(i)
				server.cmd(command)
				server.cmd("iperf -s -u -l 1200 -yc -i 1 1>jitter.log &")
				for it in range(0,steps):
					print "Server: "+server.IP()
					h1.cmd('iperf -c %s -N -u -b %sk -l 1200 -t %s -i 1 &>/dev/null' % (server.IP(), str(btraffic), duration))   
					sleep(10)
				server.cmd("killall iperf 2>/dev/null")
				server.cmd("head -n -1 jitter.log")
				server.cmd("cat jitter.log | cut -d ',' -f 10 >> a1_"+str(i))	
				i = i+1
				server.cmd("cd ..")	
	
	

	if(testnumber==2):
		
		for i in range(1,5):
			#Servers:h3, h5, h7, h9
			server = net.get('h'+str(2*i+1))

			logdir = path+"/"+str(i)
			os.mkdir(logdir)
			command = "cd /p4app/"+jitterdir+ "/"+outputfolder+"/"+str(i)
			server.cmd(command)
			server.cmd("iperf -s -u -l 1200 -yc -i 1 1>jitter.log &")
			for it in range(0,steps):
				print "Server: "+server.IP()
				h1.cmd('iperf -c %s -N -u -b %sk -l 1200 -t %s -i 1 &>/dev/null' % (server.IP(), str(btraffic), duration))   
				sleep(10)
			server.cmd("killall iperf 2>/dev/null")
			server.cmd("head -n -1 jitter.log")
			server.cmd("cat jitter.log | cut -d ',' -f 10 >> a1_"+str(i))	
			server.cmd("cd ..")	
	

	os.system("killall -9 iperf")



def main():
	lg.setLogLevel('info')  
	
	if len(sys.argv) > 3:
		method = sys.argv[1]
		is_fabric = int(sys.argv[2])
		n = int(sys.argv[3])
	else:
		method = "method"
		is_fabric = 0    
		n = 10
	
	print "Setting-up a %d-switch linear topology" % n
		
	testdir="test" # output directory

	bw=1
	#testnumber=1
	testnumber=2
	cfgdir='cfg'+str(testnumber)
	net = config_network(bw, method, n, cfgdir)
	
	method = method+"-fabric"	
	
	start_vnfs(net)
	sleep(10)
	
	test_sfc_conectivity(net)	
	sleep(10)

	os.system("killall -9 iperf")
	os.system("killall -9 ping")

	start = time()
	print "Starting experiment"

	run_latency_test(net, bw, testdir, method, testnumber)
	sleep(60)
	run_jitter_test(net, bw, testdir, method, testnumber)
	sleep(60)	
	run_fct_test(net, bw, testdir, method, testnumber)	
	sleep(60)

	print('Please wait until the experiment is complete...')    

	#CLI(net)
	#net.stop()
	end = time()
	print("Experiment took %.3f seconds" % (end - start))


if __name__ == '__main__':
    main()
