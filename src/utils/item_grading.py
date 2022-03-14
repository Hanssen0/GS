from init_utils import *
root = init_by_key('root')
MAX_THRESHOLD = 10
UNIT = 1
WEIGHT_l1 = 2
WEIGHT_l2 = 1.5
WEIGHT_l3 = 1.25
l1 = []
l2 = []
l3 = []
add_str = ''
org_list = []

Vs = {}
# root = '/home/oo/wordCl/'


def init_Vs():
    global Vs
    domTree = xmldom.parse(root+"/config/variables.xml")
    # 文档根元素
    rootNode = domTree.documentElement
    print(rootNode.nodeName)
    levels = ['UNIT','WEIGHT_l1','WEIGHT_l2','WEIGHT_l3']
    # 所有顾客
    items = rootNode.getElementsByTagName("item")
    for it in items:
        k =  it.getElementsByTagName("key")
        name = k[0].firstChild.data
        val =  it.getElementsByTagName("value")
        if(name not in levels):
            continue
        value = float(val[0].firstChild.data)
        Vs[name] = value

def grade_item(dic):
    init_lists()
    global add_str
    add_score = 0
    for it in dic:
        # if (it=='__label__ACADEMIC'):
        add_score+=grade_acdemic(dic[it])
    return add_score,add_str

def init_lists():
    global add_str
    add_str = ''

    for i in range(3):
        f = open(root+'data/level_E/l'+str(i+1)+'.txt',encoding = "utf-8")
        lines = f.readlines()
        if(i==0):
            global l1
            l1 = [item.strip()  for item in lines]
        elif(i==1):
            global l2
            l2 = [item.strip()  for item in lines]
        elif(i==2):
            global l3

            l3 = [item.strip()  for item in lines]

    
def grade_acdemic(items):
    scroe = 0
    global Vs,UNIT,WEIGHT_l1,WEIGHT_l2,WEIGHT_l3
    global add_str
    init_Vs()
    for it in items :
        if it in l1:
            if WEIGHT_l1 in Vs.keys():
                WEIGHT_l1 = Vs['WEIGHT_l1']
            scroe+=(UNIT*WEIGHT_l1)
            add_str = add_str+' + ( l1: '+it+')'
        elif it in l2:
            if WEIGHT_l2 in Vs.keys():
                WEIGHT_l2 = Vs['WEIGHT_l2']
            scroe+=(UNIT*WEIGHT_l2)
            add_str = add_str+' + ( l2: '+it+')'

        elif it in l3:
            if WEIGHT_l3 in Vs.keys():
                WEIGHT_l3 = Vs['WEIGHT_l2']
            scroe+=(UNIT*WEIGHT_l3)
            add_str = add_str+' + ( l3: '+it+')'

    return scroe

def grade_acdemic(items):
    scroe = 0

    global add_str
    global Vs,UNIT,WEIGHT_l1,WEIGHT_l2,WEIGHT_l3
    if UNIT in Vs.keys():
        UNIT = Vs['UNIT']
    for it in items :

        if it in l1:
            if WEIGHT_l1 in Vs.keys():
                WEIGHT_l1 = Vs['WEIGHT_l1']
            sc = UNIT*WEIGHT_l1
            scroe+=sc
            add_str = add_str+' + '+str((sc))+'( l1: '+it+')'
        elif it in l2:
            if WEIGHT_l2 in Vs.keys():
                WEIGHT_l2 = Vs['WEIGHT_l2']
            sc = UNIT*WEIGHT_l2
            scroe+=sc
            add_str = add_str+' + '+str((sc))+'( l2: '+it+')'

        elif it in l3:
            if WEIGHT_l3 in Vs.keys():
                WEIGHT_l3 = Vs['WEIGHT_l2']
            sc = UNIT*WEIGHT_l3
            scroe+=sc
            add_str = add_str+' + '+str((sc))+'( l3: '+it+')'
    return scroe

def added_points(items):

    l = []
    init_lists()
    global Vs,UNIT,WEIGHT_l1,WEIGHT_l2,WEIGHT_l3
    init_Vs()
    if 'UNIT' in Vs.keys():
        UNIT = Vs['UNIT']
    if 'WEIGHT_l3' in Vs.keys():
        WEIGHT_l3 = Vs['WEIGHT_l2']
    if 'WEIGHT_l2' in Vs.keys():
        WEIGHT_l2 = Vs['WEIGHT_l2']
    if 'WEIGHT_l1' in Vs.keys():
        WEIGHT_l1 = Vs['WEIGHT_l2']
    for it in items :
        dic = {}
        if it in l1:
            dic['name'] = it
            dic['score']  = UNIT*WEIGHT_l1
            l.append(dic)

        elif it in l2:
            dic['name'] = it
            dic['score']  = (UNIT*WEIGHT_l2)
            l.append(dic)

        elif it in l3:
            dic['name'] = it
            dic['score']  = (UNIT*WEIGHT_l3)
            l.append(dic)


    return l

def com_score(dic,com = False):
    if(com):
        pass