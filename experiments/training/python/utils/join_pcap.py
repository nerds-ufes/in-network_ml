from scapy.all import *


print ("Loading PCAP")

w_cap = PcapWriter("../pcap/wed.100000.pcap")
rb_cap = PcapReader("../pcap/wedB.pcap")
rdh_cap = PcapReader("../pcap/wed_dh.pcap")
rdge_cap = PcapReader("../pcap/wed_dge.pcap")
rdsh_cap = PcapReader("../pcap/wed_dsh.pcap")
rdsl_cap = PcapReader("../pcap/wed_dsl.pcap")
rh_cap = PcapReader("../pcap/wed_dh.pcap")
print ("PCAP loaded")

def count(f, qt, label):
    c = 0
    for packet in f:

        if not packet.haslayer(IP):   
            continue
        
        if c == qt:
            break

        w_cap.write(packet)

        c +=1
        if c % 1000 == 0:
            print ('{}-packets {}'.format(label, c))


count(rdsl_cap, 290, 'dos_slowloris')
count(rdsh_cap, 190, 'dos_slowhttptest')
count(rdh_cap, 6259, 'dos_hulk')
count(rdge_cap, 373, 'dos_goldeneye')
count(rh_cap, 90, 'Heartblend')

count(rb_cap, 482116, 'benign')
