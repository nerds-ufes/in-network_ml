from p4app import P4Mininet, P4Program
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel  
import sys

if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = 10

print "Setting-up a %d-switch fabric topology" % N

core_prog = P4Program('core.p4')
edge_prog = P4Program('edge.p4')


class FabricTopo(Topo):
    def __init__(self, n, **opts):
        Topo.__init__(self, **opts)

        switches = []

        for i in xrange(1, N+1):
			ip = "10.0.%d.%d" %( i,  i)
			mac = '00:00:00:00:%02x:%02x' %( i,  i)
			host = self.addHost('h%d' % i, ip = ip, mac = mac)
			edge = self.addSwitch('e%d' % i, program=edge_prog)		
			switch = self.addSwitch('s%d' % i, program=core_prog) 
			self.addLink(host, edge)
			self.addLink(edge, switch)
			
			if (i==1):
				#Add host for 0 hop
				ip = "10.0.1.11" 
				mac = '00:00:00:00:01:0b'
				host = self.addHost('h11', ip = ip, mac = mac)
				self.addLink(host, edge)
							
			switches.append(switch)

        # Connection between core switches
        lastSwitch = None
        for i in xrange(0,N):
			switch = switches[i]
			
			#if (i==0):
				#switch0 = self.addSwitch('s0', program=core_prog)
				#self.addLink( switches[0], switch0)
			
			if lastSwitch:
				self.addLink( lastSwitch, switch)
			lastSwitch = switch		


if __name__ == '__main__':                                                                             
	setLogLevel( 'info' )  

	topo = FabricTopo(N)
	net = P4Mininet(program='core.p4', topo=topo)
	net.start()

	print 'Switches Configuration'

	for i in range(1, N+1):
		sw = net.get('s%d'% i)	
		ed = net.get('e%d'% i)	
		fname = 'cfg/'+'s%d'% i+'-commands.txt'
		print 'Configuring switch: '+'s%d'% i
		print 'Config filename: '+fname
		with open(fname, 'r') as file:
			cmd = file.read()
		sw.command(cmd)
		
		fname = 'cfg/'+'e%d'% i+'-commands.txt'
		print 'Configuring edge: '+'e%d'% i
		print 'Config filename: '+fname
		with open(fname, 'r') as file:
			cmd = file.read()
		ed.command(cmd)
		
	print "h1 ping h10"	
	h1 = net.get('h1')
	result = h1.cmd('ping -c10 10.0.10.10')
	print result

	CLI(net)
	net.stop()  
	print "OK"


