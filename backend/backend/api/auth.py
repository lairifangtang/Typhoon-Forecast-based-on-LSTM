'''
@Project ：typhoon_dev
@File    ：auth.py
@IDE     ：PyCharm
@Author  ：今天晚上吃啥啊
@Date    ：2023/7/10 10:50
'''
# 登录注册
import sys

from flask import Blueprint, request, make_response, jsonify
from api.decorator import login_required, log_request
from utils.helper import generate_unique_account_id
from models.models import User, db
from utils.response import get_register_login_response, get_error_response
import hashlib
import string
import random

# 创建蓝图对象
blue_auth = Blueprint('blue_auth', __name__)


def password_salt(password, salt):
    obj = hashlib.md5(salt.encode("utf-8"))
    obj.update(password.encode("utf-8"))
    secret = obj.hexdigest()

    return secret


@blue_auth.post('/login')
# @log_request
def login_request():
    data = request.get_json()
    print(f"data{data}")
    account_id = data.get('account_id')
    password = data.get('password')

    # 用户ID或密码为空
    if account_id is None or password is None:
        return get_error_response('用户ID或密码为空 account_id or password is null')

    # 查找指定用户
    user = User.query.filter_by(account_id=account_id).first()

    # account_id不存在
    if not user:
        return get_error_response("用户ID不存在 account_id not exist")

    # 错误密码
    pwd = password_salt(password=password, salt=user.salt)
    if user.password != pwd:
        return get_error_response("错误密码 wrong password")

    data = {
        'msg': "登录成功 Login Successfully",
        'result': {
            'account_id': account_id,
            'user_name': user.user_name,
            'isAdmin': user.isAdmin
        },
        'cookie': {
            'account_id': account_id,
            'isAdmin': user.isAdmin
        },
        'success': True
    }
    return jsonify(data)


# 注册接口
# 向数据库增加用户
@blue_auth.post('/register')
# @log_request
def register_request():
    data = request.get_json()
    print(f"data{data}")
    user_name = data.get('user_name')
    password = data.get('password')

    if user_name is None or password is None:
        return get_register_login_response(False, "用户名或密码为空 name or password is null", user_name, None, None)

    characters = string.ascii_letters + string.digits
    salt = ''.join(random.SystemRandom().choice(characters) for _ in range(8))

    pwd = password_salt(password=password, salt=salt)

    try:
        # 获得随机生成的不与之前重复的用户ID
        account_id = generate_unique_account_id()

        # 创建用户对象
        user = User(user_name=user_name, account_id=account_id, password=pwd, salt=salt)

        # 添加用户到会话
        db.session.add(user)

        # 提交会话
        db.session.commit()

    except:
        # 发生异常时回滚事务
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        raise

    return get_register_login_response(True, "注册成功 register successfully", user_name, False, account_id)


# 退出登录，删除cookie
@blue_auth.post("/logout")
# @log_request
@login_required
def delete_cookie():
    # todo 退出登录 接口文档+response函数+视图函数
    resp = make_response("del success")
    # 删除cookie
    resp.delete_cookie("Name1")
    return resp
