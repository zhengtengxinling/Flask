# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/11
# file:settings.py
# 配置为开发者环境
ENV = 'development'
DEBUG = True
# 设计密钥
SECRET_KEY = 'add'
BOOTSTRAP_SERVE_LOCAL = True
# 数据库的连接
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flask"
SQLALCHEMY_TRACK_MODIFICATIONS = False
