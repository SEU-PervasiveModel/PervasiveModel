from flask import Flask
from backend.config import Config
from backend.extensions import db, cors
from backend.matlab.engine import MatlabEngine, matlab_engine
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    @app.before_request
    def ensure_matlab_initialized():
        MatlabEngine.initialize(app.root_path)

    
    # 配置日志
    logging.basicConfig(level=logging.DEBUG)
    
    # 初始化数据库和跨域
    db.init_app(app)
    cors.init_app(app)
    
    # 初始化 MATLAB 引擎
    with app.app_context():
        try:
            matlab_engine.initialize(app.root_path)
        except Exception as e:
            app.logger.error(f"应用启动失败: {str(e)}")
            # 生产环境应在此处处理失败情况
    
    # 注册蓝图
    from backend.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # 应用退出时清理
    @app.teardown_appcontext
    def shutdown_engine(exception=None):
        matlab_engine.shutdown()
    
    return app