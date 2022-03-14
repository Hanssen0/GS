from utils.utils import *
from init_utils import *
root = init_by_key('root')
colls = []

def use_jieba_parti(sen = ''):
    list = listdir(root+'data/trainingdata')
    jieba.load_userdict(root+'data/refine_cla/dict/coll.txt')

    nouns = []
    words = jieba.cut(sen)
    stopwords = stopwordslist(root+'data/stopwords.txt')
    for word, flag in words:
        if word not in stopwords:
            if('n' in flag):
                nouns.append(word)
    return nouns
    # print ('%s %s'%  (word, flag))

def deal_org_txt(org_txt): #处理原始txt
    list = str.split(org_txt)
    for item in list:
        new_item = item + ' nt'
        if(item not in colls):
            # print(new_item)
            words = pseg.cut(item)
            print(words[0])
        colls.append(item)


if __name__=='__main__':
    org_list = listdir(root+'data/refine_cla/org')
    for txt_file in org_list:
        if('txt' in txt_file):
            with open(txt_file,'r') as f:
                text = f.read()
                deal_org_txt(text)
                print()
                print()


