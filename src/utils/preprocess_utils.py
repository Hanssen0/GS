from utils.utils import *
import json
from init_utils import *
root = init_by_key('root')


def preprocess_docx2txt(list):

    for index,docx_f in enumerate( list):
        name = docx_f.split('/')[-1].split('.')[0]
        if ('.docx' in docx_f):
            print(str(index)+'：'+docx_f)
            text = readdocx(docx_f)
            if(text!=''):
                with open(root+'data/tmp/txt/'+name+'.txt','w') as f:    #设置文件对象
                    f.write(text)


def preprocess_docx():
    list = listdir(root+'data/trainingdata')
    docxlist = []


    for f in list :
        if(('docx') in f):
            docxlist.append(f)
    print(len(docxlist))

    for docx_f in docxlist:
        file_name = docx_f.split('/')[-1]
        dstfile = root+'data/tmp/docx/'+file_name
        copyfile(docx_f,dstfile)

def str2list(str):
    l = str.split()
    return l

def savelist(storage_file,list):
    if storage_file!="":
        with open(storage_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(list, indent=4 ,ensure_ascii=False))


def savenouns():
    nouns_list = []
    txt_list = listdir(root+'data/tmp/txt')
    for index,txt_file in enumerate( txt_list):
        if('.txt' in txt_file):
            with open(txt_file,'r') as f:
                text = f.read()
                nouns = use_jieba_parti(text)
                print(nouns)
                for n in nouns:
                    if(not n in nouns_list):
                        nouns_list.append(n)

    with open(root+'data/tmp/nouns.txt', 'w') as f:    #设置文件对象
        f.write(str(nouns_list))
def printdic(dic,senc,print_item = False):

    for item in dic:
        del_set = set()
        for it in dic[item]:
            pos  = []
            if(item =='__label__ACADEMIC'):
                pos = screen_acdimic_dict(it,senc)


            else:
                pos = find_pos(senc,it)
            if len(pos)==0:
                del_set.add(it)
            else:
                print('   '+it+':'+str(pos))
            if(print_item):
                for p in pos:
                    print('      '+str(p)+":"+senc[p])
        for it in del_set:
            dic[item].remove(it)

def screen_acdimic_dict(it,senc):
    new_pos = []
    flags = ['学院','大学']
    pos = find_pos(senc,it)
    # print('   '+it+':'+str(pos))
    for p in pos:
        for flag in flags:
            if flag in senc[p]:
                new_pos.append(p)
                break
    return new_pos

def find_pos(senc,n) : #找单词在哪句话
    l = []
    for index , s in enumerate(senc):
        if not s.find(n) == -1 :
            l.append(index)
    return l

