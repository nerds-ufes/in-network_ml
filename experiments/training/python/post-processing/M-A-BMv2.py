from decimal import Decimal
import copy

d_class = {'benign':0, 'dos_hulk': 1, 'dos_goldeneye': 2, 'dos_slowhttptest': 3, 'wa_brute_force': 4, 'dos_slowloris': 5, 'i_portscan': 6}
d_features = {'TcpDstPort':(0, 65000), 'PacketSize': (0, 1500), 'hdr.tcp.ctrl': (0, 63), 'hdr.ipv4.flags': (0,3), 'UdpDstPort': (0,65000), 'hdr.tcp.ecn': (0,3), 'EtherType': (0, 65535), 'Protocol': (0, 255)}


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

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.condition1:
            self.key = '{} {} {}'.format( self.condition1, self.condition2, self.condition3)
        else:
            self.key = 'class={}'.format(self.clazz)    
        if self.right is None and self.left is None:
            line = '{}'.format(self.key)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2




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

def pre_ordem(tree, lado, obj, i):
    d = copy.deepcopy(obj)
    if not tree.condition1:
        print('table_add tbl_rf{} rf{} {} {} {} {} {} {} {} {} =>  {} 1 '.format(i+1, i+1, feature(d, 'EtherType'),
                                                feature(d, 'Protocol'), feature(d, 'hdr.ipv4.flags'),
                                                feature(d, 'PacketSize'), feature(d, 'TcpDstPort'),
                                                feature(d, 'hdr.tcp.ctrl'), feature(d, 'hdr.tcp.ecn'),
                                                 feature(d, 'UdpDstPort'), d_class[tree.clazz]+2))
        return
    
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
    file = open('{}/treeRF{}.dot'.format(dir, i), 'r') 
    print ('table_set_default tbl_rf{} drop'.format(i+1))

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
    pre_ordem(list[0], 'Root', dict(), i)
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
    sys.stdout = open('{}/s1-command.txt'.format(dir), 'w')
    for x in range(0,5):
        main(x)


