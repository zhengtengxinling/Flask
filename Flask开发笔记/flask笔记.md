# flask开发

1、Flask介绍：
Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2。
Flask的基本模式为在程序里将一个视图函数分配给一个URL，每当用户访问这个URL时，系统就会执行给该URL分配好的视图函数，获取函数的返回值并将其显示到浏览器上，其工作过程见图。
![建立flask框架](C:\Users\踩着上帝的小丑\python\flaskProject1\Flask开发笔记\img.png)

# 2、Flask安装：

### 1、安装pycharm专业版

### 2、pychram自带Flask框架，新建项目选中Flask框架

### 3、如图

![img.png](C:\Users\踩着上帝的小丑\python\flaskProject1\Flask开发笔记\img_1.png)

### 4、如图

![img_1.png](C:\Users\踩着上帝的小丑\python\flaskProject1\Flask开发笔记\img_2.png)

###   3、Flask使用

Flask类只有一个必须指定的参数，即程序主模块或者包的名字，__name__是系统变量，该变量指的是本py文件的文件名 第二部分，路由和视图函数：

 客户端发送url给web服务器，web服务器将url转发给flask程序实例，程序实例。需要知道对于每一个url请求启动那一部分代码，所以保存了一个url和python函数的映射关系。处理url和函数之间关系的程序，称为路由。

用@app.route('/路由'）表示这是一个url地址，通过浏览器输入所对应的地址便可访问到该函数，return的返回值是展示在前端界面上。return返回的不只是字符串，也可以返回其他页面

![](C:\Users\踩着上帝的小丑\AppData\Roaming\Typora\typora-user-images\image-20220805114959622.png)

![image-20220805114916022](C:\Users\踩着上帝的小丑\AppData\Roaming\Typora\typora-user-images\image-20220805114916022.png)

### 1、render_template()：

render_template表示渲染，渲染前端页面，render_template('前端html页面',参数)

前端

```html
<html>
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<body>
    1234
    <div class="container">
        <div class="row">
            <div class="col-lg-9">
              欢迎进入这个页面
            </div>
        </div>
    </div>
</body>
</html>
```

后端：

```python
from flask import Flask
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('a.html')

if __name__ == "__main__":
    app.run()
```

如图![image-20220805115642901](C:\Users\踩着上帝的小丑\AppData\Roaming\Typora\typora-user-images\image-20220805115642901.png)

###  2、redirect()：

redirect表示跳转网页，后端会显示跳转302，302表示网页跳转，一般来说redirect跟url_for连接，实现页面跳转，当然直接输入url网址进行跳转。redirect('url地址')![image-20220805121908365](C:\Users\踩着上帝的小丑\AppData\Roaming\Typora\typora-user-images\image-20220805121908365.png)

### 3、url_for():

`url_for`: **url_for**的一个参数是一个视图函数的名字的字符串格式,后面的参数的参数以关键字的形式传递给`url`。 如果传递的参数在那个视图中url中定义了，那么这个参数就会以路径参数的形式给`url`。 如果传递的参数没有在`url`中定义，那么这些参数将会以查询字符串的形式放到`url`中。我们通常是通过`url`来查找函数，但当我们不知道`url`的时候，可以通过反向解析，通过`url_for`的形式，传入需要解析的函数来获取`url`

```python
from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    my_list_path = url_for('my_list', page=1, count=111)
    print(my_list_path)       # 结果为： /list/1/?count=111
    return my_list_path
@app.route('/list/<int:page>/')
def my_list(page):
    return '第 {} 页'.format(page)
```

### 4、response

response视图函数的返回值会自动转换为一个响应对象:

1. 如果返回的是一个字符串，那么flask会重新创建一个werkzeug，wrappers，Response对象，Response将该字符串作为主体，状态码为200，MIME的类型为text/html，然后返回该Response对象。
2. 如果返回的是一个元组，元组的数据类型是(response, status, headers).
   status的值会覆盖默认的200状态码，headers可以是一个列表和字典，作为额外的消息头。
3. 可以返回’Response‘及其子类。

### 5、 add_template_filter 有两种方法 :

​                                第一种:通过flask模块中的add_template_filter方法
​                                        a、定义函数，带有参数和返回值
​                                        b、添加过滤器 app.add_template_filter(function,name='')
​                                        c、在模板中使用：{{  变量 | 自定义过滤器}}
​                                :第二种：使用装饰器完成
​                                        a、定义函数，带有参数和返回值
​                                        b、通过装饰器完成@app.template_filter('过滤器名字')进行装饰器的修饰，进行绑定功能
​                                        c、在模板中使用：{{  变量 | 自定义过滤器}}

### 6、页面的继承，使用    {% block  %}   中间是可以修改的内容{% endblock %}

{% extends '页面.html' %}  继承模板原本的模型，原模板中所有的格式都会继承

### 7、{% include '页面.html''%}  包含 可以设置一个基本的模板，进行继承，相比之下

block更灵活，继承的范围小

### 8、link的使用，可以使用<link href="{{urt_for('static',filename="")}}>

### 9、宏：marco

​    1、把它看作一个jinjia2的一个函数，这个函数可以返回一个html字符串
​    2、目的：代码可以复用，避免代码冗余
​    使用方法：
​        1、在模板中直接定义：类似 ：macro1.html 中定义方法
​        2、将所有宏提提取到一个模板中：macro.html 导入方法：{% import 'macro.html' as xx %} {{   xxx.宏名字（参数）}}

### 10、{{%set%}}可以申明变量,全局变量   {% with get_flashed_messages as  %} {% endwith %}类似局部变量定义

{{ % import '' %}}   导入宏模块  {{ % include %}}   包含
![img.png](C:\Users\踩着上帝的小丑\python\flaskProject\笔记\img.png)

### 11、flask三大块：

    1、视图 (view)
        @app.route('/',endpoint='',methods=['GET,'POST'])
        def index():
            直接使用request
            return respone|''| render_template(‘’.html)
    2、模板 (template)
        查看6-9点
    3、模型 (model)
        数据库的连接和使用
        1、配置数据库的连接路径   mysql+pymysql://user:password@hostip:root//database_name
        SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:root@localhost:3306/flask
        2、创建包
            __init__.py 中添加
            db=SQLALchemy()             ------> 必须跟app联系
            def creat_app(app):
                return app

###  第三方库组件

1、数据库连接

下载Flask_SQLAlchemy

![img_1.png](C:\Users\踩着上帝的小丑\python\flaskProject\笔记\img_1.png)
![img_5.png](C:\Users\踩着上帝的小丑\python\flaskProject\笔记\img_2.png)
![img_3.png](C:\Users\踩着上帝的小丑\python\flaskProject\笔记\img_3.png)
![img_4.png](C:\Users\踩着上帝的小丑\python\flaskProject\笔记\img_4.png)
![img_6.png](C:\Users\踩着上帝的小丑\python\flaskProject\笔记\img_6.png)

 实例代码

```python
from flask import Flask  # 调用flask模块
from flask_migrate import Migrate,MigrateCommand
from flask_sqlalchemy import SQLAlchemy  # 调用flask和数据库连接的模块

app = Flask(__name__)
app.config['ENV'] = 'development'  # 配置开发者环境
# 数据库的连接和可视化
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager=Manager('db',MigrateCommand)

# ext.init_app(app)  # 将db对象和app进行关联
class User(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

user = User()
user.username="1234"
user.password="123"
db.session.add(user)
db.session.commit()
user1 = User.query.filter(User.username == '4' and User.password=='4').delete()
db.session.commit

@app.route('/')
def index():
    return '你好'

if __name__ == "__main__":
    # app.debug = True
    app.run(debug=True, use_reloader=False)
```

2、映射关系

下载Flask_Migrate,通过Flask_SQLAlchemy来实现对数据库的直接连接和操作，Flask_Migrate需要下载2.7.0版本，3.0.0+版本没有MigrateCommand，无法实现映射

![image-20220805144231892](C:\Users\踩着上帝的小丑\AppData\Roaming\Typora\typora-user-images\image-20220805144231892.png)

3、Flask实现前端表单的书写，需要下载Flask_wtform



后端代码

```python
from  flask import Flask,render_template,request,redirect
from wtforms.fields import simple
from wtforms import Form
from wtforms import validators
from wtforms import widgets
app = Flask(__name__,template_folder="templates")

class Myvalidators(object):
    '''自定义验证规则'''
    def __init__(self,message):
        self.message = message
    def __call__(self, form, field):
        print(field.data,"用户输入的信息")
        if field.data == "haiyan":
            return None
        raise validators.ValidationError(self.message)

class LoginForm(Form):
    '''Form'''
    name = simple.StringField(
        label="用户名",
        widget=widgets.TextInput(),
        validators=[
            Myvalidators(message="用户名必须是haiyan"),#也可以自定义正则
            validators.DataRequired(message="用户名不能为空"),
            validators.Length(max=8,min=3,message="用户名长度必须大于%(max)d且小于%(min)d")
        ],
        render_kw={"class":"form-control"}  #设置属性
    )

    pwd = simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="密码不能为空"),
            validators.Length(max=8,min=3,message="密码长度必须大于%(max)d且小于%(min)d"),
            validators.Regexp(regex="\d+",message="密码必须是数字"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class":"form-control"}
    )

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="GET":
        form = LoginForm()
        return render_template("a.html",form=form)
    else:
        form = LoginForm(formdata=request.form)
        if form.validate():
            print("用户提交的数据用过格式验证，值为：%s"%form.data)
            return "登录成功"
        else:
            print(form.errors,"错误信息")
        return render_template("a.html",form=form)


if __name__ == '__main__':
    # app.__call__()
    app.run(debug=True)

```

前端代码

```html
<body>
<form action="" method="post" novalidate>
    <p>{{ form.name.label }} {{ form.name }} {{ form.name.errors.0 }}</p>
    <p>{{ form.pwd.label }} {{ form.pwd }} {{ form.pwd.errors.0 }}</p>
    <input type="submit" value="提交">
</form>
</body>
```

4、resful 进行前后端分离 下载flask_resful

​	```

setting.py 配置文件

```
DEBUG=True
ENV='development'
# 设置数据库 连接的数据库，第三方库，数据库的用户名和密码，本机服务器，端口与好，数据库的名字
SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:root@localhost:3306/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

common.py

```
from flask import Flask
from user.model import *
import setting
from ext import db, api,cors
from user.view import user_bp


def const():
    app = Flask(__name__)
    # 将setting的配置加载到app上
    app.config.from_object(setting)
    # 将数据库和app连接
    db.init_app(app=app)
    api.init_app(app=app)
    # 进行跨域处理，关联到app上,supports_credentails支持当前的证书
    cors.init_app(app=app,supports_credentails=True)
    app.register_blueprint(user_bp)
    print(app.url_map)
    return app
```

app.py 主程序应用

```
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from common import const
from ext import db

app = const()
# 导入manager
manager = Manager(app=app)
# 导入数据库和app的关系
migrate = Migrate(app=app, db=db)
manager.add_command('db',MigrateCommand)

@app.route('/')
def index():
    return '大家好'
if __name__ == '__main__':
    manager.run()
```

model.py 数据库建立

```python
from ext import  db
# 定义数据库内容
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    isdelete=db.Column(db.Boolean())
```





view.py 可视化文件

```
# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/8/3
# file:view.py
from flask import Blueprint

from flask_restful import Resource, fields, marshal_with, reqparse, inputs

from ext import api
from user.model import User

user_bp = Blueprint('user', __name__, url_prefix='/user')


# 对前端展示的数据进行修改
class fun(fields.Raw):
    def format(self, value):
        print('----------------->', value)
        return '存在' if value else '不存在'


user_list = {
    'id': fields.Integer,
    'name': fields.String(attribute='username'),
    'bool': fields.Boolean(attribute='isdelete'),
    '判断': fun(attribute='isdelete'),
    'password': fields.String
}
user_list1 = {
    'id': fields.Integer,
    'username': fields.String,
    'URi': fields.Url('signle_user', absolute=True)
}
# 参数解析
parse = reqparse.RequestParser()
# 表示类型，必须输入，如果报错啦给一个提示,location可以设置postman的位置location=['form']限制是post请求
parse.add_argument('username', type=str, required=True, help='必须输入用户名')
# 对密码添加正则表达式
parse.add_argument('password', type=inputs.regex(r'^\d{6,12}$'), required=True, help='必须输入密码')
# 可以实现复选框
parse.add_argument('hobby', action='append')
# marshal 可以进行套迭，marshal(数据，模板（例如，user_list）)
# 传值给后端
class student(Resource):
    @marshal_with(user_list1)  # 将不是序列化的对象转为序列化对象
    def get(self):
        user = User.query.all()

        return user

    @marshal_with(user_list1)  # 将不是序列化的对象转为序列化对象
    def post(self):
        # 获取前端给的值
        args = parse.parse_args()
        username = args.get('username')
        password = args.get('password')
        hobby = args.get('hobby')
        print(hobby)
        user = User()
        user.username = username
        user.password = password
        return user


class student1(Resource):
    @marshal_with(user_list)
    def get(self, id):
        print('-------------------->data', id)
        user = User.query.get(id)
        return user

    def post(self):
        return {'------------------->': 'student1_post'}

# 对路由进行修改便可以查找具体的值
api.add_resource(student, '/student/', endpoint='all_user')
api.add_resource(student1, '/student/<int:id>', endpoint='signle_user')

```

