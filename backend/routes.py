from flask import Blueprint, request, jsonify
from backend.models import User
from backend.extensions import db
from backend.matlab.engine import matlab_engine  # 新增
import matlab

from flask import Blueprint, request, jsonify
from backend.matlab.engine import matlab_engine
import matlab
import traceback

api = Blueprint('api', __name__)

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