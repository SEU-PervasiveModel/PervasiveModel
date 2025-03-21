from flask import Blueprint, request, jsonify
from backend.models import User
from backend.extensions import db
from backend.matlab.engine import matlab_engine
from backend.matlab.functions import init_channel_model, configure_antenna, create_track
import matlab
import traceback
from werkzeug.exceptions import BadRequest

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def api_root():
    return jsonify({
        "status": "online",
        "api_version": "1.0",
        "endpoints": [
            "/api/matlab-compute",
            "/api/register",
            "/api/login",
            "/api/track",
            "/api/antenna"
        ]
    })

@api.route('/matlab-compute', methods=['POST'])
def matlab_compute():
    try:
        # 1. 获取并验证数据
        data = request.get_json(force=True)
        if 'values' not in data:
            return jsonify({"error": "缺少必要参数 values"}), 400
            
        # 2. 转换数据类型
        input_value = data['values']
        if isinstance(input_value, list):
            matlab_data = matlab.double(input_value)
        else:
            matlab_data = matlab.double([float(input_value)])
        
        # 3. 获取引擎实例
        engine = matlab_engine.get_engine()
        
        # 4. 调用 MATLAB 函数
        result = engine.compute(matlab_data)
        
        # 5. 转换结果类型
        if isinstance(result, matlab.double):
            output = result._data.tolist()  # 转换为 Python 列表
        else:
            output = float(result)
            
        return jsonify({
            "result": output,
            "status": "success"
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"计算失败: {str(e)}",
            "status": "error"
        }), 500
    # 注册接口
@api.route('/register', methods=['POST'])
def register():
    # 获取前端发送的JSON数据
    data = request.get_json()
    
    # 检查必填字段
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': '缺少用户名或密码'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已被占用'}), 409
    
    # 创建用户
    user = User(
        username=data['username'],
        email=data.get('email', '')  # 邮箱可选
    )
    user.set_password(data['password'])  # 加密密码
    
    # 保存到数据库
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': '注册成功', 'user_id': user.id}), 201

# 登录接口（示例）
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    return jsonify({'message': '登录成功', 'user_id': user.id})

REQUIRED_PARAMS = {
    # 基础数值参数
    'move_speed': {'type': 'double'},
    'move_accel': {'type': 'double'},
    'name': {'type': 'string'},
    
    # 三维向量（数组类型）
    'ini_pos': {
        'type': 'array',
        'length': 3,
        'element_type': 'double'
    },
    
    'move_dir': {
        'type': 'array',
        'length': 3,
        'element_type': 'double'
    },

    # 枚举选择参数
    'track_type': {
        'type': 'enum',
        'options': ['static', 'linear', 'circle', 'random','random_circle']
    }
}

@api.route('/track', methods=['POST'])
def handle_track():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请提供轨迹参数"}), 400
            
        # 验证必要参数
        for param in ['name', 'move_speed', 'move_accel', 'ini_pos', 'move_dir', 'track_type']:
            if param not in data:
                return jsonify({"error": f"缺少必要参数: {param}"}), 400
                
        # 验证数组参数
        for param in ['ini_pos', 'move_dir']:
            if not isinstance(data[param], list) or len(data[param]) != 3:
                return jsonify({"error": f"参数 {param} 必须是长度为3的数组"}), 400
                
        success, result = create_track(data)
        
        if success:
            return jsonify({
                "status": "success",
                "message": result
            })
        else:
            return jsonify({
                "status": "error", 
                "error": result
            }), 400
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"创建轨迹失败: {str(e)}",
            "status": "error"
        }), 500
    
@api.route('/antenna', methods=['POST'])
def handle_antenna():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "请提供天线参数"}), 400
            
        success, result = configure_antenna(data)
        
        if success:
            return jsonify({
                "status": "success",
                "message": result
            })
        else:
            return jsonify({
                "status": "error",
                "error": result
            }), 400
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"天线配置失败: {str(e)}",
            "status": "error"
        }), 500