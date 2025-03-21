import matlab.engine
import os
import logging

class MatlabEngine:
    _engine = None
    
    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            try:
                import os
                logging.info(f'进程 {os.getpid()} 初始化 MATLAB 引擎')
                cls._engine = matlab.engine.start_matlab()
                
                # 添加MATLAB脚本路径
                script_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                         'backend', 'matlab', 'scripts')
                cls._engine.addpath(script_dir)
                
                # 添加所有子文件夹到MATLAB路径
                cls._engine.eval("addpath(genpath('" + script_dir.replace('\\', '/') + "'))", nargout=0)
                
            except Exception as e:
                logging.error(f'MATLAB引擎初始化失败: {str(e)}')
                raise
        return cls._engine

matlab_engine = MatlabEngine()