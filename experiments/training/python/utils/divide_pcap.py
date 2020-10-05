from scapy.all import *
from datetime import datetime
import argparse

def wef():
    print ("Loading PCAP WED")

    r_cap = PcapReader("../pcap/wed.pcap")
    wb_cap = PcapWriter("../pcap/wedB.pcap")
    wdsl_cap = PcapWriter("../pcap/wed_dsl.pcap")
    wdsh_cap = PcapWriter("../pcap/wed_dsh.pcap")
    wdh_cap = PcapWriter("../pcap/wed_dh.pcap")
    wdge_cap = PcapWriter("../pcap/wed_dge.pcap")
    wh_cap = PcapWriter("../pcap/wedh.pcap")
    print ("PCAP loaded")

    ipAttack = ['172.16.0.1']
    vitDos = ['192.168.10.50']
    vitHeartbleed = ['192.168.10.51']

    count = 0
    list = 6*[0]
    sys.stdout = open("test.txt", "w")
    for packet in r_cap:

        if not packet.haslayer(IP):   
            continue

        if (packet[IP].src in ipAttack and packet[IP].dst in vitDos) or (packet[IP].src in ipAttack and packet[IP].dst in vitHeartbleed):
            tt = datetime.fromtimestamp(packet.time)

            #print('{} /// {}  <=  {}   <=   {} ==  {}'.format(packet[IP].dst, tt, datetime.fromisoformat('2017-07-05T09:47:00'), datetime.fromisoformat('2017-07-05T15:32:59'), (tt >= datetime.fromisoformat('2017-07-05T10:43:00') and tt >= datetime.fromisoformat('2017-07-05T11:00:59'))))
            if (packet[IP].dst in vitDos) and (datetime.fromisoformat('2017-07-05T09:47:00') <= tt  and tt <= datetime.fromisoformat('2017-07-05T10:10:59')):
                wdsl_cap.write(packet)
                list[0] += 1
            elif (packet[IP].dst in vitDos) and (datetime.fromisoformat('2017-07-05T10:14:00') <= tt  and tt <= datetime.fromisoformat('2017-07-05T10:35:59')):
                wdsh_cap.write(packet)
                list[1] += 1
            elif (packet[IP].dst in vitDos) and (datetime.fromisoformat('2017-07-05T10:43:00') <= tt  and tt <= datetime.fromisoformat('2017-07-05T11:00:59')):
                wdh_cap.write(packet)
                list[2] += 1
            elif (packet[IP].dst in vitDos) and (datetime.fromisoformat('2017-07-05T11:10:00') <= tt and tt <= datetime.fromisoformat('2017-07-05T11:23:59')):
                wdge_cap.write(packet)
                list[3] += 1
            elif (packet[IP].dst in vitHeartbleed) and (datetime.fromisoformat('2017-07-05T15:12:00') <= tt and tt <= datetime.fromisoformat('2017-07-05T15:32:59')):
                wh_cap.write(packet)
                list[4] += 1
        else:
            wb_cap.write(packet)
            list[5] += 1
        count +=1
        if count % 20000 == 0:
            print ('packets {} {}'.format(count, list))
            sys.stdout.flush()

    sys.stdout.close()

def thu():
    print ("Loading PCAP THU")

    r_cap = PcapReader("../pcap/thu.pcap")
    wb_cap = PcapWriter("../pcap/thub.pcap")
    wabf_cap = PcapWriter("../pcap/thu_wabf.pcap")
    waxss_cap = PcapWriter("../pcap/thu_waxss.pcap")
    wasi_cap = PcapWriter("../pcap/thu_wasi.pcap")
    idb1_cap = PcapWriter("../pcap/thu_idb1.pcap")
    icd_cap = PcapWriter("../pcap/thu_icd.pcap")
    idb2_cap = PcapWriter("../pcap/thu_idb2.pcap")
    print ("PCAP loaded")

    ipAttack = ['172.16.0.1']
    vit = ['192.168.10.50', '192.168.10.8', '192.168.10.25']
    count = 0
    list = 9*[0]
    sys.stdout = open("test.txt", "w")
    for packet in r_cap:

        if not packet.haslayer(IP):   
            continue

        tt = datetime.fromtimestamp(packet.time)
        if (packet[IP].src in ipAttack and packet[IP].dst in vit):

            #print('{} /// {}  <=  {}   <=   {} ==  {}'.format(packet[IP].dst, tt, datetime.fromisoformat('2017-07-05T09:47:00'), datetime.fromisoformat('2017-07-05T15:32:59'), (tt >= datetime.fromisoformat('2017-07-05T10:43:00') and tt >= datetime.fromisoformat('2017-07-05T11:00:59'))))
            if (datetime.fromisoformat('2017-07-06T09:20:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T10:00:59')):
                wabf_cap.write(packet)
                list[0] += 1
            elif (datetime.fromisoformat('2017-07-06T10:15:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T10:35:59')):
                waxss_cap.write(packet)
                list[1] += 1
            elif (datetime.fromisoformat('2017-07-06T10:40:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T10:42:59')):
                wasi_cap.write(packet)
                list[2] += 1
            elif (datetime.fromisoformat('2017-07-06T14:19:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T14:19:59') or 
                 datetime.fromisoformat('2017-07-06T14:20:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T14:21:59') or 
                 datetime.fromisoformat('2017-07-06T14:33:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T14:35:59') ):
                idb1_cap.write(packet)
                list[3] += 1
            elif (datetime.fromisoformat('2017-07-06T14:53:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T15:00:59')):
                icd_cap.write(packet)
                list[4] += 1
            elif (datetime.fromisoformat('2017-07-06T15:04:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T15:45:59')):
                idb2_cap.write(packet)
                list[5] += 1
            else:
                wb_cap.write(packet)
                list[8] += 1           
        elif (packet[IP].src == '192.168.10.8' and datetime.fromisoformat('2017-07-06T15:04:00') <= tt  and tt <= datetime.fromisoformat('2017-07-06T15:45:59')):
            idb2_cap.write(packet)
            list[7] += 1        
        else:
            wb_cap.write(packet)
            list[6] += 1
        count +=1
        if count % 20000 == 0:
            print ('packets {} {}'.format(count, list))
            sys.stdout.flush()

    sys.stdout.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process to extract features from pcap.')
    parser.add_argument('-wed', help='Wednesday pcap file', action='store_true', default=False, dest='wed')
    parser.add_argument('-thu', help='Thursday pcap file', action='store_true', default=False, dest='thu')
    args = parser.parse_args()


    if args.wed:
        wed()
    if args.thu:
        thu()