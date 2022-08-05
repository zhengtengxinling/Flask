# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/11
# file:login.py
from flask import render_template, request, make_response, session, Blueprint, redirect, url_for, jsonify, flash
from io import BytesIO
# 导入Flask模块，进行实体化
from db_table.db_check import login_check, register_check, forget_check
from db_table.db_setting import Login
from static.Login.identify_check import random_pic

login_bp = Blueprint('Login', __name__)


# 登录界面
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    # p判断是post请求还是get请求
    if request.method == 'POST':
        username = request.form.get('login_username')
        password = request.form.get('login_password')
        select = request.values.get('select')
        # 设置cookie
        ls = Login.query.filter(Login.username == username,
                                Login.password == password,Login.value== select).first()
        if password != '' and username != '' and select != '':
            flag, msg = login_check(username, password, select)
            if flag == 3:
                # 给cookie传一个参数，当有这个参数跳转，没有就返回登录界面
                response = redirect(url_for('user.user_base'))
                response.set_cookie('uid', str(ls.id), max_age=1800)
                return response
            elif flag == 2:
                response = redirect(url_for('Manager.manager_base'))
                response.set_cookie('uid', str(ls.id), max_age=1800)
                return response
            elif flag == 1:
                flash('密码输入错误,请重新输入')
                return render_template('Login/login.html')
            else:
                return render_template('Login/login.html', msg=msg)
    return render_template('Login/login.html')


# 注册界面
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 判断请求是post请求还是get请求
    if request.method == 'POST':
        username = request.form.get('register_username')
        password = request.form.get('register_password')
        repassword = request.form.get('register_repassword')
        nickname= request.form.get('register_nickname')
        phone = request.form.get('register_phone')
        # 将数据放在后端与数据库进行匹配
        if repassword == password and username != '' and phone != '' \
                and password != '' and len(phone) == 6:
            flag, msg = register_check(username, password, phone,nickname)
            if flag:
                return render_template('Login/register.html', msg=msg)
            else:
                return render_template('Login/register.html', msg=msg)
    return render_template('Login/register.html')


# 忘记密码界面
@login_bp.route('/forget', methods=['GET', 'POST'])
def get_secret():
    if request.method == 'POST':
        # 从输入框中获取电话号码，密码和验证码
        name = request.form.get('forget_name')
        password = request.form.get('forget_password')
        input_code = request.form.get('forget_code')
        # 获取session中的验证码与输入框中的验证码进行比较
        code = session.get('valid')
        # 出现的情况: 用户名的电话号码不存在，电话号码存在，判断验证码是否正确
        # 如果验证码不相同，则重新输入验证码
        if name !='' and password != '' and code.lower() != input_code.lower() and input_code != '':
            msg = '验证码错误，请重新输入验证码'
            return render_template('Login/forget_secret.html', msg=msg)
        # 如果验证码相同,电话号码输入正确，而且密码的值不为空
        elif code.lower() == input_code.lower() and name!='' and password != '':
            flag, msg = forget_check(name, password)
            if flag:
                return render_template('Login/forget_secret.html', msg=msg)
            else:
                return render_template('Login/forget_secret.html', msg=msg)
    return render_template('Login/forget_secret.html')


# 添加验证照片的功能
@login_bp.route('/image')
def image():
    # 返回的值一个是img照片，一个是验证码的结果
    img, code = random_pic()
    #  把照片转换二进制
    buttfer = BytesIO()
    # 将照片保存
    img.save(buttfer, 'JPEG')
    # 将code的数据保存在session中
    session['valid'] = code
    buttfer_save = buttfer.getvalue()
    response = make_response(buttfer_save)
    response.headers['Content-Type'] = 'image/jpg'
    return response


@login_bp.route('/out')
def out():
    flash('已经退出')
    response = redirect(url_for('Login.login'))
    response.delete_cookie('uid')
    return response
