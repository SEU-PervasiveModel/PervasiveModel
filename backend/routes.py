from flask import Blueprint, request, jsonify
from backend.models import User
from backend.extensions import db
from backend.matlab.engine import matlab_engine  # 新增
import matlab

from flask import Blueprint, request, jsonify
from backend.matlab.engine import matlab_engine
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
def handle_device_data():
    try:
        data = request.get_json()
        errors = []
        processed = {}

        # 参数存在性检查
        missing_params = [p for p in REQUIRED_PARAMS if p not in data]
        if missing_params:
            errors.extend([f"Missing required parameter: {p}" for p in missing_params])

        # 类型验证处理
        for param, config in REQUIRED_PARAMS.items():
            if param not in data:
                continue  # 已处理缺失情况
            
            try:
                # 枚举类型验证
                if config['type'] == 'enum':
                    if data[param] not in config['options']:
                        errors.append(f"Invalid {param}: must be one of {config['options']}")
                    else:
                        processed[param] = data[param]
                
                # 三维向量验证
                elif config['type'] == 'array':
                    value = data[param]
                    if not isinstance(value, list):
                        errors.append(f"{param} must be an array")
                        continue
                    
                    if len(value) != config['length']:
                        errors.append(f"{param} requires exactly {config['length']} elements")
                        continue
                    
                    valid_elements = []
                    for i, element in enumerate(value):
                        try:
                            num = float(element)
                            if not isinstance(element, (int, float)):
                                errors.append(f"{param}[{i}] contains non-numeric type")
                            else:
                                valid_elements.append(num)
                        except (TypeError, ValueError):
                            errors.append(f"{param}[{i}] is not a valid double")
                    
                    if len(valid_elements) == config['length']:
                        processed[param] = valid_elements
                
                # 基础数值验证
                elif config['type'] == 'double':
                    try:
                        num = float(data[param])
                        if not isinstance(data[param], (int, float)):
                            errors.append(f"{param} contains non-numeric type")
                        else:
                            processed[param] = num
                    except (TypeError, ValueError):
                        errors.append(f"{param} is not a valid double")

            except Exception as e:
                errors.append(f"Validation error for {param}: {str(e)}")

        # 错误处理
        if errors:
            return jsonify({
                "status": "error",
                "message": "Parameter validation failed",
                "errors": errors,
                "error_count": len(errors)
            }), 400

        # 示例业务处理（可替换实际逻辑）
        processed['vector_magnitude'] = sum(x**2 for x in processed['ini_pos'])**0.5
        
        return jsonify({
            "status": "success",
            "received": processed,
            "validation": {
                "parameter_count": len(processed),
                "vector_dimensions": len(processed['ini_pos'])
            }
        }), 200

    except BadRequest as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"Server error: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    
@api.route('/antenna', methods=['POST'])
def handle_antenna_config():
    # 尝试解析JSON请求体
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
    except Exception as e:
        return jsonify({"error": "Invalid JSON format"}), 400

    # 校验天线类型参数
    antenna_type = data.get('antenna_type')
    valid_types = ['uniform_linear', 'uniform_plane', 'cylindrical']
    if not antenna_type or antenna_type not in valid_types:
        return jsonify({
            "error": "Invalid antenna type",
            "valid_types": valid_types,
            "received": antenna_type
        }), 400

    # 定义数值型参数列表
    numeric_params = [
        'num_per_row',      # 每行单元数
        'num_per_col',      # 每列单元数
        'spacing_row',      # 行间距（单位：波长）
        'spacing_col',      # 列间距（单位：波长）
        'rotate_z',         # Z轴旋转角度（度）
        'rotate_y',         # Y轴旋转角度（度） 
        'rotate_x'          # X轴旋转角度（度）
    ]

    # 数值参数校验
    params = {}
    try:
        for param in numeric_params:
            value = data[param]
            # 双重类型校验
            if not isinstance(value, (int, float)):
                raise ValueError
            params[param] = float(value)
    except KeyError as e:
        return jsonify({
            "error": f"Missing required parameter: {e.args[0]}"
        }), 400
    except ValueError:
        return jsonify({
            "error": f"Invalid value for parameter {param}. Must be numeric."
        }), 400

    # 天线名称
    antenna_name = data.get('name')
   

    # 此处添加实际的天线配置处理逻辑
  

    # 返回成功响应
    return jsonify({
        "status": "Configuration received",
        "antenna_type": antenna_type,
        "antenna_name": antenna_name,
        "parameters": params
    }), 200



