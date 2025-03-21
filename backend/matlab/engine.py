import matlab.engine
import os
import logging

class MatlabEngine:
    def __init__(self):
        self._engine = None
        self._initialized = False
    
    def initialize(self, root_path=None):
        """初始化MATLAB引擎"""
        if not self._initialized:
            try:
                logging.info(f'进程 {os.getpid()} 初始化 MATLAB 引擎')
                self._engine = matlab.engine.start_matlab()
                
                # 添加MATLAB脚本路径
                if root_path:
                    script_dir = os.path.join(root_path, 'matlab', 'scripts')
                    if os.path.exists(script_dir):
                        self._engine.addpath(script_dir)
                        
                        # 添加所有子文件夹到MATLAB路径
                        self._engine.eval("addpath(genpath('" + script_dir.replace('\\', '/') + "'))", nargout=0)
                        logging.info(f'添加MATLAB脚本路径: {script_dir}')
                
                self._initialized = True
                return True
            except Exception as e:
                logging.error(f'MATLAB引擎初始化失败: {str(e)}')
                self._initialized = False
                raise
        return False
    
    def is_initialized(self):
        """检查引擎是否已初始化"""
        return self._initialized and self._engine is not None
    
    def shutdown(self):
        """关闭MATLAB引擎"""
        if self._initialized and self._engine:
            try:
                self._engine.quit()
                logging.info('MATLAB引擎已关闭')
            except Exception as e:
                logging.error(f'关闭MATLAB引擎失败: {str(e)}')
            finally:
                self._engine = None
                self._initialized = False
    
    def get_engine(self):
        """获取MATLAB引擎实例"""
        if not self.is_initialized():
            self.initialize()
        return self._engine

# 创建单例实例
matlab_engine = MatlabEngine()