# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/20
# file:db_manager.py
from db_table.db_setting import Login, Send_Tell, db, Paper, Exam, Exam_Topic, Score


# 修改管理者的信息
def manager_info_save(username, nickname, phone, password, icon):
    if nickname != '':
        Login.query.filter(Login.username == username).update({'nickname': nickname})
    if password != '':
        Login.query.filter(Login.username == username).update({'password': password})
    if len(phone) == 6:
        Login.query.filter(Login.username == username).update({'phone': phone})
    Login.query.filter(Login.username == username).update({'icon': icon})
    return True, '修改成功'


# 对管理者所发布的消息写入
def send_tell_save(content, manager_id):
    manager = Send_Tell()
    manager.content = content
    manager.user_id = manager_id
    db.session.add(manager)
    db.session.commit()
    return True, '发送成功'


# 对管理者所设计的试题进行查看
def paper_check(username, paper_type):
    print(username,paper_type)
    # 如果查询成功的话，则返回查询出来的数据，如果查询不成功的话，则表示选择项为all，则选择所有的类型
    user = Paper.query.filter(Paper.type == paper_type, Paper.name == username).all()
    if user:
        return True, user
    else:
        user = Paper.query.filter(Paper.name==username).all()
        return False, user


# 对增加题库的实现
def add_content(paper_content, paper_type, select_A, select_B, select_C, select_D, answer, name):
    paper = Paper()
    paper.paper_content = paper_content
    paper.type = paper_type
    paper.select_A = select_A
    paper.select_B = select_B
    paper.select_C = select_C
    paper.select_D = select_D
    paper.answer = answer
    paper.name = name
    db.session.add(paper)
    db.session.commit()
    return 'True','添加成功'


# 对题库的查询
def exam_select(select):
    info = Exam.query.filter(Exam.exam_name == select).all()
    if info:
        return True, info
    else:
        return False, '查无结果'


# 对自动生成试卷
def make_paper_random(start_time, end_time, name, topic, classroom):
    exam = Exam()
    exam.start_time = start_time
    exam.end_time = end_time
    exam.teacher = name
    exam.exam_name = topic
    exam.classroom = classroom
    db.session.add(exam)
    db.session.commit()
    return True


def make_paper_subject(single, single_score, double, double_score, tiankong, tiankong_score, exam_name, start_time):
    # 将单选题的数据写入数据库
    for single_1 in single:
        exam_topic = Exam_Topic()
        exam_topic.paper_content = single_1.paper_content
        exam_topic.type = single_1.type
        exam_topic.score = single_score
        exam_topic.select_A = single_1.select_A
        exam_topic.select_B = single_1.select_B
        exam_topic.select_C = single_1.select_C
        exam_topic.select_D = single_1.select_D
        exam_topic.answer = single_1.answer
        exam_topic.exam_subject = exam_name
        exam_topic.start_time = start_time
        db.session.add(exam_topic)
        db.session.commit()
    # 将多选题的数据写入数据库
    for double_1 in double:
        exam_topic = Exam_Topic()
        exam_topic.paper_content = double_1.paper_content
        exam_topic.type = double_1.type
        exam_topic.score = double_score
        exam_topic.select_A = double_1.select_A
        exam_topic.select_B = double_1.select_B
        exam_topic.select_C = double_1.select_C
        exam_topic.select_D = double_1.select_D
        exam_topic.answer = double_1.answer
        exam_topic.exam_subject = exam_name
        exam_topic.start_time = start_time
        db.session.add(exam_topic)
        db.session.commit()
    # 将填空题的数据写入数据库
    for tiankong_1 in tiankong:
        exam_topic = Exam_Topic()
        exam_topic.paper_content = tiankong_1.paper_content
        exam_topic.type = tiankong_1.type
        exam_topic.score = tiankong_score
        exam_topic.select_A = tiankong_1.select_A
        exam_topic.select_B = tiankong_1.select_B
        exam_topic.select_C = tiankong_1.select_C
        exam_topic.select_D = tiankong_1.select_D
        exam_topic.answer = tiankong_1.answer
        exam_topic.exam_subject = exam_name
        exam_topic.start_time=start_time
        db.session.add(exam_topic)
        db.session.commit()

# 手动生成试卷和题库
def make_paper_hand(data, subject, single_score, double_score, tiankong_score, start_time):
    for i in data:
        t = Paper.query.filter(Paper.paper_id == int(i)).first()
        exam_topic = Exam_Topic()
        exam_topic.paper_content = t.paper_content
        exam_topic.type = t.type
        exam_topic.select_A = t.select_A
        exam_topic.select_B = t.select_B
        exam_topic.select_C = t.select_C
        exam_topic.select_D = t.select_D
        exam_topic.answer = t.answer
        exam_topic.exam_subject = subject
        exam_topic.start_time = start_time
        if t.type == '填空题':
            exam_topic.score = tiankong_score
        elif t.type == '单选题':
            exam_topic.score = single_score
        elif t.type == '多选题':
            exam_topic.score = double_score
        db.session.add(exam_topic)
        db.session.commit()
    return True,'试卷生成完成'

def view(name):
     return Score.query.filter(Score.maker==name).all()

