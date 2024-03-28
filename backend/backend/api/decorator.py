'''
@Project ：typhoon_dev 
@File    ：decorator.py
@IDE     ：PyCharm 
@Author  ：今天晚上吃啥啊
@Date    ：2023/7/10 11:02
'''
from datetime import datetime
from functools import wraps
from flask import request, jsonify

from models.models import User


# 定义一个装饰器，用于检查id是否存在，id是否有效
def login_required(view_func):
    @wraps(view_func)
    def decorated_func(*args, **kwargs):
        # print("装饰器：登录检查装饰器被调用啦")
        data = request.get_json()
        # print(f"装饰器：获取请求体数据{request.headers}")
        account_id = data.get('account_id')

        if not account_id:
            return jsonify({
                'message': 'error account_id'
            }), 401

        user = User.query.filter_by(account_id=account_id).first()

        if not user:
            return jsonify({
                'message': 'database dont has this account_id'
            }),401

        print(f"装饰器：用户{account_id}进行了访问")
        return view_func(*args, **kwargs)

    return decorated_func


def log_request(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 获取请求头
        request_headers = str(request.headers)

        # 获取请求体
        request_body = str(request.get_json())

        # 调用原始函数并记录返回结果
        response = func(*args, **kwargs)

        # 获取返回头
        response_headers = str(response.headers)

        # 获取返回体
        response_body = response.response

        # 获取 HTTP 状态码
        status_code = str(response.status_code)

        # 将请求头、请求体、返回头、返回体、HTTP 状态码和时间戳写入文件
        with open('C:\\Users\\17995\\Desktop\\share\\share.txt', 'a') as file:
            file.write('--------- -------- -------- --------- --------\n')
            file.write('------Request------\n')
            if not request_headers:
                file.write(f"Request Headers: {request_headers}\n")
            if not request_body:
                file.write(f"Request Body: {request_body}\n\n")

            file.write('------Response------\n')
            if not response_headers:
                file.write(f"Response Headers: {response_headers}\n")
            if not response_body:
                file.write(f"Response Body: {response_body}\n")
            file.write(f"Status Code: {status_code}\n")
            file.write(f"Timestamp: {timestamp}\n\n")

        return response

    return decorated_function
