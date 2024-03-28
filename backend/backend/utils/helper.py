'''
@Project ：typhoon_dev 
@File    ：helper.py
@IDE     ：PyCharm 
@Author  ：今天晚上吃啥啊
@Date    ：2023/7/10 8:43
'''

import json
from models.models import *
import random


# # 从cookie值（字符串）中获取account_id 和 isAdmin
# def get_data_from_cookie(cookie_value):
#     # 字符串转义字符替换
#     cookie_value = cookie_value.replace('//"', '"')
#     cookie_value = cookie_value.replace('//054', ',')
#
#     # JSON字符串转换为字典
#     cookie_data = json.loads(cookie_value)
#
#     account_id = cookie_data.get('account_id')
#     isAdmin = cookie_data.get('isAdmin')
#
#     return account_id, isAdmin

# 获取用户的id和身份
def get_id_type(data):
    account_id = data.get('account_id')
    user = User.query.filter_by(account_id=account_id).first()
    return int(account_id), user.isAdmin


# 生成数据库中不存在的随机用户ID
def generate_unique_account_id():
    while True:
        account_id = random.randint(10000, 19999)  # 生成随机整数
        if not User.query.filter_by(account_id=account_id).first():  # 检查是否存在相同的 account_id
            return int(account_id)


# 判断台风数据是否有空值
def has_none_typhoon(ty_name, isPublic, lat, lon, dist2land, storm_speed, storm_dir,
                     usa_wind,usa_sshs, basin, nature, track_type):
    if ty_name is None or isPublic is None or lon is None or lat is None or dist2land is None or storm_dir is None \
            or storm_speed is None or usa_wind is None or usa_sshs is None or basin is None or nature is None \
            or track_type is None:
        return True
    else:
        return False
