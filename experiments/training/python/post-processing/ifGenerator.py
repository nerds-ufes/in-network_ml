from decimal import Decimal
d_class = {'benign':0, 'dos_hulk': 1, 'dos_goldeneye': 2, 'dos_slowhttptest': 3, 'wa_brute_force': 4, 'dos_slowloris': 5, 'i_portscan': 6}
#d_feature = {'benign':0, 'dos_hulk': 1, 'dos_goldeneye': 2, 'dos_slowhttptest': 3, 'wa_brute_force': 4, 'dos_slowloris': 5, 'i_portscan': 6}

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
        t.condition3 = l_[2]
    else:
        t.elze = True
    l_ = l[0].split(' [')
    level = int(l_[0])
    t.level = level
    return t

def ordem(tree, str, strif): 
    if not tree: return
    #print('{}{}, {}, {} {} {}, ELSE: {}'.format(str, tree.level, tree.clazz, tree.condition1,tree.condition2,tree.condition3,tree.elze))
    level = ''
    if 'rigth' in strif:
        f2.write('{}{}else \n'.format(level, str[0:-4]))
    if tree.condition1:
        f2.write('{}{}if ({} {} {}) \n'.format(level, str, tree.condition1,tree.condition2,int(Decimal(tree.condition3))))
    if tree.elze and strif == 'left': 
        f2.write('{}{}meta.class = {};\n'.format(level, str, d_class[tree.clazz]))
    if tree.elze and 'rigth' in strif: 
        f2.write('{}{}meta.class = {};\n'.format(level, str, d_class[tree.clazz]))

    str +='    '
    else_ = ''        
    if tree.left and tree.left.elze:
        else_ = ' else'        

    ordem(tree.left, str, 'left')
    ordem(tree.right, str, 'rigth'+else_)

dir = '../results/tmp'
if __name__ == '__main__':
    file = open('{}/tree.dot'.format(dir), 'r') 

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

    f2= open("{}/if.txt".format(dir),"w+")
    ordem(list[0], '    ', f2)
    f2.close()
    
    str = open('{}/if.txt'.format(dir), 'r').read()
    str2 = open('if_Model.py', 'r').read()

    f2= open("{}/if_Test.py".format(dir),"w+")
    f2.write(str2.replace('*if*', str))
    f2.close()