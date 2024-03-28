'''
@Project ：typhoon_dev 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：今天晚上吃啥啊
@Date    ：2023/7/10 10:15
'''
from gevent import pywsgi
from wsgiref.simple_server import make_server
from werkzeug.serving import run_simple
import settings
from models.models import db
from api import typhoon_info, users, auth, logs,typhoon_predict
from flask import Flask
from flask_cors import CORS

# 创建Flask应用对象
app = Flask(__name__)
CORS(app, supports_credentials=True)
# 从配置对象加载配置到应用程序
app.config.from_object(settings.Config)

# 将models模块的db对象连接上app（数据库关联）
db.init_app(app)

# app应用蓝图
app.register_blueprint(auth.blue_auth)
app.register_blueprint(users.blue_users)
app.register_blueprint(typhoon_info.blue_typhoon_model)
app.register_blueprint(logs.blue_logs)
app.register_blueprint(typhoon_predict.blue_typhoon_predict)

if __name__ == '__main__':
    httpserver = pywsgi.WSGIServer('0.0.0.0', 8080, app)
    #WSGIServer(('0.0.0.0', 8080), app)
    httpserver.serve_forever()
    # run_simple('127.0.0.1', 8080, app)
    # server = make_server('127.0.0.1', 8080, app)
    # server.serve_forever()
#
# with app.app_context():
#     # 清空数据库表
#     db.drop_all()
#     # 根据模型类创建数据库表
#     db.create_all()
