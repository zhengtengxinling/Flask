# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/13
# file:db_setting.py
from flask_sqlalchemy import *  # 调用flask和数据库连接的模块

db = SQLAlchemy()

"""
建立登录的信息
建表的内容：用户名，密码，身份（学生或者是老师),电话号码，别称,班级,头像的处理
需要对用户名设置为唯一性，对电话号码设置唯一性
"""


class Login(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    Class = db.Column(db.String(255), nullable=True)
    icon = db.Column(db.String(255), nullable=True)
    send_tell = db.relationship('Send_Tell', backref='student')
    paper = db.relationship('Paper', backref='student')
    exam = db.relationship('Exam', backref='student')



"""
发送通知
建表的内容：序号id，时间time，内容content
"""


class Send_Tell(db.Model):
    __tablename__ = 'send_tell'
    num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 跟Login中进行关联，关联之后的结果可以获取username
    content = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False,
                     default=(time.strftime('%Y-%m-%d %H:%M:%S'), time.localtime())[0])
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


"""
题库的内容
建表内容：序号id,题目paper_content,出卷老师teacher, 类型type,a,b,c,d四个选项，正确选项answer,用一个框里面的进行判断
"""


class Paper(db.Model):
    __tablename__ = 'paper'
    paper_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paper_content = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    select_A = db.Column(db.String(255), nullable=True)
    select_B = db.Column(db.String(255), nullable=True)
    select_C = db.Column(db.String(255), nullable=True)
    select_D = db.Column(db.String(255), nullable=True)
    answer = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), db.ForeignKey('student.username'), nullable=False)


"""
考试安排的内容
建表内容：序号id（主键）,出卷老师teacher,考试开始时间start_time,考试结束时间end_time,考试科目exam_name
"""


class Exam(db.Model):
    __tablename__ = 'exam'
    exam_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    exam_name = db.Column(db.String(255), nullable=False)
    classroom = db.Column(db.String(255), nullable=False)
    exam_topic = db.relationship('Exam_Topic', backref='exam')
    teacher = db.Column(db.String(255), db.ForeignKey('student.username'), nullable=False)

"""
考试题库的内容
建表内容：序号id（主键），出卷的题目topic（和题库中的数据库差不多），考试科目的名字（exma_name)和考试安排进行连接
通过考试科目可以找到名称
"""


class Exam_Topic(db.Model):
    __tablename__ = 'exam_topic'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paper_content = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    select_A = db.Column(db.String(255), nullable=True)
    select_B = db.Column(db.String(255), nullable=True)
    select_C = db.Column(db.String(255), nullable=True)
    select_D = db.Column(db.String(255), nullable=True)
    answer = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    exam_subject = db.Column(db.String(255), db.ForeignKey('exam.start_time'), nullable=False)


"""
建学生成绩的表
建表内容：序号id(主键)，学生姓名（username),学科(subject),分数（score),学科总分(sum_score),考试开始的时间（start_time)
"""


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    exam_time = db.Column(db.DateTime, nullable=False)
    student_score = db.Column(db.String(255), nullable=True)
    sum_score = db.Column(db.String(255), nullable=False)
    classroom=db.Column(db.String(255),nullable=False)
    maker = db.Column(db.String(255), nullable=False)

