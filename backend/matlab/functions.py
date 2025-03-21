from .engine import matlab_engine
import matlab
import numpy as np
import logging

def init_channel_model(params):
    """初始化信道模型"""
    try:
        engine = matlab_engine.get_engine()
        # 转换Python参数为MATLAB参数
        matlab_params = {k: matlab.double([v]) if isinstance(v, (int, float)) else v 
                       for k, v in params.items()}
        
        # 调用MATLAB函数
        result = engine.channel_model(matlab_params, nargout=1)
        return True, result
    except Exception as e:
        logging.error(f"初始化信道模型失败: {str(e)}")
        return False, str(e)

def configure_antenna(params):
    """配置天线参数"""
    try:
        engine = matlab_engine.get_engine()
        
        # 提取参数
        antenna_type = params.get('antenna_type', 'uniform_plane')  
        num_per_row = params.get('num_per_row', 8)
        num_per_col = params.get('num_per_col', 8)
        spacing_row = params.get('spacing_row', 0.5)
        spacing_col = params.get('spacing_col', 0.5)
        rotate_z = params.get('rotate_z', 0)
        rotate_y = params.get('rotate_y', 0)
        rotate_x = params.get('rotate_x', 0)
        
        # 调用MATLAB函数
        if antenna_type == 'uniform_linear':
            result = engine.antenna_array('linear', 
                                         matlab.double([num_per_row]), 
                                         matlab.double([2.4e9]),  # 默认频率
                                         matlab.double([spacing_row]), 
                                         None, None,
                                         matlab.double([rotate_z]), 
                                         matlab.double([rotate_y]), 
                                         matlab.double([rotate_x]),
                                         nargout=1)
        elif antenna_type == 'uniform_plane':
            result = engine.antenna_array('planar', 
                                         matlab.double([num_per_row]), 
                                         matlab.double([num_per_col]),
                                         matlab.double([2.4e9]),  # 默认频率
                                         matlab.double([spacing_row]),
                                         matlab.double([spacing_col]), 
                                         None, None,
                                         matlab.double([rotate_z]), 
                                         matlab.double([rotate_y]), 
                                         matlab.double([rotate_x]),
                                         nargout=1)
        elif antenna_type == 'cylindrical':
            result = engine.antenna_array('cylindrical', 
                                         matlab.double([num_per_row]), 
                                         matlab.double([num_per_col]),
                                         matlab.double([2.4e9]),  # 默认频率
                                         matlab.double([spacing_row]),
                                         matlab.double([spacing_col]), 
                                         None, None,
                                         matlab.double([rotate_z]), 
                                         matlab.double([rotate_y]), 
                                         matlab.double([rotate_x]),
                                         nargout=1)
        else:
            return False, "不支持的天线类型"
            
        return True, "天线配置成功"
    except Exception as e:
        logging.error(f"配置天线失败: {str(e)}")
        return False, str(e)

def create_track(params):
    """创建轨迹"""
    try:
        engine = matlab_engine.get_engine()
        
        # 提取参数
        track_type = params.get('track_type', 'linear')
        name = params.get('name', 'device1')
        move_speed = params.get('move_speed', 1.0)
        move_accel = params.get('move_accel', 0.0)
        ini_pos = params.get('ini_pos', [0, 0, 0])
        move_dir = params.get('move_dir', [1, 0, 0])
        
        # 调用MATLAB函数
        result = engine.track(track_type,
                              matlab.double([len(name)]),  # 采样点数量
                              matlab.double([move_speed]),
                              matlab.double([move_accel]),
                              matlab.double(ini_pos),
                              matlab.double(move_dir),
                              matlab.double([100]),  # 默认采样点数
                              nargout=1)
        
        return True, "轨迹创建成功"
    except Exception as e:
        logging.error(f"创建轨迹失败: {str(e)}")
        return False, str(e)