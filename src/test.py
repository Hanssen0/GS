import csv
from utils.preprocess_utils import *
from utils.item_grading import *
import re
import json
from init_utils import *
root = init_by_key('root')


def judge_folder(folder_path,model):



    list = listdir(folder_path,[])
    score = 60
    to_pro = {}
    pro = []
    f = False
    # name = folder_path.split('/')[-1].split('.')[0]
    name = "tmp"
    file_name = root+'data/out/'+name+'.json'
    for index,file in enumerate( list):

        dic = initdict()
        pos_list = []
        text = ''

        if('docx' in file):
            text = readdocx(file)
        elif('pdf' in file):
            text = readpdf(file)
        if(not is_pdf_legal(text)):
            continue
        if(len(text)>0):
            f = True
            project_dic={}
            f_name = file.split('/')[-1].split('.')[0]
            project_dic['NAME'] = f_name
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
            pro.append(project_dic)
            to_pro['SCORE'] = judge_score_list(name,pro,True)

    if(f):
        to_pro['FILES'] = pro
        with open(file_name,'w',encoding='utf8') as file_obj:

            json.dump(to_pro,file_obj,indent=4,ensure_ascii=False)

            print(name+'写入成功')
        return to_pro
def sim_json(js):
    s_js = {}
    score={}
    files=[]

    score['AI'] = js['SCORE']['AI']
    for f in js['FILES']:
        new_f = {}
        new_f['NAME'] = f['NAME']
        labels = f['LABELS']
        new_ls = {}
        etys=[]

        for l in labels.keys():

            if(len(labels[l]['items'])>0):
                new_ls[l]={}
                new_ls[l]['items'] = labels[l]['items']
        new_f['LABELS'] = new_ls

        for e in f['ENTITYS']:
            new_e = {}
            new_e['name'] = e['name']
            etys.append(new_e)
        new_f['ENTITYS']= etys
        files.append(new_f)



    s_js['FILES']     = files
    s_js['SCORE']     = score



    return s_js




def init_data():
    csv_f = csv.reader(root+'data/wimai_10k.csv')
    str = ''
    with open(root+'data/waimai_10k.csv', 'r') as f:    #设置文件对象
        csv_f = csv.reader(f)
        for index,l in enumerate(csv_f):
            if(not index==0):
                line = '__label__'+l[0]+' '+l[1]+'\n'
                str = str+line
    with open(root+'data/train_test.txt','w') as f:    #设置文件对象
        f.write(str)

def check_titles(text):
    heads= ['研发背景','项目概述','项目概况','技术方案','产品现状','进展状况','态势展望','行业概括','市场前景','项目背景','项目的优势','市场分析','执行总结','风险分析','发展战略','产品介绍','产品和服务介绍','营销计划',
            '财务规划','财务管理','风险及对策','行业概况','财务分析','风险预期','团队介绍','学生团队','团队架构','顾问团队','营销策略','商业模式','公司管理','风险管理与对策','团队介绍','竞争分析','比对'
        ,'对比','可行性分析','背景介绍','项目现状','营销推广','营销策略','核心团队','财务预测','未来发展','未来展望']
    # table = [{}*5][]
    application_form = ['参赛类别','主要成员','报名表','项目类别','项目简介','参赛赛道','项目名称','申报表','指导教师意见','指导老师']
    cnt = 0

    for t in application_form:
        if t in text:
            cnt+=2
    if(cnt<4):
        cnt = 0
        for t in heads:
            if t in text:
                cnt+=1
    if(cnt>=3):
        return True
    return False


def check_sentence(text):
    sents = text.replace(' ','').split('。')
    repeated_s = 0
    for s in sents:
        if(len(s)<2):
            continue
        cnt_s = sents.count(s)
        if(cnt_s>4):
            repeated_s+=1
        if(cnt_s>6):
            return False
    if(repeated_s>3):
        return False
    return True
def is_pdf_legal(text):



    res_t=check_titles(text)
    res_h= check_sentence(text)
    if( res_t and  res_h):
        return True
    return False

def is_docx_legal(text):



    res_t=check_titles(text)
    res_h= check_sentence(text)
    if( res_t and  res_h):
        return True
    return False

def is_file_legal(path):
    list = listdir(path,[])
    res = False
    for index,file in enumerate( list):

        text = ''
        if('docx' in file):
            text = readdocx(file)
        elif('pdf' in file):
            text = readpdf(file)
        if(not text==''):
            res = is_pdf_legal(text)
            if(res):
                return True
    return False


if __name__=='__main__':
    # train_f = 'data/train_test.txt'
    # model = fasttext.train_supervised('data/train2.txt',
    #                                   label_prefix='__label__',
    #                                   lr=0.1,
    #                                   dim=100,
    #                                   epoch=50,
    #                                   neg=2)
    # model_name = root+'model/classify_8.bin'
    # model = fasttext.load_model(model_name)
    # path = root+'data/test/第六届互联网+大赛西浦参赛BP'
    # all_file = os.walk(root+'data/test/第六届互联网+大赛西浦参赛BP')
    # files = []
    # for f in all_file:
    #    if os.path.isdir(f[0]) and (not f[0]==path) :
    #         js = judge_folder(f[0])
    #         s_js = sim_json(js)
        #`
    f_path = "/Users/oo/STUDY/STUDY/Postgraduate/papers/wordCl/data/src_data/"
    # f_path = "/Users/oo/STUDY/STUDY/Postgraduate/papers/wordCl/data/src_data/苏州服务外包2020第六届江苏省互联网+大赛外包学院校内决赛送评委审阅材料/4 (红旅)“一箭三雕”生态养殖创业项目/"
    is_file_legal(f_path)


