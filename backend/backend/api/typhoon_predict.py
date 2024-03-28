'''
@Project ：typhoon_dev
@File    ：typhoon_predict.py
@IDE     ：PyCharm
@Author  ：我
@Date    ：2023/7/12 10:21
'''
import sys
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
import tensorflow as tf
import joblib
import pandas as pd
import numpy as np

from api.decorator import log_request, login_required
from models.models import TyphoonInfo, ActionLogs, db
from gevent import os
from utils.helper import get_id_type
from utils.response import get_alter_typhoon_response

# 创建蓝图对象

blue_typhoon_predict = Blueprint('blue_typhoon_predict', __name__)

# 获取当前脚本所在的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建模型文件的相对路径
# 加载LSTM模型
model_path = os.path.join(current_dir, "..", "typhoon_LSTM", "lstm_model.h5")
model = tf.keras.models.load_model(model_path)

# 加载标准化参数
model_path = os.path.join(current_dir, "..", "typhoon_LSTM", "scaler_X.pkl")
scaler_X = joblib.load(model_path)
model_path = os.path.join(current_dir, "..", "typhoon_LSTM", "scaler_y.pkl")
scaler_y = joblib.load(model_path)


def Cal_line(lat, lon, dist2land, storm_speed, storm_dir, usa_wind, usa_sshs, basin, nature, track_type):
    # 创建一个DataFrame并设置默认值为0
    input_data = pd.DataFrame({
        'LAT': [lat],
        'LON': [lon],
        'DIST2LAND': [dist2land],
        'STORM_SPEED': [storm_speed],
        'STORM_DIR': [storm_dir],
        'USA_WIND': [usa_wind],
        'USA_SSHS': [usa_sshs],
        'BASIN_EP': [0],
        'BASIN_NI': [0],
        'BASIN_SA': [0],
        'BASIN_SI': [0],
        'BASIN_SP': [0],
        'BASIN_WP': [0],
        'NATURE_DS': [0],
        'NATURE_ET': [0],
        'NATURE_MX': [0],
        'NATURE_NR': [0],
        'NATURE_SS': [0],
        'NATURE_TS': [0],
        'TRACK_TYPE_PROVISIONAL': [0],
        'TRACK_TYPE_PROVISIONAL_spur': [0],
        'TRACK_TYPE_main': [0],
        'TRACK_TYPE_spur-merge': [0],
        'TRACK_TYPE_spur-other': [0],
        'TRACK_TYPE_spur-split': [0]
    })
    # 根据输入的值设置相应的列为1
    input_data[f'BASIN_EP'] = 1 if basin == 0 else 0
    input_data[f'BASIN_NI'] = 1 if basin == 1 else 0
    input_data[f'BASIN_SA'] = 1 if basin == 2 else 0
    input_data[f'BASIN_SI'] = 1 if basin == 3 else 0
    input_data[f'BASIN_SP'] = 1 if basin == 4 else 0
    input_data[f'BASIN_WP'] = 1 if basin == 5 else 0

    input_data[f'NATURE_DS'] = 1 if nature == 0 else 0
    input_data[f'NATURE_ET'] = 1 if nature == 1 else 0
    input_data[f'NATURE_MX'] = 1 if nature == 2 else 0
    input_data[f'NATURE_NR'] = 1 if nature == 3 else 0
    input_data[f'NATURE_SS'] = 1 if nature == 4 else 0
    input_data[f'NATURE_TS'] = 1 if nature == 5 else 0

    input_data[f'TRACK_TYPE_PROVISIONAL'] = 1 if track_type == 0 else 0
    input_data[f'TRACK_TYPE_PROVISIONAL_spur'] = 1 if track_type == 1 else 0
    input_data[f'TRACK_TYPE_main'] = 1 if track_type == 2 else 0
    input_data[f'TRACK_TYPE_spur-merge'] = 1 if track_type == 3 else 0
    input_data[f'TRACK_TYPE_spur-other'] = 1 if track_type == 4 else 0
    input_data[f'TRACK_TYPE_spur-split'] = 1 if track_type == 5 else 0

    # 将输入数据转换为浮点数类型
    input_data = input_data.astype(float)

    # 数据进行标准化
    input_data_scaled = scaler_X.transform(input_data)

    # 将输入数据转换为期望的形状
    input_sequence = np.array([input_data_scaled])  # 形状：(1, timesteps, num_features)

    # 预测输出
    predicted_sequence_scaled = model.predict(input_sequence)  # 形状：(1, 5, num_features)
    predicted_sequence_2d = np.reshape(predicted_sequence_scaled, (5, -1))  # 将其转换为二维数组 (5, num_features)
    predicted_sequence = scaler_y.inverse_transform(predicted_sequence_2d)  # 反标准化

    # 提取预测值
    pre_result = []
    # pre_result[0] = predicted_sequence[0]
    # pre_result[1] = predicted_sequence[1]
    # pre_result[2] = predicted_sequence[2]
    # pre_result[3] = predicted_sequence[3]
    # pre_result[4] = predicted_sequence[4]


    # print("test:", y1, y2, y3, y4, y5)
    return predicted_sequence


'''
调用预测模型
'''


@blue_typhoon_predict.post('/typhoon_predict')
@login_required
# @log_request
def line_request():
    data = request.get_json()
    account_id, isAdmin = get_id_type(data)
    print(f"前端传来：{data}")

    ty_name = data.get('ty_name')

    # 检查空值
    if account_id is None or ty_name is None:
        return jsonify({
            'msg': 'account_id or ty_name is None.',
            'result': None,
            'success': False
        })

    typhoon1 = TyphoonInfo.query.filter_by(account_id=account_id, ty_name=ty_name).first()
    typhoon2 = TyphoonInfo.query.filter_by(ty_name=ty_name, isPublic=True).first()

    if typhoon1:
        typhoon = typhoon1
    elif typhoon2:
        typhoon = typhoon2

    predict = Cal_line(lat=typhoon.lat, lon=typhoon.lon, dist2land=typhoon.dist2land,
                       storm_speed=typhoon.speed, storm_dir=typhoon.dir, usa_wind=typhoon.usa_wind,
                       usa_sshs=typhoon.sshs, basin=typhoon.basin, nature=typhoon.nature, track_type=typhoon.track)


    y1 = predict[0]
    y2 = predict[1]
    y3 = predict[2]
    y4 = predict[3]
    y5 = predict[4]

    # 台风等级
    ty_level = []
    for j in range(5):
        if predict[j][2] <= 62 * 1.852:
            ty_level.append('热带低压')
        elif 62 * 1.852 < predict[j][2] <= 88 * 1.852:
            ty_level.append('热带风暴')
        elif 88 * 1.852 < predict[j][2] <= 117 * 1.852:
            ty_level.append('强热带风暴')
        elif 117 * 1.852 < predict[j][2] <= 149 * 1.852:
            ty_level.append('台风')
        elif 149 * 1.852 < predict[j][2] <= 183 * 1.852:
            ty_level.append('强台风')
        elif predict[j][2] > 184 * 1.852:
            ty_level.append('超强台风')

    # 7级风圈大小，10级风圈大小，12级风圈大小
    radius = []
    for i in range(5):
        if predict[i][2] <= 126 * 1.852:
            radius.append([300, 0, 0])
        elif 126 * 1.852 < predict[i][2] <= 151 * 1.852:
            radius.append([300, 100, 0])
        elif predict[i][2] > 151 * 1.852:
            radius.append([300, 100, 40])

    # 当前时间+3，+6，+9，+12，+15
    time = []
    current_time = datetime.now()
    for i in range(5):
        new_time = current_time + timedelta(hours=(i+1) * 3)
        formatted_time = new_time.strftime('%Y-%m-%d %H:%M')
        time.append(formatted_time)

    try:
        action_log = ActionLogs(account_id=account_id, ty_name=ty_name, isPublic=typhoon.isPublic,
                                op_type=3, op_details=f'predict result: '
                                                      f'维度1:{y1[0]:.1} 经度1:{y1[1]:.1} 风级1:{ty_level[0]}, '
                                                      f'维度2:{y2[0]:.1} 经度2:{y2[1]:.1} 风级2:{ty_level[1]}, '
                                                      f'维度3:{y3[0]:.1} 经度3:{y3[1]:.1} 风级3:{ty_level[2]}, '
                                                      f'维度4:{y4[0]:.1} 经度4:{y4[1]:.1} 风级4:{ty_level[3]}, '
                                                      f'维度5:{y5[0]:.1} 经度5:{y5[1]:.1} 风级5:{ty_level[4]}, ')
        db.session.add(action_log)
        db.session.commit()
    except:
        db.session.rollback()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("异常类型:", exc_type)
        print("异常值:", exc_value)
        response = get_alter_typhoon_response('error when writing logs', False, account_id, isAdmin, ty_name)
        return response, 500

    return jsonify({
        'msg': "模型调用成功",
        'result': [
            {'lat': float(y1[0]), 'lon': float(y1[1]), 'usa_wind': float(y1[2]), 'level7_radius': radius[0][0],
             'level10_radius': radius[0][1], 'level12_radius': radius[0][2], 'time': time[0]},
            {'lat': float(y2[0]), 'lon': float(y2[1]), 'usa_wind': float(y2[2]), 'level7_radius': radius[1][0],
             'level10_radius': radius[1][1], 'level12_radius': radius[1][2], 'time': time[1]},
            {'lat': float(y3[0]), 'lon': float(y3[1]), 'usa_wind': float(y3[2]), 'level7_radius': radius[2][0],
             'level10_radius': radius[2][1], 'level12_radius': radius[2][2], 'time': time[2]},
            {'lat': float(y4[0]), 'lon': float(y4[1]), 'usa_wind': float(y4[2]), 'level7_radius': radius[3][0],
             'level10_radius': radius[3][1], 'level12_radius': radius[3][2], 'time': time[3]},
            {'lat': float(y5[0]), 'lon': float(y5[1]), 'usa_wind': float(y5[2]), 'level7_radius': radius[4][0],
             'level10_radius': radius[4][1], 'level12_radius': radius[4][2], 'time': time[4]}
        ],
        'success': True
    })
