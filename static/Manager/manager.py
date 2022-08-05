# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/20
# file:Manager.py
import os
import random
from flask import Blueprint, render_template, request, redirect, url_for

from werkzeug.utils import secure_filename

from db_table.db_check import check
from db_table.db_manager import manager_info_save, send_tell_save, paper_check, add_content, exam_select, \
    make_paper_random, make_paper_subject, make_paper_hand, view
from db_table.db_setting import Score, Exam_Topic

teacher_bp = Blueprint('Manager', __name__, url_prefix='/Manager')

base_file = os.path.dirname(os.path.dirname(__file__))
icon_base_path = os.path.join(base_file, 'icon')
pic_log = ['gif', 'png', 'jpg', 'jpeg']


# 管理员的主页
@teacher_bp.route('/', methods=['POST', 'GET'])
def manager_base():
    # 判断是否存在这个用户，存在的话，才可以展示
    uid = request.cookies.get('uid', None)
    print(uid)
    if uid:
        info = check(uid)
        if request.method == 'POST':
            content = request.form.get('info_send')
            print(content != '')
            if content is not None:
                if content != '':
                    ls = send_tell_save(content, int(uid))
                    return render_template('teacher/manager_base.html', user=info, msg=ls[1])
                else:
                    return render_template('teacher/manager_base.html', user=info)
            else:
                return render_template('teacher/manager_base.html', user=info)
        # 如果是get请求，就表示展示的页面
        else:
            return render_template('teacher/manager_base.html', user=info)
    return render_template('Login/login.html')


# 管理员的修改个人信息页面
@teacher_bp.route('/info', methods=['POST', 'GET'])
def manager_info():
    uid = request.cookies.get('uid', None)
    info = check(uid)
    if uid:
        if request.method == 'POST':
            nickname = request.form.get('rev_nickname')
            phone = request.form.get('rev_phone')
            password = request.form.get('rev_secret')
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
                    flag, msg = manager_info_save(info.username, nickname, phone, password, icon_pic)
                    if flag:
                        return render_template('teacher/manager_info.html', user=info, msg=msg)
                else:
                    return render_template('teacher/manager_info.html', user=info, msg='照片的格式不符合，请重新输入')
            else:
                manager_info_save(info.username, nickname, phone, password, info.icon)
        return render_template('teacher/manager_info.html', user=info)
    return render_template('teacher/manager_info.html')


# 试题管理功能
@teacher_bp.route('/paper')
def manager_paper():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        print(info)
        # 获取select框中的数据
        content_type = request.args.get('select')
        flag, msg = paper_check(info.username, content_type)
        ls = ['多选题', '单选题', '填空题']
        s = {}
        sum_type=0
        print(flag)
        if flag:
            for i in msg:
                if i.type not in ls:
                    s[i.type] = 0
                else:
                    s[i.type] = 1
            sum_type = len(s.keys())
        return render_template('teacher/manager_paper.html',info=info,user=msg, paper_sum=sum_type)
    return redirect(url_for('user.user_base'))


# 增加试题的功能
@teacher_bp.route('/add_paper', methods=['POST', 'GET'])
def add_paper():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        if request.method == 'POST':
            # 将从前端获得的数据转为后端的数据
            # 题目的类型，题目，题目的正确答案，ABCD四个选项
            paper_type = request.form.get('select')
            paper_content = request.form.get('content')
            select_A = request.form.get('input_A')
            select_B = request.form.get('input_B')
            select_C = request.form.get('input_C')
            select_D = request.form.get('input_D')
            answer = request.form.get('answer').upper()
            if paper_type != 'all' and paper_content != '' and answer != '':
                ls = add_content(paper_content, paper_type, select_A, select_B, select_C, select_D, answer,
                                 info.username)
                if ls[0]:
                    return render_template('teacher/add_paper.html', user=info, msg=ls[1])
            else:
                return render_template('teacher/add_paper.html', user=info)
        else:
            return render_template('teacher/add_paper.html', user=info)
    return redirect(url_for('user.user_base'))


# 考试的功能
@teacher_bp.route('/exam')
def manager_exam():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        select_subject = request.args.get('select_subject')
        if select_subject != '':
            flag, msg = exam_select(select_subject)
            print(flag, msg)
            if flag:
                return render_template('teacher/manager_exam.html', user=info, exam=msg)
            else:
                return render_template('teacher/manager_exam.html', user=info, msg=msg)
        else:
            return render_template('teacher/manager_exam.html', user=info, exam=info.exam)
    return redirect(url_for('user.user_base'))


@teacher_bp.route('/exam/make_paper', methods=['POST', 'GET'])
def make_paper():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        print(info)
        if request.method == 'POST':
            # 获取生成数据的一系列值
            exam_name = request.form.get('subject')
            classroom = request.form.get('classroom')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            single_geshu = request.form.get('single_geshu')
            single_score = request.form.get('single_score')
            double_geshu = request.form.get('double_geshu')
            double_score = request.form.get('double_score')
            tiankong_geshu = request.form.get('tiankong_geshu')
            tiankong_score = request.form.get('tiankong_score')
            # 设计三个数组，进行存放不同类型的题目，单选题，多选题，填空题
            single, double, tiankong = [], [], []
            for user in info.paper:
                if user.type == '填空题':
                    tiankong.append(user)
                elif user.type == '单选题':
                    single.append(user)
                elif user.type == '多选题':
                    double.append(user)
            # 将数据导入数据库中
            # 判断数据是否为空，如果数据不为空的话，将考试时间的信息写入数据库中，将考试卷写在数据库中
            if exam_name != '' and classroom != '' and start_time != '' \
                    and end_time != '' and single_score != '' and single_geshu != '' \
                    and double_geshu != '' and double_score != '' and tiankong_score != '' and tiankong_geshu != '':
                # 随机生成题目
                single = random.sample(single, int(single_geshu))
                double = random.sample(double, int(double_geshu))
                tiankong = random.sample(tiankong, int(tiankong_geshu))
                # 将input时间进行格式化，将input时间中的T改为空格
                start_time = start_time.replace('T', ' ')
                end_time = end_time.replace('T', ' ')
                # 将考试的通知写入数据库
                make_paper_random(start_time, end_time, info.username, exam_name, classroom)
                # 将考试的题目写入数据库
                make_paper_subject(single, single_score, double, double_score, tiankong,
                                   tiankong_score, exam_name, start_time)
                return redirect(url_for('Manager.paper'))
            else:
                return render_template('teacher/make_paper_ramdon.html', user=info)
        else:
            return render_template('teacher/make_paper_ramdon.html', user=info)
    return redirect(url_for('user.user_base'))


# 手动出试卷的流程
@teacher_bp.route('/exam/hand_paper', methods=['POST', 'GET'])
def hand_paper():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        # 获取题库的需要
        paper = request.args.getlist('checkbox')
        # 获取其他的信息
        subject = request.args.get('subject')
        classroom = request.args.get('classroom')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        single_score = request.args.get('single_score')
        double_score = request.args.get('double_score')
        tiankong_score = request.args.get('tiankong_score')
        print(paper, subject, classroom, start_time, end_time, single_score, double_score, tiankong_score)
        # 对数据进行处理
        if subject != '' and classroom != '' and start_time != '' and end_time != '' \
                and single_score != '' and double_score != '' and tiankong_score != '' and len(paper) != 0:
            # 将时间进行格式化
            start_time = start_time.replace('T', ' ')
            end_time = end_time.replace('T', ' ')
            # 将考试的通知写入数据库
            make_paper_random(start_time, end_time, info.username, subject, classroom)
            # 将选中的题库写进数据库中
            flag, msg = make_paper_hand(paper, subject, single_score, double_score, tiankong_score, start_time)
            if flag:
                return redirect(url_for('Manager.paper'))
        else:
            return render_template('teacher/hand_paper.html', user=info)
    return redirect(url_for('user.user_base'))


# 生成试卷
@teacher_bp.route('/creat_paper')
def paper():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        start_time=info.exam[-1].start_time
        exam=Exam_Topic.query.filter(Exam_Topic.start_time==start_time).all()
        return render_template('teacher/paper.html', user=info,exam=exam)
    return redirect(url_for('user.user_base'))


# 对学生成绩的查看
@teacher_bp.route('/student_score')
def student_score():
    uid = request.cookies.get('uid', None)
    if uid:
        info = check(uid)
        score = view(info.username)
        select_type = request.args.get('select')
        if select_type != '':
            # 当查询的班级存在的时候，则显示查询的班级，不存在的时候，则显示全部
            score1 = Score.query.filter(Score.classroom == select_type).all()
            if score1 != '':
                return render_template('teacher/look_score.html', user=info, score=score1)
        return render_template('teacher/look_score.html', user=info, score=score)
    return redirect(url_for('user.user_base'))
