import xml.dom.minidom as xmldom
import os

file = os.path.abspath(__file__)
root = file[0:len(file)-18]
def init_by_key(key):
    global Vs
    domTree = xmldom.parse(root+"/config/variables.xml")
    # 文档根元素
    rootNode = domTree.documentElement
    print(rootNode.nodeName)

    # 所有顾客
    items = rootNode.getElementsByTagName("item")
    for it in items:
        k =  it.getElementsByTagName("key")
        name = k[0].firstChild.data
        val =  it.getElementsByTagName("value")
        if(name.lower()==key.lower()):
            value = (val[0].firstChild.data)

            return value
