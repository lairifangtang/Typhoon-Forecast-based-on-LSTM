'''
@Project ：typhoon_dev
@File    ：typhoon_info.py
@IDE     ：PyCharm
@Author  ：今天晚上吃啥啊
@Date    ：2023/7/10 10:21
'''

import sys
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from api.decorator import log_request, login_required
from models.models import TyphoonInfo, db, ActionLogs
from utils.helper import get_id_type, has_none_typhoon
from utils.response import get_alter_typhoon_response

# 创建蓝图对象
blue_typhoon_model = Blueprint('blue_typhoon_model', __name__)


# 创建新台风
@blue_typhoon_model.post('/typhoon_info/add')
@login_required
# @log_request
def create_typhoon():
    data = request.get_json()
    print(f"data{data}")
    account_id, isAdmin = get_id_type(data)
    print(f"创建台风{request.values}")

    ty_name = data.get('ty_name')
    isPublic = data.get('isPublic')
    notes = data.get('notes')
    lat = data.get('lat')
    lon = data.get('lon')
    dist2land = data.get('dist2land')
    storm_speed = data.get('storm_speed')
    storm_dir = data.get('storm_dir')
    usa_wind = data.get('usa_wind')
    usa_sshs = data.get('usa_sshs')
    basin = data.get('basin')
    nature = data.get('nature')
    track_type = data.get('track_type')

    if not isAdmin and isPublic:
        return jsonify({
            'msg': '普通用户不能创建公开模板',
            'ty_name': ty_name,
            'success': False
        })
    print(data)
    print(ty_name, isPublic, lat, lon, dist2land, storm_speed,
          storm_dir, usa_wind, usa_sshs, basin, nature, track_type)
    # 允许台风没有备注
    if has_none_typhoon(ty_name, isPublic, lat, lon, dist2land, storm_speed,
                        storm_dir, usa_wind, usa_sshs, basin, nature, track_type):
        return jsonify({
            'msg': 'has none value',
            'ty_name': ty_name,
            'success': False
        })
    if notes is None:
        notes = 'no comments'

    typhoon1 = TyphoonInfo.query.filter_by(ty_name=ty_name, isPublic=True).first()
    typhoon2 = TyphoonInfo.query.filter_by(account_id=account_id, ty_name=ty_name).first()

    # 检查是否和公开的模版重名了，是否和自己名下的其他模版重名了
    if typhoon1 or typhoon2:
        return jsonify({
            'msg': 'same name error',
            'ty_name': ty_name,
            'success': False
        })

    try:
        typhoon = TyphoonInfo(account_id=account_id, ty_name=ty_name, isPublic=isPublic, notes=notes,
                              lat=lat, lon=lon, dist2land=dist2land, speed=storm_speed, dir=storm_dir,
                              usa_wind=usa_wind, sshs=usa_sshs, basin=basin, nature=nature, track=track_type)
        db.session.add(typhoon)
        db.session.commit()

    except:
        # 发生异常时回滚事务
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        return jsonify({
            'msg': 'error when insert into database.(data value error)',
            'ty_name': ty_name,
            'success': False
        })

    try:
        action_log = ActionLogs(account_id=account_id, ty_name=ty_name, isPublic=isPublic,
                                op_type=0, op_details=
                                f"用户账号为{account_id}创建了名字为{ty_name}的台风")
        db.session.add(action_log)
        db.session.commit()

    except:
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        return jsonify({
            'msg': 'error when log',
            'ty_name': ty_name,
            'success': False
        })
    print(f"\n成功\n")

    return jsonify({
        'msg': '台风已创建',
        'ty_name': ty_name,
        'success': True
    })


# 删除台风
@blue_typhoon_model.post('/typhoon_info/delete')
@login_required
# @log_request
def typhoon_delete():
    data = request.get_json()
    account_id, isAdmin = get_id_type(data)
    print(f"data{data}")

    ty_name = data.get('ty_name')

    typhoon = TyphoonInfo.query.filter_by(account_id=account_id, ty_name=ty_name).first()

    if not typhoon:
        return jsonify({
            'msg': 'the typhoon is None',
            'result': {
                'account_id': account_id,
                'ty_name': ty_name
            },
            'success': False
        })

    try:
        db.session.delete(typhoon)
        db.session.commit()
    except:
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        return jsonify({
            'msg': 'error when del in database',
            'result': {
                'account_id': account_id,
                'ty_name': ty_name
            },
            'success': False
        })

    try:
        action_log = ActionLogs(account_id=account_id, ty_name=ty_name, isPublic=typhoon.isPublic,
                                op_type=1, op_details=
                                f"用户账号为{account_id}删除了名字为{ty_name}的台风")
        db.session.add(action_log)
        db.session.commit()
    except:
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        return jsonify({
            'msg': 'error when writing into logs',
            'result': {
                'account_id': account_id,
                'ty_name': ty_name
            },
            'success': False
        })

    return jsonify({
        'msg': '成功删除该台风',
        'result': {
            'account_id': account_id,
            'ty_name': ty_name
        },
        'success': True
    })


# 修改台风信息
@blue_typhoon_model.post('/typhoon_info/alter')
@login_required
# @log_request
def typhoon_alter():
    data = request.get_json()
    account_id, isAdmin = get_id_type(data)

    print(data)

    ty_name = data.get('ty_name')
    isPublic = data.get('isPublic')
    notes = data.get('notes')
    lat = data.get('lat')
    lon = data.get('lon')
    dist2land = data.get('dist2land')
    storm_speed = data.get('storm_speed')
    storm_dir = data.get('storm_dir')
    usa_wind = data.get('usa_wind')
    usa_sshs = data.get('usa_sshs')
    basin = data.get('basin')
    nature = data.get('nature')
    track_type = data.get('track_type')

    # 允许notes为空
    if has_none_typhoon(ty_name, isPublic, lat, lon, dist2land, storm_speed,
                        storm_dir, usa_wind, usa_sshs, basin, nature, track_type):
        return jsonify({
            'msg': 'has none in values',
            'ty_name': ty_name,
            'success': False
        })
    if notes is None:
        notes = 'no comments'

    typhoon = TyphoonInfo.query.filter_by(account_id=account_id, ty_name=ty_name).first()

    # 如果台风查询结果为空
    if typhoon is None:
        response = get_alter_typhoon_response('no typhoon found by account_id and ty_name', False, account_id, isAdmin,
                                              ty_name,
                                              isPublic, notes, lat, lon, dist2land, storm_speed, storm_dir, usa_wind,
                                              usa_sshs, basin, nature, track_type)
        return response, 404

    # 如果普通用户修改了isPublic
    if not isAdmin and typhoon.isPublic != isPublic:
        response = get_alter_typhoon_response('common user cannot alter public typhoon', False, account_id, isAdmin,
                                              ty_name,
                                              isPublic, notes, lat, lon, dist2land, storm_speed, storm_dir, usa_wind,
                                              usa_sshs, basin, nature, track_type)
        return response, 401

    # 记录修改的详细细节
    original_typhoon = {
        "ty_name": typhoon.ty_name,
        "isPublic": typhoon.isPublic,
        "notes": typhoon.notes,
        "lat": typhoon.lat,
        "lon": typhoon.lon,
        "dist2land": typhoon.dist2land,
        "storm_speed": typhoon.speed,
        "storm_dir": typhoon.dir,
        "usa_wind": typhoon.usa_wind,
        "usa_sshs": typhoon.sshs,
        "basin": typhoon.basin,
        "nature": typhoon.nature,
        "track_type": typhoon.track
    }
    modified_typhoon = {
        "ty_name": ty_name,
        "isPublic": isPublic,
        "notes": notes,
        "lat": lat,
        "lon": lon,
        "dist2land": dist2land,
        "storm_speed": storm_speed,
        "storm_dir": storm_dir,
        "usa_wind": usa_wind,
        "usa_sshs": usa_sshs,
        "basin": basin,
        "nature": nature,
        "track_type": track_type
    }
    differ = f"您修改了"
    for key in original_typhoon:
        if modified_typhoon[key] != original_typhoon[key]:
            differ = differ + f" {key}:{original_typhoon[key]} to {modified_typhoon[key]},"

    try:
        typhoon.ty_name = ty_name
        typhoon.isPublic = isPublic
        typhoon.notes = notes
        typhoon.lat = lat
        typhoon.lon = lon
        typhoon.dist2land = dist2land
        typhoon.speed = storm_speed
        typhoon.dir = storm_dir
        typhoon.usa_wind = usa_wind
        typhoon.sshs = usa_sshs
        typhoon.basin = basin
        typhoon.nature = nature
        typhoon.track = track_type

        db.session.commit()
    except SQLAlchemyError as e:
        # 处理数据库提交异常
        db.session.rollback()  # 回滚会话中的更改
        error_msg = str(e)
        print(error_msg)
        # 进行适当的错误处理操作
        response = get_alter_typhoon_response('error when writing logs', False, account_id, isAdmin, ty_name)
        return response, 500

    try:
        action_log = ActionLogs(account_id=account_id, ty_name=ty_name, isPublic=typhoon.isPublic,
                                op_type=2, op_details=
                                differ)
        db.session.add(action_log)
        db.session.commit()
    except:
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        response = get_alter_typhoon_response('error when writing logs', False, account_id, isAdmin, ty_name)
        return response, 500

    response = get_alter_typhoon_response('alter success', True, account_id, isAdmin, ty_name,
                                          isPublic, notes, lat, lon, dist2land, storm_speed, storm_dir, usa_wind,
                                          usa_sshs, basin, nature, track_type)
    return response, 200


# 查询所有台风数据
@blue_typhoon_model.post('/typhoon_info/search')
@login_required
# @log_request
def typhoon_list():
    data = request.get_json()
    print(f"data{data}")
    account_id, isAdmin = get_id_type(data)

    if account_id is None or isAdmin is None:
        return jsonify({
            'msg': 'id is none or isAdmin is none',
            'result': None,
            'success': True
        }), 404

    typhoons = TyphoonInfo.query.all()
    # print(typhoons)
    typhoon_data = []
    for typhoon in typhoons:
        #     print(f"正在访问台风：{typhoon}")
        #     print(f"ty.id{typhoon.account_id},id{account_id},ty.isPublic{typhoon.isPublic}")
        if int(typhoon.account_id) == int(account_id) or typhoon.isPublic:
            typhoon_data.append({
                'ty_name': typhoon.ty_name,  # 台风名字，唯一标识台风
                'isPublic': typhoon.isPublic,  # 公开/私有
                'notes': typhoon.notes,  # 该台风基本信息的备注
                'lat': typhoon.lat,  # 纬度
                'lon': typhoon.lon,  # 经度
                'dist2land': typhoon.dist2land,  # 中心到地面的距离
                'storm_speed': typhoon.speed,  # 速度
                'storm_dir': typhoon.dir,  # 方向（0-360）
                'usa_wind': typhoon.usa_wind,  # 一分钟平均最大风速，20——150
                'usa_sshs': typhoon.sshs,  # 风的等级：可以写-5——5
                'basin': typhoon.basin,
                'nature': typhoon.nature,
                'track_type': typhoon.track
            })
    print(typhoon_data)
    return jsonify({
        'msg': 'search success',
        'result': typhoon_data,
        'success': True
    })
