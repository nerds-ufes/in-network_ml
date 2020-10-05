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

def feature(d, f):
    if f in d:
        return '{}->{}'.format(d[f][0], d[f][1])
    else:
        return '{}->{}'.format(d_features[f][0], d_features[f][1])

a = 1
e = 1
dic = dict()
printed = dict()

def dic_feature(d, f):
    feat = feature(d,f)
    global e
    if f not in dic:
        dic.update({f: dict([(feat, e)])})
        e += 1
    elif feat not in dic[f]:
        dic[f].update({feat: e})
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

        print (f'       {{"name\": \"dt{i}_rule{c}\", \n        "match\": {{ ')
        print (f'              "ingress::scalars.metadata@{d_names["EtherType"]}": {{"value": "{eth}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["TcpDstPort"]}": {{"value": "{tP}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["PacketSize"]}": {{"value": "{size}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["hdr.tcp.ctrl"]}": {{"value": "{ctrl}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["hdr.ipv4.flags"]}": {{"value": "{flag}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["UdpDstPort"]}": {{"value": "{uP}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["hdr.tcp.ecn"]}": {{"value": "{ecn}"}}, ')
        print (f'              "ingress::scalars.metadata@{d_names["Protocol"]}": {{"value": "{pro}"}} ')
        print ( '       },')
        print(f'        \"action\": {{\"type\": \"ingress::act_dt\",\"data\": {{\"port\": {{\"value\": \"v0.{d_class[tree.clazz]+1}\"}} }} }}')
        print('   },')
        c += 1


        return d
    
    #print('{} / {}<={}'.format(d, tree.condition1, tree.condition3))

    if tree.left:
        if tree.condition1 not in d:
            d.update({tree.condition1: [d_features[tree.condition1][0], tree.condition3]})
            #dic[tree.condition1] == (0, tree.condition3)
        else:
            d[tree.condition1][1] = tree.condition3        
        pre_ordem(tree.left, 'L', d, i)
    if tree.right:
        if tree.condition1 not in obj:
            d.update({tree.condition1: [tree.condition3+1, d_features[tree.condition1][1]]})
        else:
            d[tree.condition1][0] = d[tree.condition1][1]+1
            d[tree.condition1][1] = obj[tree.condition1][1]
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
            #dic[tree.condition1] == (0, tree.condition3)
        else:
            d[tree.condition1][1] = tree.condition3        

        f = feature(d, tree.condition1)
        if tree.condition1 not in dic:
            dic.update({tree.condition1: dict([(f, e)])})
            #print(f'{tree.condition1} {e} : {f}')
            e += 1
        elif feat not in dic[tree.condition1]:
            dic[tree.condition1].update({f: e})
            #print(f'{tree.condition1} {e} : {f}')
            e += 1


        range_pre_order(tree.left, 'L', d, i, feat)
    if tree.right:
        if tree.condition1 not in obj:
            d.update({tree.condition1: [tree.condition3+1, d_features[tree.condition1][1]]})
        else:
            d[tree.condition1][0] = d[tree.condition1][1]+1
            d[tree.condition1][1] = obj[tree.condition1][1]

        f = feature(d, tree.condition1)
        if tree.condition1 not in dic:
            dic.update({tree.condition1: dict([(f, e)])})
            #print(f'{tree.condition1} {e} : {f}')
            e += 1
        elif feat not in dic[tree.condition1]:
            dic[tree.condition1].update({f: e})
            #print(f'{tree.condition1} {e} : {f}')
            e += 1
        
        range_pre_order(tree.right, 'R', d, i, feat)
    


def ordem(tree, str, strif): 
    if not tree: return
    #print('{}{}, {}, {} {} {}, ELSE: {}'.format(str, tree.level, tree.clazz, tree.condition1,tree.condition2,tree.condition3,tree.elze))
    level = ''
    if 'rigth' in strif:
        f2.write('{}{}else \n'.format(level, str[0:-4]))
    if tree.condition1:
        f2.write('{}{}if ({} {} {}) \n'.format(level, str, tree.condition1,tree.condition2,int(Decimal(tree.condition3))))
    if tree.elze and strif == 'left': 
        f2.write('{}{}meta.class = \'{}\';\n'.format(level, str, tree.clazz))
    if tree.elze and 'rigth' in strif: 
        f2.write('{}{}meta.class = \'{}\';\n'.format(level, str, tree.clazz))

    str +='    '
    else_ = ''        
    if tree.left and tree.left.elze:
        else_ = ' else'        

    ordem(tree.left, str, 'left')
    ordem(tree.right, str, 'rigth'+else_)

dir = '../results/tmp'

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
    range_pre_order(list[0], 'Root', dict(), i, 'EtherType')
    print (f'{{ \"tables\": {{')
    print (f'   \"ingress::tbl_dt\": {{"rules\": [')

    d = pre_ordem(list[0], 'Root', dict(), i)
    print ('    ] },')

    max_tab = len(dic)
    b = 1
    for key1 in dic:
        a = 1
        n = d_names[key1].replace('_', '.')
        n_ = n.replace('.', '_')
        print (f'   \"ingress::tbl_{n_}\": {{"rules\": [')
        max_match = len(dic[key1])
        for key2 in dic[key1]:
            print (f'       {{"name\": \"dt{i}_{n_}_rule{a}\", \n        "match\": {{ "{n}": {{"value": "{key2}"}} }},')
            print(f'        \"action\": {{\"type\": \"ingress::act_{n_}\",\"data\": {{\"clazz\": {{\"value\": \"{dic[key1][key2]}\"}} }} }}')
            print('       },' if a < max_match else '       }')
            a += 1

        print ('    ] },' if b < max_tab else '    ] }')
        b += 1
    print('  } } ')
    
    return

    f2= open("{}/if.txt".format(dir),"w+")
    ordem(list[0], '    ', f2)
    f2.close()
    
    str = open('{}/if.txt'.format(dir), 'r').read()
    str2 = open('if_Model.py', 'r').read()

    f2= open("{}/if_Test.py".format(dir),"w+")
    f2.write(str2.replace('*if*', str))
    f2.close()

if __name__ == '__main__':
    import sys
    a = 1
    sys.stdout = open('{}/p4.json'.format(dir), 'w')
    for x in range(0,1):
        main(x)


