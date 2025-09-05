import os

class Config:
    # 开发环境配置
    # ENV='development'
    # 调试模式为True
    DEBUG = True
    # 关闭汉字自动转ascii
    JSON_AS_ASCII = False

    # 通过修改以下代码来操作不同的SQL比写原生SQL简单很多,通过ORM可以实现从底层更改使用的SQL
    # MySQL所在主机名
    HOSTNAME = os.getenv('DB_HOST', 'localhost')
    # MySQL监听的端口号，默认3306
    PORT = int(os.getenv('DB_PORT', 3306))
    # 连接MySQL的用户名
    USERNAME = os.getenv('DB_USERNAME', 'root')
    # 连接MySQL的密码
    PASSWORD = os.getenv('DB_PASSWORD', '')
    # MySQL上创建的数据库名称
    DATABASE = os.getenv('DB_NAME', 'typhoon')
    # 配置连接数据库路径
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
