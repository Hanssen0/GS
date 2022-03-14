import tarfile
import zipfile
import rarfile
import shutil
import time
from init_utils import *
root = init_by_key('root')

def uncompress(file,type,cur_name):

    l = ['docx','pdf']
    list = []
    package = None
    if(type=='zip'):
        package = zipfile.ZipFile(file)
        list = package.namelist() # 得到压缩包里所有文件
        # shutil.rmtree('要清空的文件夹名')
    elif(type=='rar'):
        package = rarfile.RarFile(file, mode='r') # mode的值只能为'r'
        list = package.namelist() # 得到压缩包里所有的文件
    elif(type == 'tgz' or type == 'tar' or type == 'gz'):
        # file_type == '.tgz' or file_type == '.tar' or file_type == '.gz'
        # Python自带tarfile模块
        package = tarfile.open(file)
        list = package.getnames()

    elif(type=='docx'):
        list.append(file.filename)

    elif(type=='pdf'):
        list.append(file.filename)
    if(len(list)>0):

        os.mkdir(root+'data/var/www/uploads/'+cur_name)
        os.mkdir(root+'data/var/www/uploads/'+cur_name+'/'+'tmp')
        for f in list:
            newname = ''
            try:
                newname=f.encode('cp437').decode('gbk');
            except:
                try:#此处多进行了一次判断
                    newname=f.encode('cp437').decode('utf-8');
                except:
                    newname=f
            t_l = newname.split('.')
            if(len(t_l)>0 and t_l[-1]  in l):
                if(not package==None):
                    package.extract(f, root+'data/var/www/uploads/'+cur_name+'/'+'tmp')# 循环解压文件到指定目录
                    shutil.move(root+'data/var/www/uploads/'+cur_name+'/'+'tmp/'+f,root+'data/var/www/uploads/'+cur_name+'/'+newname.split('/')[-1])
                else:
                    file.save(root+'data/var/www/uploads/'+cur_name+'/'+newname.split('/')[-1])


                # os.rename('../data/var/www/uploads/'+f.split('//')[-1],'../data/var/www/uploads/'+newname)
        shutil.rmtree(root+'data/var/www/uploads/'+cur_name+'/'+'tmp')



    # 一次性解压所有文件到指定目录
    # rf.extractall(path) # 不传path，默认为当前目录
    # shutil.rmtree('要清空的文件夹名')
    return list



# def uncompress(src_file, dest_dir):
#     """解压各种类型的压缩包
#
#     :param src_file: 你要解压的压缩包文件
#     :type src_file: file
#     :param dest_dir: 你要解压到的目标路径
#     :type dest_dir: str
#     """
#
#     file_name, file_type = os.path.splitext(src_file.name)
#
#     if file_type == '.zip':
#         # 需要安装zip包：pip install zipp
#         zip_file = zipfile.ZipFile(src_file)
#         for names in zip_file.namelist():
#             zip_file.extract(names, dest_dir)
#         zip_file.close()
#
#     elif file_type == '.rar':
#         # 需要安装rar包：pip install rarfile
#         rar = rarfile.RarFile(src_file)
#         os.chdir(dest_dir)
#         rar.extractall()
#         rar.close()
#
    # else:
    #     # file_type == '.tgz' or file_type == '.tar' or file_type == '.gz'
    #     # Python自带tarfile模块
    #     tar = tarfile.open(fileobj=src_file)
    #     for name in tar.getnames():
    #         tar.extract(name, dest_dir)
    #     tar.close()
#     return True


if __name__ == '__main__':

    dest_dir = '/Users/oo/Downloads'
    filename = ''
    filename = '/Users/oo/Downloads/012+ 高校共享吹风机/高校共享吹风机 项目计划书.docx'
    # shutil.unpack_archive(filename, extract_dir=None, format=None)
    timestamp = str(time.time())
    cur_timestamp = timestamp.replace('.', '')

    uncompress(filename,'docx',cur_timestamp)
    # uncompress(filename,'docx',cur_timestamp)
