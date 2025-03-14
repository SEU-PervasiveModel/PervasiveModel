from flask import Flask
from backend.config import Config
from backend.extensions import db, cors
from backend.matlab.engine import matlab_engine  # 新增

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    cors.init_app(app)
    
    # 启动 MATLAB 引擎
    with app.app_context():
        matlab_engine.start()  # 应用启动时初始化

    # 注册蓝图
    from backend.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # 关闭引擎的钩子
    @app.teardown_appcontext
    def shutdown_matlab(exception=None):
        matlab_engine.stop()

    return app