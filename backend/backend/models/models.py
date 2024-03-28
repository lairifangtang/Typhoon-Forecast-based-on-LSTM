from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import text, CheckConstraint, ForeignKeyConstraint

db = SQLAlchemy()


# 模型类：用户
class User(db.Model):
    __tablename__ = 'user'
    # 唯一标识用户，随机生成
    account_id = db.Column(db.Integer, primary_key=True, comment='用户ID')
    user_name = db.Column(db.String(255), comment='用户名')
    password = db.Column(db.String(255), comment='密码')
    isAdmin = db.Column(db.Boolean, server_default=text('0'), comment='是否管理员')
    salt = db.Column(db.String(255), comment='密码的盐')


# 模型类：台风基本信息模版
class TyphoonInfo(db.Model):
    __tablename__ = 'typhoon_info'
    # 唯一标识台风
    account_id = db.Column(db.Integer, db.ForeignKey('user.account_id', ondelete='CASCADE'), primary_key=True,
                           comment='用户ID')
    ty_name = db.Column(db.String(255), primary_key=True, comment='台风名字')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='台风模板创建时间')
    isPublic = db.Column(db.Boolean, server_default=text('0'), comment='模板权限（private/public）')
    notes = db.Column(db.String(500), comment='备注')
    lat = db.Column(db.Float, comment='纬度')
    lon = db.Column(db.Float, comment='经度')
    dist2land = db.Column(db.Float, comment='中心到地面的距离')
    speed = db.Column(db.Float, comment='速度')
    dir = db.Column(db.Float, comment='方向（0-360）')
    usa_wind = db.Column(db.Float, comment='一分钟平均最大风速')
    sshs = db.Column(db.Integer, comment='风的等级-5~5')
    basin = db.Column(db.Integer, comment='海域0-5')
    nature = db.Column(db.Integer, comment='性质0-5')
    track = db.Column(db.Integer, comment='轨迹类型0-5')


# 模型类：操作记录
class ActionLogs(db.Model):
    __tablename__ = 'action_Logs'
    account_id = db.Column(db.Integer, comment='用户账号')
    ty_name = db.Column(db.String(255), comment='台风名')
    isPublic = db.Column(db.Boolean, default=False, comment='log记录时间')
    op_type = db.Column(db.Integer, comment='操作类型')
    act_time = db.Column(db.DateTime, default=datetime.datetime.now, primary_key=True, comment='操作时间')
    op_details = db.Column(db.String(1000), comment='操作详细记录')

#
# with app.app_context():
#     # 清空数据库表
#     db.drop_all()
#     # 根据模型类创建数据库表
#     db.create_all()

# # 测试是否连接成功
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("select 1"))
#         print(rs.fetchone())
