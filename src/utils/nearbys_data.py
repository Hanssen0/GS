import synonyms
from src.utils.preprocess_utils import *
from init_utils import *
root = init_by_key('root')

txt_list = []
for file in os.listdir(root+'data/tmp/entity'):
    file_path = os.path.join(root+'data/tmp/entity', file)
    if os.path.isdir(file_path):
        listdir(file_path, list)
    else:
        txt_list.append(file_path)

train_f = open(root+'data/tmp0208.txt', 'w')
head = '__label__'
for index,txt_file in enumerate( txt_list):
    l = []
    if('.txt' in txt_file):
        lable = head+(txt_file.split('/')[-1].split('.')[0]).upper()
        with open(txt_file,'r') as f: #设置文件对象
            str  = f.read()
            l = str2list(str)
            for item in l :
                nearbys = synonyms.nearby(item, 10)[0]
                for nb in nearbys:
                    train_f.write(lable+' '+nb+'\n')