from flask import Blueprint, request, jsonify
from api.decorator import log_request, login_required
from models.models import ActionLogs, db
from utils.helper import get_id_type

# 创建蓝图对象
blue_logs = Blueprint('blue_logs', __name__)


@blue_logs.post('/logs/search')
@login_required
# @log_request
def log_list():
    data = request.get_json()
    print(f"data{data}")
    account_id, isAdmin = get_id_type(data)

    # 检索所有的logs
    logs = ActionLogs.query.all()
    logs_data = []

    for log in logs:
        print(f"正在检索log:{log}")
        if int(account_id) == int(log.account_id):
            logs_data.append({
                'ty_name': log.ty_name,
                'act_time': log.act_time,
                'op_type': log.op_type,
                'op_details': log.op_details
            })
    if len(logs_data) == 0:
        return jsonify({
            'msg': 'no logs in database',
            'result': None,
            'success': True
        })

    return jsonify({
        'msg': 'ohhhhh',
        'result': logs_data,
        'success': True
    })


@blue_logs.post('/logs/clear')
@login_required
@log_request
def log_clear():
    data = request.get_json()
    print(f"data{data}")
    account_id, isAdmin = get_id_type(data)

    logs = ActionLogs.query.all()

    for log in logs:
        if int(log.account_id) == int(account_id):
            db.session.delete(log)
            db.session.commit()

    return jsonify({
        'msg': 'ohhhhhh',
        'success': True
    })
