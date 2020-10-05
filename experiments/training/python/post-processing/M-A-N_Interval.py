from decimal import Decimal
import copy

d_class = {'benign':0, 'dos_hulk': 1, 'dos_goldeneye': 2, 'dos_slowhttptest': 3, 'wa_brute_force': 4, 'dos_slowloris': 5, 'i_portscan': 6}
d_features = {'TcpDstPort':(0, 65000), 'PacketSize': (0, 1500), 'hdr.tcp.ctrl': (0, 63), 'hdr.ipv4.flags': (0,3), 'UdpDstPort': (0,65000), 'hdr.tcp.ecn': (0,3), 'EtherType': (0, 65535), 'Protocol': (0, 255)}
d_names = {'TcpDstPort':'tcp_dstPort', 'PacketSize': 'ipv4_totalLen', 'hdr.tcp.ctrl': 'tcp_ctrl', 
           'hdr.ipv4.flags': 'ipv4_flags', 'UdpDstPort': 'udp_dstPort', 'hdr.tcp.ecn': 'tcp_ecn', 'EtherType': 'ethernet_etherType', 'Protocol': 'ipv4_protocol'}


class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.condition1 = None
        self.condition2 = None
        self.condition3 = None
        self.clazz = None
        self.level = None
        self.elze = False
        self.key = ''

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

 
class MARule:
    def __init__(self):
        etherType = Rule(0, 132)
        protocol = Rule(0, 61889)
        flags = Rule(0, 61889)
        totalLen = Rule(0, 1500)
        ctrl = Rule(0, 63)
        ecn = Rule(0, 3)
        tcp_dstPort = Rule(0, 65000)
        udp_dstPort = Rule(0, 65000)
class Rule:
    def __init__(self, li, ls):
        self.feature = ''
        self.limite_inferior = li
        self.limite_superior = ls

def montaTree(line):
    t = Tree()

    l_ = line.split('class = ')
    l_ = l_[1].split('"')
    t.clazz = l_[0]
    l = line.split('\\n')
    if len(l) == 5:
        l_ = l[0].split('[label="')
        l_ = l_[1].split(' ')
        t.condition1 = l_[0]
        t.condition2 = l_[1]
        t.condition3 = int(float(l_[2]))
    else:
        t.elze = True
    l_ = l[0].split(' [')
    level = int(l_[0])
    t.level = level
    return t

def range_(d, f):
    if f in d:
        return '{}->{}'.format(d[f][0], d[f][1]), d[f][0], d[f][1]
    else:
        return '{}->{}'.format(d_features[f][0], d_features[f][1]), d_features[f][0], d_features[f][1]

a = 1
e = 1
dic = dict()
interval = dict()

def dic_feature(d, f):
    feat, ini, fim = range_(d,f)
    global e
    if f not in dic:
        dic.update({f: dict([(feat, e)])})
        interval.update({f: [ini, fim]})
        e += 1
    elif feat not in dic[f]:
        dic[f].update({feat: e})
        if ini not in interval[f]:
            interval[f].append(ini)
        if fim not in interval[f]:
            interval[f].append(fim)
        e += 1

    return dic[f][feat]
c = 0
def pre_ordem(tree, lado, obj, i):
    d = copy.deepcopy(obj)
    global a
    global c
    if not tree.condition1:
        eth = dic_feature(d, "EtherType")
        tP = dic_feature(d, "TcpDstPort")
        size = dic_feature(d, "PacketSize")
        ctrl = dic_feature(d, "hdr.tcp.ctrl")
        flag = dic_feature(d, "hdr.ipv4.flags")
        uP = dic_feature(d, "UdpDstPort")
        ecn = dic_feature(d, "hdr.tcp.ecn")
        pro = dic_feature(d, "Protocol")

        c += 1

        return d
    if tree.left:    
        pre_ordem(tree.left, 'L', d, i)
    if tree.right:
        pre_ordem(tree.right, 'R', d, i)
    
    return d

def range_pre_order(tree, lado, obj, i, feat):
    d = copy.deepcopy(obj)
    global a
    global e
    if not tree.condition1:
        return

    if tree.left:
        if tree.condition1 not in d:
            d.update({tree.condition1: [d_features[tree.condition1][0], tree.condition3]})
        else:
            d[tree.condition1][1] = tree.condition3        

        f, ini, fim = range_(d, tree.condition1)
        if tree.condition1 not in dic:
            dic.update({tree.condition1: dict([(f, e)])})
            interval.update({tree.condition1: [ini, fim]})
            e += 1
        elif f not in dic[tree.condition1]:
            dic[tree.condition1].update({f: e})
            if ini not in interval[tree.condition1]:
                interval[tree.condition1].append(ini)
            if fim not in interval[tree.condition1]:
                interval[tree.condition1].append(fim)
            e += 1

        range_pre_order(tree.left, 'L', d, i, feat)
    if tree.right:
        if tree.condition1 not in obj:
            d.update({tree.condition1: [tree.condition3+1, d_features[tree.condition1][1]]})
        else:
            d[tree.condition1][0] = d[tree.condition1][1]+1
            d[tree.condition1][1] = obj[tree.condition1][1]

        f, ini, fim = range_(d, tree.condition1)
        if tree.condition1 not in dic:
            dic.update({tree.condition1: dict([(f, e)])})
            interval.update({tree.condition1: [ini, fim]})
            e += 1
        elif f not in dic[tree.condition1]:
            dic[tree.condition1].update({f: e})
            if ini not in interval[tree.condition1]:
                interval[tree.condition1].append(ini)
            if fim not in interval[tree.condition1]:
                interval[tree.condition1].append(fim)
            e += 1
        
        range_pre_order(tree.right, 'R', d, i, feat)
    
dir = '../../results/tmp'

def print_range_rule(i, n, n_, a, rng, vl, max_match):
    print (f'       {{"name\": \"dt{i}_{n_}_rule{a}\", \n        "match\": {{ "{n}": {{"value": "{rng}"}} }},')
    print(f'        \"action\": {{\"type\": \"ingress::act_{n_}\",\"data\": {{\"clazz\": {{\"value\": \"{vl}\"}} }} }}')
    print('       },' if a < max_match else '       }')

def update_dict(dic, key, rng, a):
    if key in dic:
        dic[key].update({rng: a})
    else:
        dic.update({key: dict([(rng, a)])})

def print_main_rules(d, interval_rng, label):
    c = 0
    print('PRINT:::')
    print(d)
    print(interval_rng)
    for eth in interval_rng['EtherType']:
        _eth = range_(d, 'EtherType')  
        rng_eth = [int(n) for n in eth.split('->')]
        if not (_eth[1] <= rng_eth[0] and _eth[2] >= rng_eth[1]):
            continue
        for tcp in interval_rng['TcpDstPort']:
            _tcp = range_(d, 'TcpDstPort')  
            rng_tcp = [int(n) for n in tcp.split('->')]
            if not (_tcp[1] <= rng_tcp[0] and _tcp[2] >= rng_tcp[1]):
                continue
            for pkt in interval_rng['PacketSize']:
                _pkt = range_(d, 'PacketSize')  
                rng_pkt = [int(n) for n in pkt.split('->')]
                if not (_pkt[1] <= rng_pkt[0] and _pkt[2] >= rng_pkt[1]):
                    continue
                for ctl in interval_rng['hdr.tcp.ctrl']:
                    _ctl = range_(d, 'hdr.tcp.ctrl')  
                    rng_ctl = [int(n) for n in ctl.split('->')]
                    if not (_ctl[1] <= rng_ctl[0] and _ctl[2] >= rng_ctl[1]):
                        continue
                    for flg in interval_rng['hdr.ipv4.flags']:
                        _flg = range_(d, 'hdr.ipv4.flags')  
                        rng_flg = [int(n) for n in flg.split('->')]
                        if not (_flg[1] <= rng_flg[0] and _flg[2] >= rng_flg[1]):
                            continue
                        for udp in interval_rng['UdpDstPort']:
                            _udp = range_(d, 'UdpDstPort')  
                            rng_udp = [int(n) for n in udp.split('->')]
                            if not (_udp[1] <= rng_udp[0] and _udp[2] >= rng_udp[1]):
                                continue
                            for ecn in interval_rng['hdr.tcp.ecn']:
                                _ecn = range_(d, 'hdr.tcp.ecn')  
                                rng_ecn = [int(n) for n in ecn.split('->')]
                                if not (_ecn[1] <= rng_ecn[0] and _ecn[2] >= rng_ecn[1]):
                                    continue
                                for pro in interval_rng['Protocol']:
                                    _pro = range_(d, 'Protocol')  
                                    rng_pro = [int(n) for n in pro.split('->')]
                                    if not (_pro[1] <= rng_pro[0] and _pro[2] >= rng_pro[1]):
                                        continue
                                    print (f'EtherType: {eth} TcpDstPort: {tcp} PacketSize: {pkt} ctrl: {ctl} flg: {flg} udp: {udp} ecn: {ecn} pro: {pro}={label}')

                                    c += 1


    return c
    
def process_main_rules(tree, lado, obj, i):
    #print(tree.level)
    d = copy.deepcopy(obj)
    global a
    global c
    if not tree.condition1:
        print_main_rules(d, i, tree.clazz)
        return d
    if tree.left:    
        if tree.condition1 not in d:
            d.update({tree.condition1: [d_features[tree.condition1][0], tree.condition3]})
        else:
            d[tree.condition1][1] = tree.condition3        
        process_main_rules(tree.left, 'L', d, i)
    if tree.right:
        if tree.condition1 not in obj:
            d.update({tree.condition1: [tree.condition3+1, d_features[tree.condition1][1]]})
        else:
            d[tree.condition1][0] = d[tree.condition1][1]+1
            d[tree.condition1][1] = obj[tree.condition1][1]
        process_main_rules(tree.right, 'R', d, i)
    
    return d

def main(i):    
    file = open('{}/tree.dot'.format(dir, i), 'r') 

    list = {}
    tree = None
    for line in file: 
        l = line.split('\\n')
        idx = line.split(' -> ')
        level = 0
        if len(l) == 5 or len(l) == 4:
            l_ = l[0].split(' [')
            level = int(l_[0])
            list[level] = montaTree(line)
            #print('{}, {}, {} {} {}, ELSE: {}'.format(list[level].level, list[level].clazz, list[level].condition1,list[level].condition2,
            #     list[level].condition3,list[level].elze))
        elif len(idx) == 2:
            idx1 = int(idx[0])
            idx2 = int(idx[1].split(' ')[0])
            t = list[idx1]

            if t.left: t.right = list[idx2]
            else: t.left = list[idx2]

            #print('{}, {}, {} {} {}, ELSE: {}'.format(t.level, t.clazz, t.condition1,t.condition2,t.condition3,t.elze))

    str = ''

    #list[0].display()
    print()
    range_pre_order(list[0], 'Root', dict(), i, '')

    d = pre_ordem(list[0], 'Root', dict(), i)

    print (dic)

    max_tab = len(interval)
    b = 1
    interval_rng = dict()
    for key1 in interval:
        interval[key1].sort()
        a = 1
        n = d_names[key1].replace('_', '.')
        n_ = n.replace('.', '_')
        print (f'   \"ingress::tbl_{n_}\": {{"rules\": [')
        max_match = len(interval[key1])

        for x in range(0, max_match-1):
            if x % 2 != 0:
                continue
            print (f'')
            rng = ''
            opp = ''
            if x != 0 and interval[key1][x-1] < interval[key1][x]-1:
                rng = f'{interval[key1][x-1]+1}->{interval[key1][x]-1}'
                print_range_rule(i, n, n_, a, rng, a, max_match)
                update_dict(interval_rng, key1, rng, a)
                a += 1
            
            rng = f'{interval[key1][x]}->{interval[key1][x+1]}'
            if x < max_match -2:
                opp = f'{interval[key1][x+1]}->{interval[key1][x+2]}'
                if opp in dic[key1]:
                    rng = f'{interval[key1][x]}->{interval[key1][x+1]-1}'
                    print_range_rule(i, n, n_, a, rng, a, max_match)
                    update_dict(interval_rng, key1, rng, a)
                    a += 1
                    rng = f'{interval[key1][x]}->{interval[key1][x+1]}'

                    print (f'OPPOSITE: {opp}')
                    print(dic[key1])
            opposite = rng.split('->')
            opposite = f'{opposite[1]}->{opposite[0]}'

            print_range_rule(i, n, n_, a, rng, a, max_match)
            update_dict(interval_rng, key1, rng, a)
            a += 1

        print ('    ] },' if b < max_tab else '    ] }')
        b += 1
    print('  } } ')
    print()
    print(list[0])
    process_main_rules(list[0], 'Root', dict(), interval_rng)


    return

if __name__ == '__main__':
    import sys
    a = 1
    sys.stdout = open('{}/p4_2.json'.format(dir), 'w')
    for x in range(0,1):
        main(x)


