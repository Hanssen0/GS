import fasttext
import re
from utils.item_grading import *
from src.utils.preprocess_utils import *
from init_utils import *
root = init_by_key('root')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #
    model_name = root+'model/classify_8.bin'
    #
    # dic = initdict()

    # sen = "“筑梦·红色家园”公益创业项目旨在构筑扶贫模式，助力脱贫攻坚，传承红色文化，守护精神家园，以向贫困人民传播红色文化为最终目的。该项目集聚创意规划红色教育活动、爱心支教、设计APP、网络教育课程服务号、情景游戏于一身，以整合社会公益资源、提供公益服务平台，致力于实现线上与线下互动的完美结合。\
    # 在创意规划红色教育活动方案上，师范以及中文师范的优秀人才，优势有团队专业性强，同属教育领域；空暇时多，项目运行周密；团队意志坚定，热忱公益活动。团队分工如下：项目负责人（统筹规划项目进程）、财务负责人（财务管理）、市场部负责人（宣传策划）、技术人员（线上平台建设）。"
    # nouns = use_jieba_parti(sen)
    # print(nouns)

    # preprocess_docx()
    # path = 'data/tmp/docx'
    # list = listdir('data/tmp/docx')

    # docx_f = 'data/tmp/docx/基于蛋白纳米反应器的肿瘤诊疗一体化纳米药物的开发-商业计划书-龚黎明.docx'
    # readdocx(docx_f)
    # preprocess_docx2txt(list)
    # for index,docx_f in enumerate( list):
    #     name = docx_f.split('/')[-1].split('.')[0]
    #     if ('.docx' in docx_f):
    #         print(str(index)+'：'+docx_f)
    #         text = readdocx(docx_f)
    #         if(text!=''):
    #             with open('data/tmp/txt/'+name+'.txt','w') as f:    #设置文件对象
    #                 f.write(text)
    # nouns_list = []
    # txt_list = listdir('data/tmp/txt')
    # for index,txt_file in enumerate( txt_list):
    #     if('.txt' in txt_file):
    #         with open(txt_file,'r') as f:    #设置文件对象
    #             text = f.read()
    #             nouns = use_jieba_parti(text)
    #             print(nouns)
    #             for n in nouns:
    #                 if(not n in nouns_list):
    #                     nouns_list.append(n)
    #
    # with open('data/tmp/nouns.txt','w') as f:    #设置文件对象
    #             f.write(str(nouns_list))

    #
    # model = fasttext.train_supervised('data/train2.txt',
    #                                   label_prefix='__label__',
    #                                   dim = 512,
    #                                   epoch = 100,
    #                                   lr = 0.05,
    #                                   lr_update_rate = 50,
    #                                   min_count = 3,
    #                                   loss = 'softmax',
    #                                   word_ngrams = 2,bucket = 1000000)
    # model.save_model(model_name)
    # #加载模型
    # 使用fasttext的load_model进行模型的重加载
    model = fasttext.load_model(model_name)
    #     str = '这个小组出自于南京信息工程大学'
    #     y = model.predict('好吃极了')
    #     print(y)

    # nouns = use_jieba_parti(str)
    #     for n in nouns:
    #         y = model.predict(n)
    #         if(y[1]>0.5):
    #             dic[y[0][0]].add(n)
    #
    # y = model.predict('一等奖')
    # print(y)
    # y = model.predict('北京大学')
    # print(y)

    # list = listdir('data/test')
    list = listdir(root+'data/test/show0112')
    for index,docx_f in enumerate( list):

        dic = initdict()
        pos_list = []
        score = 60
        str1 = " = 60(基础分数) "
        if('docx' in docx_f):

            project_dic={}

            name = docx_f.split('/')[-1].split('.')[0]
            file_name = root+'data/out/'+name+'.json'


            project_dic['NAME'] = name
            text = readdocx(docx_f)

            nouns = use_jieba_parti(text)
            # senc = text.split('。')
            senc = re.split('[。\n]',text)
            for n in nouns:
                y = model.predict(n)
                if(y[1]>0.45):
                    pos = find_pos(senc,n)
                    if(len(dic[y[0][0]])==0):
                        score = score+1
                        str1 = str1+'+ 1'+'('+y[0][0]+') '
                    dic[y[0][0]]['items'].append(n)
                    dic[y[0][0]]['score'] = 1
            # add_s,add_str = grade_item(dic)
            added_point = added_points(nouns)

            project_dic['LABELS'] = dic

            project_dic['ENTITYS'] = added_point
            project_dic['SCORE'] = judge_score(project_dic,True)

        with open(file_name,'w',encoding='utf8') as file_obj:

            '''写入json文件'''
            json.dump(project_dic,file_obj,indent=4,ensure_ascii=False)

        print(name+'写入成功')

        # print(dic)
        # printdic(dic,senc)
        # score+=add_s
        # print(str((score))+str1+add_str)
        # print()







# classifier = fasttext.train_supervised('./data/train_data.txt',label='__label__', wordNgrams=2,epoch=20,lr=0.1,dim=100)

#参数说明
'''
train_supervised(input, lr=0.1, dim=100, 
                   ws=5, epoch=5, minCount=1, 
                   minCountLabel=0, minn=0, 
                   maxn=0, neg=5, wordNgrams=1, 
                   loss="softmax", bucket=2000000, 
                   thread=12, lrUpdateRate=100,
                   t=1e-4, label="__label__", 
                   verbose=2, pretrainedVectors="")
'''

"""
训练一个监督模型, 返回一个模型对象
@param input: 训练数据文件路径
@param lr:              学习率
@param dim:             向量维度
@param ws:              cbow模型时使用
@param epoch:           次数
@param minCount:        词频阈值, 小于该值在初始化时会过滤掉
@param minCountLabel:   类别阈值，类别小于该值初始化时会过滤掉
@param minn:            构造subword时最小char个数
@param maxn:            构造subword时最大char个数
@param neg:             负采样
@param wordNgrams:      n-gram个数
@param loss:            损失函数类型, softmax, ns: 负采样, hs: 分层softmax
@param bucket:          词扩充大小, [A, B]: A语料中包含的词向量, B不在语料中的词向量
@param thread:          线程个数, 每个线程处理输入数据的一段, 0号线程负责loss输出
@param lrUpdateRate:    学习率更新
@param t:               负采样阈值
@param label:           类别前缀
@param verbose:         ??
@param pretrainedVectors: 预训练的词向量文件路径, 如果word出现在文件夹中初始化不再随机
@return model object
"""





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
