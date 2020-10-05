from p4app import P4Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys

if len(sys.argv) > 1:
    N = int(sys.argv[1])
else:
    N = 10

print("Setting-up a %d-switch fabric topology" % N)


class FabricTopo(Topo):
    def __init__(self, n, **opts):
        Topo.__init__(self, **opts)

        switches = []

        for i in xrange(1, N + 1):
            ip = "10.0.%d.%d" % (i, i)
            mac = "00:00:00:00:%02x:%02x" % (i, i)
            host = self.addHost("h%d" % i, ip=ip, mac=mac)
            switch = self.addSwitch("s%d" % i)
            self.addLink(host, switch)
            switches.append(switch)
            if i == 1:
                ip = "10.0.1.11"
                mac = "00:00:00:00:01:0b"
                host = self.addHost("h11", ip=ip, mac=mac)
                self.addLink(host, switch)

                # Connection between core switches
        lastSwitch = None
        for i in xrange(0, N):
            switch = switches[i]
            if lastSwitch:
                self.addLink(lastSwitch, switch)
            lastSwitch = switch


if __name__ == "__main__":
    setLogLevel("info")

    topo = FabricTopo(N)
    # net = P4Mininet(program='polka.p4', topo=topo, enable_debugger=True)
    net = P4Mininet(program="polka.p4", topo=topo)
    net.start()

    print("Switch: Configuration")

    for i in range(1, N + 1):
        sw = net.get("s%d" % i)
        fname = "cfg/" + "s%d" % i + "-commands.txt"
        print("Configuring switch: " + "s%d" % i)
        print("Config filename: " + fname)
        with open(fname, "r") as file:
            cmd = file.read()

        # sw.command('table_add ipv4_lpm set_nhop 10.0.0.10/32 => 10.0.0.10 1')
        # sw.command('set_crc16_parameters calc 0x002d 0x0 0x0 false false')
        sw.command(cmd)

    print("h1 ping h10")
    h1 = net.get("h1")
    result = h1.cmd("ping -c10 10.0.10.10")
    print(result)

    CLI(net)
    net.stop()
    print("OK")
