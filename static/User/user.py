# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/15
# file:User_view.py
import os
from flask import render_template, Blueprint, request, redirect, url_for

from werkzeug.utils import secure_filename

from db_table.db_check import user_info_save, check, look_exam, exam_paper, exam_check, get_score
from db_table.db_setting import Login

user_bp = Blueprint('user', __name__, url_prefix='/user')
base_file = os.path.dirname(os.path.dirname(__file__))
icon_base_path = os.path.join(base_file, 'icon')
pic_log = ['gif', 'png', 'jpg', 'jpeg']


# 用户的首页
@user_bp.route('/')
def user_base():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        tell = Login.query.filter(Login.value == '2').all()
        return render_template('User/user_base.html', user=info, talks=tell)
    else:
        msg = '用户还未登录，无法进入主页面'
        return render_template('Login/login.html', msg=msg)


# 用户的个人信息界面
@user_bp.route('/info', methods=['GET', 'POST'])
def user_info():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        if request.method == 'POST':
            nickname = request.form.get('rev_nickname')
            phone = request.form.get('rev_phone')
            password = request.form.get('rev_secret')
            choice = request.values.get("select")
            # 两个属性，一个是文件的名字，一个是文件的类型
            icon = request.files.get('icon')
            # 获取icon中的文字属性
            icon_name = icon.filename
            suffix = icon_name.rsplit('.')[-1]
            # 当照片为空时，则保留之前的照片，当照片不空时，对他进行修改
            if icon_name != '':
                if suffix in pic_log:
                    icon_name = secure_filename(icon_name)  # 对文件进行python的合理命名
                    icon_path = os.path.join(icon_base_path, icon_name)
                    icon.save(icon_path)
                    icon_pic = os.path.join('icon/', icon_name)
                    flag, msg = user_info_save(info.username, nickname, phone, password, choice, icon_pic)
                    if flag:
                        return render_template('User/user_info.html', user=info, msg=msg)
                else:
                    return render_template('User/user_info.html', user=info, msg='照片的格式不符合，请重新输入')
            else:
                user_info_save(info.username, nickname, phone, password, choice, info.icon)
        return render_template('User/user_info.html', user=info)
    return redirect(url_for('user.user_info'))


# 进行考试页面的展示
@user_bp.route('/look_paper')
def look_paper():
    uid = request.cookies.get('uid', None)
    if uid:
        # 获得自己的账号
        info = check(uid)
        # 需要知道自己所属的班级，查到老师所带的班级，才可以查到有关这个班级的考试
        exam = look_exam(info.Class)
        return render_template('User/look_paper.html', user=info, exam_info=exam)
    return redirect(url_for('user.user_info'))


# 进入考试界面
@user_bp.route('/exam', methods=['POST', 'GET'])
def exam():
    uid = request.cookies.get('uid', None)
    if uid:
        # 获得自己的账号
        info = check(uid)
        # 找到跟他一个班的所有考试，并且获得最近一次考试的考试时间
        exam1 = look_exam(info.Class)[-1]
        exam_time = exam1.end_time - exam1.start_time
        exam_topic = exam_paper(info.Class)
        # 将静态页面，没有提交的数据进行展示，并对提交的数据进行判读那
        if request.method == 'POST':
            # 获取的所有的答案，并且将这些答案和数据库中的题目进行对比
            answer = request.form.getlist('student_answer')
            exam_check(info.username,info.Class, answer, exam_topic,exam1.teacher)
            return render_template('User/exam.html', user=info, exam=exam1, exam_info=exam_topic, time=exam_time)
        # 提交之后的选项
        return render_template('User/exam.html', user=info, exam=exam1, exam_info=exam_topic, time=exam_time)
    return redirect(url_for('user.user_info'))

# 查看成绩的界面
@user_bp.route('score')
def look_score():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        # 获取学生的成绩
        student_score=get_score(info.username)
        return render_template('User/score.html', user=info,score=student_score)
    return redirect(url_for('user.user_info'))
