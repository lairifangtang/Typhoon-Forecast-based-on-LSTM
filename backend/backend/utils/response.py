"""
文件功能：提供了获得json的函数，将被用在返回数据
"""
from flask import make_response, jsonify
import json


def get_error_response(msg):
    return jsonify({
        'msg': msg,
        'success': False
    })


def get_register_login_response(success, msg, user_name, isAdmin=False, account_id=-1):
    data = {
        'msg': msg,
        'result': {
            'account_id': account_id,
            'user_name': user_name,
            'isAdmin': isAdmin
        },
        ''
        'success': success
    }
    # 将python数据字典转换为json
    response = make_response(json.dumps(data))
    # 修改 http response 的 Content-Type
    response.mimetype = 'application/json'

    return response


# 修改台风模版的统一响应体
def get_alter_typhoon_response(msg, success, account_id, isAdmin, ty_name, isPublic=None,
                               notes=None, lat=None, lon=None, dist2land=None, storm_speed=None,
                               storm_dir=None, usa_wind=None, usa_sshs=None,
                               basin=None, nature=None, track_type=None):
    data = {
        'msg': msg,
        'result': {
            'account_id': account_id,
            'isAdmin': isAdmin,
            'ty_name': ty_name,
            'is_public': isPublic,
            'notes': notes,
            'lat': lat,  # 纬度
            'lon': lon,  # 经度
            'dist2land': dist2land,  # 中心到地面的距离
            'storm_speed': storm_speed,  # 速度
            'storm_dir': storm_dir,  # 方向（0-360）
            'usa_wind': usa_wind,  # 一分钟平均最大风速，20——150
            'usa_sshs': usa_sshs,  # 风的等级：可以写-5——5
            'basin': basin,
            'nature': nature,
            'track_type': track_type
        },
        'success': success
    }

    # 将python数据字典转换为json
    response = make_response(json.dumps(data))
    # 修改 http response 的 Content-Type
    response.mimetype = 'application/json'

    return response
