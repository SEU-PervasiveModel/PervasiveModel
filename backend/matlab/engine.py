import matlab.engine
import os
import logging
import atexit

class MatlabEngine:
    _engine = None
    _pid = None

    @classmethod
    def initialize(cls, app_root_path):
        if cls._engine is None or cls._pid != os.getpid():
            # 仅在新进程中初始化
            cls._pid = os.getpid()
            script_path = os.path.join(app_root_path, 'matlab/scripts')
            
            # 终止可能残留的引擎
            if cls._engine is not None:
                try:
                    cls._engine.quit()
                except:
                    pass
            
            # 启动新引擎
            cls._engine = matlab.engine.start_matlab()
            cls._engine.addpath(script_path)
            logging.info(f"进程 {cls._pid} 初始化 MATLAB 引擎")
            
            # 注册退出处理
            atexit.register(cls.shutdown)

    @classmethod
    def shutdown(cls):
        if cls._engine is not None:
            cls._engine.quit()
            cls._engine = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            raise RuntimeError("MATLAB 引擎未初始化")
        return cls._engine

# 全局访问点
matlab_engine = MatlabEngine()