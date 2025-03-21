from flask import Flask
from backend.config import Config
from backend.extensions import db, cors
from backend.matlab.engine import MatlabEngine, matlab_engine
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 配置日志
    logging.basicConfig(level=logging.DEBUG)
    
    # 初始化数据库和跨域
    db.init_app(app)
    cors.init_app(app)
    
    # 初始化 MATLAB 引擎
    with app.app_context():
        try:
            matlab_engine.initialize(app.root_path)
            app.logger.info("MATLAB引擎初始化成功")
        except Exception as e:
            app.logger.error(f"MATLAB引擎初始化失败: {str(e)}")
            # 生产环境应在此处处理失败情况
    
    # 在请求前检查MATLAB引擎状态
    @app.before_request
    def check_matlab_engine():
        if not matlab_engine.is_initialized():
            try:
                matlab_engine.initialize(app.root_path)
                app.logger.info("请求前重新初始化MATLAB引擎成功")
            except Exception as e:
                app.logger.error(f"请求前重新初始化MATLAB引擎失败: {str(e)}")
                # 可以在这里决定如何处理失败情况
    
    # 注册蓝图
    from backend.routes import api
    app.register_blueprint(api, url_prefix='/api')
    
    # 应用退出时清理
    @app.teardown_appcontext
    def shutdown_engine(exception=None):
        matlab_engine.shutdown()
    
    return app