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


class LinearTopo(Topo):
    def __init__(self, n, **opts):
        Topo.__init__(self, **opts)

        # linkopts = dict(bw=1, cls=TCLink)
        linkopts = dict()

        switches = []

        for i in xrange(1, n + 1):
            ip = "10.0.%d.%d" % (i, i)
            mac = "00:00:00:00:%02x:%02x" % (i, i)
            host = self.addHost("h%d" % i, ip=ip, mac=mac)
            switch = self.addSwitch("s%d" % i)
            self.addLink(host, switch, **linkopts)
            switches.append(switch)
            if i == 1:
                ip = "10.0.1.11"
                mac = "00:00:00:00:01:0b"
                host = self.addHost("h11", ip=ip, mac=mac)
                self.addLink(host, switch, **linkopts)

                # Connection between core switches
        lastSwitch = None
        for i in xrange(0, n):
            switch = switches[i]
            if lastSwitch:
                self.addLink(lastSwitch, switch, **linkopts)
            lastSwitch = switch


class FabricTopo(Topo):
    def __init__(self, n, core_file, edge_file, **opts):
        Topo.__init__(self, **opts)

        switches = []
        core_prog = P4Program(core_file)
        edge_prog = P4Program(edge_file)

        for i in xrange(1, n + 1):
            ip = "10.0.%d.%d" % (i, i)
            mac = "00:00:00:00:%02x:%02x" % (i, i)
            host = self.addHost("h%d" % i, ip=ip, mac=mac)
            edge = self.addSwitch("e%d" % i, program=edge_prog)
            switch = self.addSwitch("s%d" % i, program=core_prog)
            self.addLink(host, edge)
            self.addLink(edge, switch)

            if i == 1:
                # Add host for 0 hop
                ip = "10.0.1.11"
                mac = "00:00:00:00:01:0b"
                host = self.addHost("h11", ip=ip, mac=mac)
                self.addLink(host, edge)

            switches.append(switch)

            # Connection between core switches
        lastSwitch = None
        for i in xrange(0, n):
            switch = switches[i]

            # if (i==0):
            # switch0 = self.addSwitch('s0', program=core_prog)
            # self.addLink( switches[0], switch0)

            if lastSwitch:
                self.addLink(lastSwitch, switch)
            lastSwitch = switch


def config_network(bw, method, n, is_fabric):

    if is_fabric:

        core_file = method + "-core.p4"
        edge_file = method + "-edge.p4"

        topo = FabricTopo(n, core_file, edge_file)
        link = custom(TCLink, bw=bw)
        net = P4Mininet(program=core_file, topo=topo, link=link)
        net.start()

        print "Switches Configuration"

        for i in range(1, n + 1):
            sw = net.get("s%d" % i)
            ed = net.get("e%d" % i)
            fname = "cfg/" + method + "-fabric/s%d" % i + "-commands.txt"
            print "Configuring switch: " + "s%d" % i
            print "Config filename: " + fname
            with open(fname, "r") as file:
                cmd = file.read()
            sw.command(cmd)

            fname = "cfg/" + method + "-fabric/e%d" % i + "-commands.txt"
            print "Configuring edge: " + "e%d" % i
            print "Config filename: " + fname
            with open(fname, "r") as file:
                cmd = file.read()
            ed.command(cmd)

    else:
        program = method + ".p4"

        topo = LinearTopo(n)
        link = custom(TCLink, bw=bw)
        # net = P4Mininet(program='polka.p4', topo=topo, host=CPULimitedHost, link=TCLink, enable_debugger=True)
        net = P4Mininet(program=program, topo=topo, link=link)
        net.start()

        print "Switch: Configuration"

        for i in range(1, n + 1):
            sw = net.get("s%d" % i)
            fname = "cfg/" + method + "/s%d" % i + "-commands.txt"
            print "Configuring switch: " + "s%d" % i
            print "Config filename: " + fname
            with open(fname, "r") as file:
                cmd = file.read()
            sw.command(cmd)

    return net


def run_iperf_test(net, bw, directoryName, method):

    os.chdir(directoryName)
    path = os.getcwd() + "/iperf_test"

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)
    os.chdir(path)

    # Start iperf test
    fileName = method + "_iperf"  # output filename
    steps = 3
    dataSize = 1000000
    port = 5001

    h1 = net.get("h1")
    for h in net.hosts:
        if h != h1:
            h.cmd("iperf -s -p %s -M 1200 > /dev/null &" % port)

    for server in net.hosts:
        if server != h1:
            # print ("The current working directory is %s" % os.getcwd())
            outputFile = "%s_%s_bw%s_%sb.txt" % (
                fileName,
                server.name,
                bw,
                dataSize,
            )
            print "Output filename: " + outputFile
            for i in range(0, steps):
                # http://www.jb.man.ac.uk/~jcullen/code/python/iperf_tests.py
                # timestamp,source_address,source_port,destination_address,destination_port,interval,transferred_bytes,bits_per_second
                h1.cmd(
                    "iperf -c %s -M 1200 -p %s -n %d -yc 2> /dev/null >>%s/%s"
                    % (server.IP(), port, dataSize, path, outputFile)
                )
                sleep(10)

    # cat test.txt | cut -d ',' -f 7 | cut -d '-' -f 2 > output.txt

    os.system("killall -9 iperf")


def run_latency_test(net, bw, testdir, method):

    print "Starting latency test"

    latencydir = testdir + "/latency_test"
    path = os.getcwd() + "/" + latencydir

    if not (os.path.exists(path)):
        os.mkdir(path)

    outputfolder = "%s_bw%s" % (method, bw)
    path = path + "/" + outputfolder

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    scriptdir = "scripts"
    shutil.copyfile(scriptdir + "/gen_latency.sh", path + "/gen_latency.sh")

    h1 = net.get("h1")

    command = "cd /p4app/" + latencydir + "/" + outputfolder
    print command
    result = h1.cmd(command)
    print result
    result = h1.cmd("chmod +x gen_latency.sh")
    print result
    result = h1.cmd("./gen_latency.sh")
    print result

    os.system("killall -9 ping")


def run_latency_test_bigpacket(net, bw, testdir, method):

    print "Starting latency test"

    latencydir = testdir + "/latency_test_bigpacket"
    path = os.getcwd() + "/" + latencydir

    if not (os.path.exists(path)):
        os.mkdir(path)

    outputfolder = "%s_bw%s" % (method, bw)
    path = path + "/" + outputfolder

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    scriptdir = "scripts"
    shutil.copyfile(
        scriptdir + "/gen_latency_bigpacket.sh",
        path + "/gen_latency_bigpacket.sh",
    )

    h1 = net.get("h1")

    command = "cd /p4app/" + latencydir + "/" + outputfolder
    print command
    result = h1.cmd(command)
    print result
    result = h1.cmd("chmod +x gen_latency_bigpacket.sh")
    print result
    result = h1.cmd("./gen_latency_bigpacket.sh")
    print result

    os.system("killall -9 ping")


def run_latency_test_background_traffic(net, bw, testdir, method):

    print "Starting latency test with background traffic"

    latencydir = testdir + "/latency_test_btraffic"
    path = os.getcwd() + "/" + latencydir

    if not (os.path.exists(path)):
        os.mkdir(path)

    outputfolder = "%s_bw%s" % (method, bw)
    path = path + "/" + outputfolder

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    scriptdir = "scripts"
    shutil.copyfile(
        scriptdir + "/gen_latency_btraffic.sh",
        path + "/gen_latency_btraffic.sh",
    )

    h1 = net.get("h1")

    command = "cd /p4app/" + latencydir + "/" + outputfolder
    print command
    result = h1.cmd(command)
    print result
    result = h1.cmd("chmod +x gen_latency_btraffic.sh")
    print result

    # Start servers for background traffic
    for server in net.hosts:
        if server != h1:
            server.cmd("iperf -s -u -l 1200 &")

    result = h1.cmd("./gen_latency_btraffic.sh")
    print result

    os.system("killall -9 ping")
    os.system("killall -9 iperf")


def run_fct_test(net, bw, testdir, method):

    print "Starting fct test"

    fctdir = testdir + "/fct_test"
    path = os.getcwd() + "/" + fctdir

    if not (os.path.exists(path)):
        os.mkdir(path)

    outputfolder = "%s_bw%s" % (method, bw)
    path = path + "/" + outputfolder

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    scriptdir = "scripts"
    shutil.copyfile(scriptdir + "/gen_fct.sh", path + "/gen_fct.sh")

    h1 = net.get("h1")

    for h in net.hosts:
        if h != h1:
            h.cmd("iperf -s -M 1200 > /dev/null &")

    command = "cd /p4app/" + fctdir + "/" + outputfolder
    print command
    result = h1.cmd(command)
    print result
    result = h1.cmd("chmod +x gen_fct.sh")
    print result
    result = h1.cmd("./gen_fct.sh")
    print result

    os.system("killall -9 iperf")


def run_jitter_test(net, bw, testdir, method):

    print "Starting jitter test"

    jitterdir = testdir + "/jitter_test"
    path = os.getcwd() + "/" + jitterdir

    if not (os.path.exists(path)):
        os.mkdir(path)

    outputfolder = "%s_bw%s" % (method, bw)
    path = path + "/" + outputfolder

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    h1 = net.get("h1")
    h11 = net.get("h11")

    # Generate background traffic that is half of link capacity
    btraffic = bw * 1000 / 2

    i = 1
    steps = 1
    duration = 70
    for server in net.hosts:
        if server == h11:
            i = 0
        if server != h1:
            logdir = path + "/" + str(i)
            os.mkdir(logdir)
            command = (
                "cd /p4app/" + jitterdir + "/" + outputfolder + "/" + str(i)
            )
            server.cmd(command)
            server.cmd("iperf -s -u -l 1200 -yc -i 1 1>jitter.log &")
            for it in range(0, steps):
                h1.cmd(
                    "iperf -c %s -N -u -b %sk -l 1200 -t %s -i 1 &>/dev/null"
                    % (server.IP(), str(btraffic), duration)
                )
                sleep(10)
            server.cmd("killall iperf 2>/dev/null")
            server.cmd("head -n -1 jitter.log")
            server.cmd("cat jitter.log | cut -d ',' -f 10 >> a1_" + str(i))
            i = i + 1
            server.cmd("cd ..")

    os.system("killall -9 iperf")


def test_conectivity(net):
    # h1 ping all
    h1 = net.get("h1")
    for client in net.hosts:
        result = h1.cmd("ping -c 1 %s" % client.IP())
        print result


def main():
    lg.setLogLevel("info")

    if len(sys.argv) > 3:
        method = sys.argv[1]
        is_fabric = int(sys.argv[2])
        n = int(sys.argv[3])
    else:
        method = "method"
        is_fabric = 0
        n = 10

    print "Setting-up a %d-switch linear topology" % n

    testdir = "test"  # output directory

    bw = 10

    net = config_network(bw, method, n, is_fabric)

    if is_fabric:
        method = method + "-fabric"

    test_conectivity(net)
    sleep(10)

    os.system("killall -9 iperf")
    os.system("killall -9 ping")

    start = time()
    print "Starting experiment"

    ## Start the bandwidth monitor in the background
    # monitor = Process(target=monitor_devs_ng, args=('%s/%s.bwm' % (testdir,filename), 1.0))
    # monitor.start()

    ## Start the CPU monitor in the background
    # monitor1 = Process(target=monitor_cpu, args=('%s/%s.cpu' % (testdir,filename), ))
    # monitor1.start()

    print ("Please wait until the experiment is complete...")

    run_latency_test(net, bw, testdir, method)
    sleep(60)
    # run_fct_test(net, bw, testdir, method)
    # sleep(60)
    run_jitter_test(net, bw, testdir, method)
    sleep(60)
    run_latency_test_background_traffic(net, bw, testdir, method)
    sleep(60)
    run_latency_test_bigpacket(net, bw, testdir, method)
    sleep(60)

    # os.system("killall -9 bwm-ng")
    # os.system("killall -9 sar")
    # monitor1.terminate()
    # monitor.terminate()
    # CLI(net)
    net.stop()
    end = time()
    print ("Experiment took %.3f seconds" % (end - start))


if __name__ == "__main__":
    main()
