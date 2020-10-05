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
    def __init__(self, n, **opts):
        Topo.__init__(self, **opts)

        # linkopts = dict(bw=1, cls=TCLink)
        linkopts = dict()
        switch = self.addSwitch("s1")

        for i in xrange(1, n + 1):
            ip = "10.0.0.%d" % (i)
            mac = "00:00:00:00:%02x:%02x" % (i, i)
            host = self.addHost("h%d" % i, ip=ip, mac=mac)
            self.addLink(host, switch, **linkopts)



def config_network():

    program = "simple.p4"

    topo = LinearTopo(2)
    link = custom(TCLink, bw=10)
    net = P4Mininet(program=program, topo=topo, link=link)
    net.start()

    print "Switch: Configuration"
    sw = net.get("s1")

    print "Configuring switch: " + "s1"
    sw.command("table_set_default ipv4_lpm tdrop")
    sw.command("table_add ipv4_lpm ipv4_forward 10.0.0.2/32 => 00:00:00:00:02:02 2")
    sw.command("table_add ipv4_lpm ipv4_forward 10.0.0.1/32 => 00:00:00:00:01:01 1")

    return net



def main():
    lg.setLogLevel("info")

    print "Setting-up a 1-switch linear topology"

    net = config_network()

    print "Starting experiment"
    h1 = net.get("h1")
    h2 = net.get("h2")

    print h1.cmd( 'ping -c1', h2.IP() ) 

    print ("Please wait until the experiment is complete...")

    net.stop()


if __name__ == "__main__":
    main()
