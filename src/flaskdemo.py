import flask
from flask import Flask, render_template, request, session, send_from_directory, redirect, make_response
import JWT_demo
from utils import response_result
from dt import pymysql_demo
from utils.uncompress_utils import *
from utils.wordcloud_utils import *
from flask_cors import CORS
import time
from flask_mail import Mail, Message
from flask import jsonify
from captcha import captcha_message
from captcha.captcha_tool import CaptchaTool
from urllib import parse
import urllib.parse
import fasttext
from init_utils import *
root = init_by_key('root')
app = Flask(__name__
            ,template_folder="../data/dist",
            static_folder="../data/dist/static"
            )
app.config["SECRET_KEY"] = "156456dsadasd"
app.config['MAIL_SERVER'] = 'smtp.163.com'
# app.config['MAIL_USER_TLS'] = True
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'meta_intell@163.com'
app.config['MAIL_PASSWORD'] = 'MJZAOVPSJRXNWWUU'
app.config['MAIL_DEFAULT_SENDER'] = 'meta_intell@163.com'
mail = Mail(app)
CORS(app)
model_name = root+'model/classify_8.bin'
model = fasttext.load_model(model_name)
# root = '/home/oo/wordCl/'
captcha_code_g = ''
from test import *
@app.before_request
def before():
    print(request.path)
    if request.path == '/login' or request.path == '/logo.png' or request.path == '/sendMail' or request.path == '/testGetCaptcha' or request.path == '/wechat' or request.path == '/captchaLaunch' or request.path == '/favicon.ico' or request.path == '/getUserName' or request.path.startswith(
            "/static") or request.path.startswith(
        "/src") or request.path == '/register' or request.path == '/' or request.path == '/updatePass':
        return None
    token = request.headers.get('token')
    user = request.headers.get('username')
    user = parse.unquote(user)
    is_overdue = JWT_demo.identify(token)
    select_token_sql = "select * from user_token where userName=%s"
    sql_token = pymysql_demo.select_token(select_token_sql, [user])
    if is_overdue != user:
        result = response_result.TOKEN_NOPASS
        return jsonify(result)
@app.route("/getEmail", methods=["GET"])
def get_email():
    username = request.args.get('username')
    get_email_sql = "select email from user where userName = %s"
    res = pymysql_demo.select_email(get_email_sql, [username])
    result = {'email': res}
    return jsonify(result)
@app.route('/sendMail')
def send_mail():
    email = request.args.get('email')
    msg = Message(subject="Reset Password/重置密码",
                  sender="远见元智能<meta_intell@163.com>",
                  recipients=[email])
    email_code = captcha_message.code_generate()
    msg.body = 'text body'
    msg.html = ' <html>\
<head>\
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\
<title></title>\
<meta charset="utf-8" />\
</head>\
        <p><b>您的验证码为：{}</b><br><span class="font_gray">(请输入该验证码完成验证，验证码30分钟内有效！)</span></p> \
        <div class="line">如果你未申请服务，请忽略该邮件。</div> \
        <div class="line">此邮件由系统自动发送，请勿回复。</div>\
</html>'.format(email_code)
    with app.app_context():
        mail.send(msg)
    print("success")
    session["email_code"] = email_code
    return jsonify(response_result.SEND_EMAIL_SUCCESS)
@app.route('/emailValidate', methods=["POST"])
def email_validate():
    req = request
    str_req_data = req.data.decode('UTF-8')
    json_req_data = json.loads(str_req_data)
    email = json_req_data['email']
    code = json_req_data['code']
    username = json_req_data['username']
    if code == session['email_code']:
        user_usertype_update_sql = "update user set email=%s, userType=1 where userName=%s"
        res = pymysql_demo.user_usertype_update(user_usertype_update_sql, [email, username])
        if res:
            return jsonify(response_result.EMAIL_UPDATE_SUCCESS)
    return jsonify(response_result.EMAIL_CODE_FAILURE)
# @app.route('/')
# def index():
#     return 'hello!'
# 主页面
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    # if(name=='index'):
    #
    #     return render_template('index.html')
    # else:
    #     return app.send_static_file('logo.png')
@app.route('/src/assets/logo.png')
def logo():
    try:
        return send_from_directory('', 'logo.png')
    except Exception as e:
        print(e)
        return str(e)
@app.route('/handler', methods=["POST"])   #文件处理总流程
def handler():
    js={}
    print(request.args)
    timestamp = str(time.time())
    cur_timestamp = timestamp.replace('.', '')
    files = request.files.getlist('files')
    bp = []
    print(cur_timestamp)

    for index,f in enumerate(files):
    # f = request.files.get('filename')
        f_index = '_'+str(index)
        fname = f.filename
        type = judge_file(fname)
        f_name = os.path.splitext(fname)[0]
        print('start_uncompress')

        uncompress(f,type,cur_timestamp+f_index)
        f_path = root+'data/var/www/uploads/'+cur_timestamp+f_index+'/'
        res = is_file_legal(f_path)
        # js['msg'] = 'successfully'
        # json_data = json.dumps(js, ensure_ascii=False)
        if( not res ):
            result = response_result.UPLOAD_FAILURE_FILE_IILLEEGAL
            result["msg"] = '请上传正确的项目文件！'
            return jsonify(result)
        else:
            username = request.headers.get('username')
            username  = urllib.parse.unquote(username,encoding='utf-8')
            # sql_get_userid= "select id from user where userName = %s"
            # userid = pymysql_demo.select_get_userid(sql_get_userid, [username])
            # sql_register = "insert into user (userName, password, email, create_time, userType) values (%s, %s, %s, now(), 0)"
            # res = pymysql_demo.user_insert(sql_register, [username, password_md5, email])
            print('start_judge')
            js = judge_folder(f_path,model) #存在数据库中的json数据
            score = js['SCORE']['AI']
            res = True
            ip = request.remote_addr
            sql_record = "select * from record where user_name = %s and score = %s and json_dict = %s and ip = %s and hash=%s "
            hs = hash_list(f_path)
            res = pymysql_demo.select_record(sql_record, [username, float(score), str(js),ip,hs])
            img_base64,s = json2img(js)
            f = get_res_files(f_path,s,js)
            if(f):
                make_zip(f_path)
            if(res):
                sql_token_record_insert = "insert into record (user_name,score,file_path,upload_time,json_dict,ip,hash) values (%s, %s,%s,now(),%s,%s,%s)"
                res_token_ = pymysql_demo.record_insert(sql_token_record_insert, [username, float(score), f_path, str(js),ip,hs])
            else:
                pass
                # shutil.rmtree(f_path)
    # return {
        #     'code':500,
        #     'msg':'文件类型错误',
        #     'data':json
        # }

        # sim_js = sim_json(js)
        res = js['SCORE']['AI']  #存在数据库中的分数
        tmp = {
            'msg': res,
            'pic' :img_base64,
            'name':str(index)+'：'+f_name,
            'zip_file':cur_timestamp+f_index
        }
        bp.append(tmp)
    result = response_result.LOGIN_SUCCESS
    result['plan'] = bp
    return jsonify(result)
    # return {json_data,200,{'ContentType':'application/json'}}
    #     {
    #     'code':200,
    #     'msg':'successfully',
    #     'data':json_data
    # }
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
def judge_file(fname):
    l = ['docx','pdf','zip','rar']
    type = fname.split('.')[-1].lower()
    if(type not in l):
        return False
    else:
        return type

@app.route('/file/upload/',methods=['POST'])
def search():
    print(request.args)
    f = request.files.get('filename')
    f.save(root+'data/var/www/uploads/' + (f.filename))
    return 'search'
@app.route('/tokenAvailable', methods=["POST"])
def token_available():
    return jsonify(response_result.LOGIN_SUCCESS)
@app.route('/getUserName', methods=["GET"])
def get_username():
    # request.headers.get('token')
    username = request.args.get('username')
    print('username:', username)
    sql_get_user = "select * from user where userName = %s"
    res = pymysql_demo.select_get_user(sql_get_user, [username])
    if not res:
        return jsonify(response_result.USERNAME_OCCUPIDE)
    return jsonify(response_result.LOGIN_SUCCESS)
@app.route('/login', methods=["POST"])
def login():
    req = request
    str_req_data = req.data.decode('UTF-8')
    json_req_data = json.loads(str_req_data)
    username = json_req_data['name']
    password = json_req_data['pwd']
    captcha_img_code = json_req_data['code']
    is_captcha_img_code = test_verify_captcha(captcha_img_code)
    if not is_captcha_img_code:
        return jsonify(response_result.LOGIN_CAPTCHA_FAILURE)
    password_md5 = pymysql_demo.encode_(password)
    token = JWT_demo.generate_access_token(username)
    sql_login = "select * from user where userName = %s and password = %s"
    res = pymysql_demo.select_user_login(sql_login, [username, password_md5])
    if res != '':
        username = res[0]
        email = res[1]
        usertype = res[2]
        sql_token_user_select = "select * from user_token where userName = %s"
        res_token = pymysql_demo.select_token(sql_token_user_select, [username])
        result = response_result.LOGIN_SUCCESS
        result['username'] = username
        result['email'] = email
        result['usertype'] = usertype
        if res_token:
            sql_token_user_update = "update user_token set token=%s where userName=%s"
            res_token_ = pymysql_demo.update_token(sql_token_user_update, [token, username])
            if res_token_:
                result['token'] = token
                return jsonify(result)
        else:
            sql_token_user_insert = "insert into user_token (userName, token) values (%s, %s)"
            res_token_ = pymysql_demo.token_insert(sql_token_user_insert, [username, token])
            if res_token_:
                result['token'] = token
                return jsonify(result)
    return jsonify(response_result.LOGIN_FAILURE)
@app.route('/register', methods=["POST"])
def register():
    req = request
    str_req_data = req.data.decode('UTF-8')
    json_req_data = json.loads(str_req_data)
    username = json_req_data['name']
    password = json_req_data['pwd']
    # phone = json_req_data['phone']
    email = json_req_data['email']
    captcha = json_req_data['code']
    is_captcha = test_verify_captcha(captcha)
    if is_captcha:
        password_md5 = pymysql_demo.encode_(password)
        sql_register = "insert into user (userName, password, email, create_time, userType) values (%s, %s, %s, now(), 0)"
        res = pymysql_demo.user_insert(sql_register, [username, password_md5, email])
        if res:
            return jsonify(response_result.REGISTER_SUCCESS)
        else:
            return jsonify(response_result.REGISTER_FAILURE_PHONE_REPEAT)
@app.route('/captchaLaunch', methods=["POST"])
def captcha_launch():
    req = request
    str_req_data = req.data.decode('UTF-8')
    json_req_data = json.loads(str_req_data)
    phone = json_req_data['phone']
    captcha = captcha_message.code_generate()
    global captcha_code_g
    captcha_code_g = captcha
    res = captcha_message.message_generate(captcha_code_g, str(phone))
    if res:
        return jsonify(response_result.MESSAGE_LAUNCHED_SUCCESS)
    return jsonify(response_result.MESSAGE_LAUNCHED_FAILURE)
@app.route('/testGetCaptcha', methods=["GET"])
def test_get_captcha():
    """
    获取图形验证码
    :return:
    """
    new_captcha = CaptchaTool()
    # 获取图形验证码
    img, code = new_captcha.get_verify_code()
    img = bytes.decode(img)
    print('img=>', img)
    # 存入session
    session["code"] = code
    print("code=>", code)
    result = response_result.LOGIN_SUCCESS
    result["img"] = img
    return jsonify(result)
def test_verify_captcha(code):
    # 获取session中的验证码
    s_code = session.get("code", None)
    print(code, s_code)
    if code != s_code:
        return False
    return True
@app.route("/resetPwd", methods=["POST"])
def reset_pwd():
    req = request
    str_req_data = req.data.decode('UTF-8')
    json_req_data = json.loads(str_req_data)
    pwd = json_req_data['pwd']
    pwd_new = json_req_data['pwdNew']
    username = json_req_data['user']
    pwd_md5 = pymysql_demo.encode_(pwd)
    pwd_new_md5 = pymysql_demo.encode_(pwd_new)
    update_pwd_sql = "update user set password=%s where userName=%s and password=%s"
    res = pymysql_demo.update_pwd(update_pwd_sql, [pwd_new_md5, username, pwd_md5])
    if res:
        return jsonify(response_result.PASSWORD_UPDATE_SUCCESS)
    else:
        return jsonify(response_result.PASSWORD_UPDATE_FAILURE)
@app.route('/updatePass', methods=["POST"])
def update_pass():
    req = request
    str_req_data = req.data.decode('UTF-8')
    json_req_data = json.loads(str_req_data)
    email = json_req_data['email']
    code = json_req_data['code']
    username = json_req_data['name']
    password = json_req_data['pwd']
    password_md5 = pymysql_demo.encode_(password)
    if code == session['email_code']:
        user_usertype_update_sql = "update user set password=%s where userName=%s and email=%s"
        res = pymysql_demo.update_pwd(user_usertype_update_sql, [password_md5, username, email])
        if res:
            return jsonify(response_result.PASSWORD_UPDATE_SUCCESS)
        else:
            return jsonify(response_result.PASSWORD_UPDATE_FAILURE)
    return jsonify(response_result.EMAIL_CODE_FAILURE)
@app.route('/historyRecord', methods=["GET"])
def get_history_record():
    username = request.args.get('username')
    print('username:', username)

    res = pymysql_demo.select_get_user_info([username])

    if res == False or res == '':
        return jsonify(response_result.USER_NOT_EXISTS)

    if res["usertype"] != 2:
        return jsonify(response_result.NO_PERMISSION)

    records = pymysql_demo.select_records()

    result = response_result.SUCCESS
    result["records"] = records

    return jsonify(result)

# @app.route('/downloadRes', methods=["GET"])
# def down_file(path):
#     response = make_response(flask.send_file(path))
#     response.headers["Content-Disposition"] = "attachment; filename={};".format(file_name)
#     return response


@app.route("/download/<fname>", methods=['GET'])
def download_file(fname):
    return send_from_directory(root+'data/tmp/res/', fname+'.zip', as_attachment=True)

if __name__ == '__main__':
    if(root!='/Users/oo/STUDY/STUDY/Postgraduate/papers/wordCl/'):
        app.run(host='0.0.0.0',port=443,ssl_context=(
            root+'ssl/7375998_meta-intell.tech.pem',
            root+'ssl/7375998_meta-intell.tech.key'))
        # app.run()
    else:
        # app.run(ssl_context=('ggl.pem', 'ggl.key'))
        # app.run(ssl_context=(root+'ssl/meta-intell.com_bundle.crt', root+'ssl/meta-intell.com.key'))
        app.run(ssl_context=(
            root+'ssl/7375998_meta-intell.tech.pem',
            root+'ssl/7375998_meta-intell.tech.key'))