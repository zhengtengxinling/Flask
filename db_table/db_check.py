# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/13
# file:db_check.py
from db_table.db_setting import Login, db, Exam, Exam_Topic, Score


# 对进行cookie的用户进行匹配
def check(uid):
    user = Login.query.filter(Login.id == int(uid)).first()
    return user


# 检查用户名是否在数据库中,则可以判断该用户之前注册过
def username_check(username):
    ls = Login.query.filter(Login.username == username).all()
    # 以用户名进行参照
    # 如果用户存在数据库中，则返回False,如果不存在的话，则返回True，表示用户并不在数据库中
    if len(ls) == 0:
        return True
    else:
        return False


# 登录功能
def login_check(username, password, select):
    # 将查询的结果组成列表的形式，进行判断
    ls = Login.query.filter(Login.username == username,
                            Login.password == password, Login.value == select).all()
    flag = username_check(username)
    if select == '1' and len(ls) != 0:
        # 说明他是一个可以找到的学生
        return 3, None
    if select == '2' and len(ls) != 0:
        return 2, None
    if len(ls) == 0 and flag == False:
        return 1, '输入错误，请重新输入'
    if flag:
        return 0, "尚未注册，请注册"


# 注册功能
def register_check(username, password, phone, nickname, value=1):
    flag = username_check(username)
    # 判断用户名是否存在
    # 当flag为True的时候，表示用户不存在，则执行注册的操作，如果存在的话，则让他重新输入或者忘记密码
    if flag:
        user = Login()
        user.username = username
        user.password = password
        user.phone = phone
        user.value = value
        user.nickname = nickname
        db.session.add(user)
        db.session.commit()
        return True, "添加成功,请返回登录进行登录"
    else:
        # 表示用户存在的情况，返回False，并提示用户
        return False, '用户已存在'


# 忘记密码,验证码的验证可以不写入
def forget_check(username, password):
    # 判断用户的电话号码是否在数据库中，如果不在则让用户返回注册界面，如果存在才可以修改密码
    ls = Login.query.filter(Login.username == username).first()
    if ls == '':
        return False, '用户还未注册，请前往注册界面进行注册'
    else:
        Login.query.filter(Login.username == username).update({'password': password})
        return True, '用户密码修改成功'


#  个人信息的保存
def user_info_save(username, nickname, phone, password, choice, icon):
    # 需要判断用户是否想改个人信息,想改的话,则修改他的个人信息,不想改的话可以不改
    if nickname != '':
        Login.query.filter(Login.username == username).update({'nickname': nickname})
    if password != '':
        Login.query.filter(Login.username == username).update({'password': password})
    if len(phone) == 6:
        Login.query.filter(Login.username == username).update({'phone': phone})
    if choice is not None:
        Login.query.filter(Login.username == username).update({'Class': choice})
    Login.query.filter(Login.username == username).update({'icon': icon})

    return True, '修改成功'


# 对考试通知情况进行展示
def look_exam(student_class):
    # 先找到老师,再找到老师所带的班级和学生所在的班级一致的考试
    return Exam.query.filter(Exam.classroom == student_class).all()


def exam_paper(student_class):
    # 找到班级和相对于的考试，选择最后一个
    title = look_exam(student_class)[-1]
    print('title的数据是', title)
    # 找到和最后一个考试一样的时间
    start_time = title.start_time
    print('考试的开始时间', start_time)
    return Exam_Topic.query.filter(Exam_Topic.start_time == start_time).all()


# 对答案的检查
def exam_check(student_name, classroom,student_answer, answer,teacher):
    sum_score = 0
    student_score = 0
    # 因为答案和题目是一一对应的关系，所以可以一个个遍历和核对答案
    for i in range(len(answer)):
        if answer[i].type == '单选题' or answer[i].type == '多选题':
            student_answer[i] = student_answer[i].upper()
            if answer[i].answer == student_answer[i]:
                student_score += answer[i].score
        else:
            if student_answer[i] == answer[i].answer:
                student_score += answer[i].score
        # 将学生所获得分数和题目的总分数进行相加
        sum_score += answer[i].score
    # 将每次数据写入到数据库中
    # 需要的数据是id(主键)，学生姓名（username),学科(subject),分数（score),学科总分(sum_score),考试开始的时间（start_time)
    score = Score()
    score.username = student_name
    score.subject = answer[0].exam_subject
    score.sum_score = sum_score
    score.exam_time = answer[0].start_time
    score.student_score = student_score
    score.classroom=classroom
    score.maker=teacher
    db.session.add(score)
    db.session.commit()

# 对成绩的查询
def get_score(username):
    return Score.query.filter(Score.username==username).all()