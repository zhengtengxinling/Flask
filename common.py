# -*- encoding:utf-8 -*-
# editor:踩着上帝的小丑
# time:2022/7/13
# file:common.py
import os
from flask import Flask
from flask_migrate import MigrateCommand

from conf import settings
from db_table.db_setting import db
from static.Login.login import login_bp
from static.Manager.manager import teacher_bp
from static.User.user import user_bp


def construct():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config['SECRET_KEY '] = os.urandom(24)
    # 连接蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(teacher_bp)
    # 数据库连接
    db.init_app(app)

    return app
