import sys
# 如果是 python2.x 还需要加上下面两行，默认编码 gbk，转为 utf8
# reload(sys)
# sys.setdefaultencoding('utf8')
from flaskdemo import app as application
sys.path.insert(0, '/var/www/html/src/')
if __name__ == '__main__':
    app.run()


