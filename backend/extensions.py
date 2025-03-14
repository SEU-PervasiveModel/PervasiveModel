from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 创建数据库实例
db = SQLAlchemy()
# 创建跨域扩展实例（允许前端访问）
cors = CORS()