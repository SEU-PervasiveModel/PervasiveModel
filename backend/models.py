from datetime import datetime
from backend.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # 定义用户表结构
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # 存储加密后的密码
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 加密密码的方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码的方法
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)