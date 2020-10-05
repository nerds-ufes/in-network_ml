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

import shlex
import sys
import os, shutil


class LinearTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        # linkopts = dict(bw=1, cls=TCLink)
        linkopts = dict()

        h1 = self.addHost("h1", ip="10.0.1.1")
        h2 = self.addHost("h2", ip="10.0.2.2")


        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")


        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s1)
        self.addLink(h2, s1)


def config_network():

    program = "simple_int.p4"

    topo = LinearTopo()
    link = custom(TCLink, bw=10)
    net = P4Mininet(program=program, topo=topo, link=link)
    net.start()

    print "Switch: Configuration"

    for i in range(1, 3):

        sw = net.get("s%d" % i)
        fname = "cfg/" + "s%d" % i + "-commands.txt"
        print("Configuring switch: " + "s%d" % i)
        print("Config filename: " + fname)
        with open(fname, "r") as file:
            cmd = file.read()

        # sw.command('table_add ipv4_lpm set_nhop 10.0.0.10/32 => 10.0.0.10 1')
        # sw.command('set_crc16_parameters calc 0x002d 0x0 0x0 false false')
        sw.command(cmd)


    return net



def main():
    lg.setLogLevel("info")

    print "Setting-up a 1-switch linear topology"

    net = config_network()

    print "Starting experiment"
    h1 = net.get("h1")

    #print h1.cmd( 'python3 send.py -f pcap/amostra27.pcap' ) 
    
    #print ("Please wait until the experiment is complete...")
    
    CLI(net)
    net.stop()


if __name__ == "__main__":
    main()
