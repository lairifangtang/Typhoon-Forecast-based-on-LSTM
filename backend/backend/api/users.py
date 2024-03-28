'''
@Project ：typhoon_dev
@File    ：users.py
@IDE     ：PyCharm
@Author  ：今天晚上吃啥啊
@Date    ：2023/7/10 9:42
'''
from flask import Blueprint, request, jsonify

from api.auth import blue_auth
from api.decorator import login_required, log_request
from utils import response
from utils.helper import get_id_type
from models.models import User, db

# 创建蓝图对象
blue_users = Blueprint('blue_users', __name__)


# 管理员查询用户列表
@blue_users.post('/users/user_list')
# @log_request
@login_required
def find_user():
    data = request.get_json()
    print(f"data{data}")
    account_id, isAdmin = get_id_type(data)

    # 如果用户不是管理员，拦截
    if not isAdmin:
        return jsonify({
            'msg': 'you are not admin,cannot use this api', 'success': False
        }), 403

    users = User.query.all()
    user_data = []
    for user in users:
        print(user)
        user_data.append({
            'account_id': user.account_id,
            'user_name': user.user_name,
            'isAdmin': user.isAdmin
        })

    if len(user_data) == 0:
        return jsonify({
            'msg': 'no user in database',
            'result': user_data,
            'success': False
        })

    return jsonify({
        'msg': 'quary users',
        'result': user_data,
        'success': True
    })


# 删除用户
@blue_users.post('/users/delete')
# @log_request
@login_required
def delete_user():
    data = request.get_json()
    print(f"data{data}")
    id_dist = data.get('id_dist')

    # 获取调用方的id,身份
    account_id, isAdmin = get_id_type(data)

    # 如果用户不是管理员
    if not isAdmin:
        return jsonify({
            'msg': 'you are not admin,cannot use this api', 'success': False
        }), 403

    # 查询要删除的用户是否存在
    user = User.query.filter_by(account_id=id_dist).first()
    print(f"删除用户：{user}")
    # 如果不存在
    if not user:
        return jsonify({
            "msg": "the account not exists",
            "result": {
                "id_dist": id_dist
            },
            "success": False
        }), 404

    # 不可以删除自己
    if int(user.account_id) == int(account_id):
        return jsonify({
            "msg": "you cannot delete yourself",
            "result": {
                "id_dist": id_dist
            },
            "success": False
        }), 403

    # 删除用户信息
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "msg": "用户信息删除成功",
        "result": {
            "id_dist": id_dist
        },
        "success": True
    })


# 修改用户名
@blue_users.post('/users/alter')
# @log_request
@login_required
def user_alter():
    data = request.get_json()
    print(f"data{data}".encode('utf-8'))
    account_id, isAdmin = get_id_type(data)

    new_username = data.get('new_user_name')
    id_dist = data.get('id_dist')

    # 如果用户不是管理员
    if not isAdmin:
        return jsonify({
            'msg': 'you are not admin,cannot use this api', 'success': False
        }), 403

    # 查询要修改的用户
    user = User.query.filter_by(account_id=id_dist).first()
    if not user:
        return jsonify({
            "msg": "the account not exists",
            "result": {
                "account_id": id_dist,
                'new_user_name': None
            },
            "success": False
        }), 404

    # 修改用户名
    user.user_name = new_username
    db.session.commit()

    return jsonify({
        'msg': "用户名修改成功",
        "result": {
            "account_id": id_dist,
            "new_user_name": new_username
        },
        "success": True
    })


# 查询是否为管理员
@blue_users.post("/users/isAdmin")
# @log_request
@login_required
def is_admin():
    data = request.get_json()
    print(f"data{data}")
    account_id = data.get('account_id')

    user = User.query.filter_by(account_id=account_id).first()

    if not user:
        return jsonify({
            'message': '查无此账户',
            'success': False,
            'isAdmin': None
        })

    return jsonify({
        'message': '查询身份成功',
        'success': True,
        'isAdmin': user.isAdmin
    })
