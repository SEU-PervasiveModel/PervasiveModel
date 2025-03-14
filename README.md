# SRTP 项目

本项目是一个基于 Flask 的 Web 应用，主要功能包括用户注册、登录和调用 MATLAB 引擎计算。项目同时使用 Flask-SQLAlchemy 进行数据库操作，Flask-Migrate 管理数据库迁移，以及 Flask-CORS 解决跨域问题。

## 项目结构

```
srtp/
├── .env                          # 环境变量配置文件
├── app.py                        # 应用入口，启动 Flask 应用
├── requirements.txt              # 项目依赖列表
├── migrations/                   # 数据库迁移相关文件（使用 Flask-Migrate/Alembic）
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── 1bf35f7c7960_update_password_hash_column_length.py
└── backend/                      # 后端代码目录
    ├── __init__.py               # 应用工厂，创建应用、注册路由、初始化扩展
    ├── config.py                 # 应用配置（数据库连接、密钥等）
    ├── extensions.py             # 初始化扩展（数据库、CORS）
    ├── models.py                 # 数据模型定义
    ├── routes.py                 # API 路由定义（用户注册、登录、MATLAB 计算接口）
    └── matlab/                   # MATLAB 相关模块
        ├── __init__.py           # MATLAB 模块初始化
        ├── engine.py             # MATLAB 引擎封装，管理 MATLAB 引擎的启动与关闭
        └── scripts/              # MATLAB 脚本目录
            ├── compute.m         # MATLAB 示例脚本（计算平方）
            └── my_matlab_script.m  # MATLAB 示例脚本（计算平方）
```

## 环境配置

- 在项目根目录中创建一个 `.env` 文件，用于配置数据库及密钥信息，例如：

  ```
  DB_HOST=localhost
  DB_USER=root
  DB_PASSWORD=your_password
  DB_NAME=myapp
  SECRET_KEY=your_secret_key
  ```

- 安装依赖：

  ```bash
  pip install -r requirements.txt
  ```

## 数据库迁移

项目使用 Flask-Migrate 进行数据库迁移。常用命令：

1. 初始化迁移目录（首次使用时执行）：

   ```bash
   flask db init
   ```

2. 生成迁移文件（例如修改 `password_hash` 字段长度后）：

   ```bash
   flask db migrate -m "Update password_hash column length"
   ```

3. 应用迁移到数据库：

   ```bash
   flask db upgrade
   ```

## 启动项目

在命令行中运行：

```bash
python app.py
```

或设置环境变量后使用 Flask 自带的运行命令：

```bash
set FLASK_APP=app.py       # Windows CMD
$env:FLASK_APP = "app.py"    # Windows PowerShell
flask run
```

## MATLAB 引擎

- 项目中集成了 MATLAB 引擎，通过 `backend/matlab/engine.py` 实现。
- MATLAB 脚本存放在 `backend/matlab/scripts/` 下，例如 `compute.m` 和 `my_matlab_script.m`。
- 应用启动时会自动初始化 MATLAB 引擎，并在应用退出时关闭引擎。

## API 接口

- `/api/matlab-compute`：接受 POST 请求，调用 MATLAB 计算函数。
- `/api/register`：用户注册接口，接收 `username`、`password`（加密存储）及可选的 `email`。
- `/api/login`：用户登录接口，验证用户名与密码。

## 备注

- 请确保 MATLAB 引擎和 MATLAB 脚本路径配置正确。
- 根据需求调整配置及错误处理逻辑。
- 使用调试模式启动时，Flask 会自动重载代码修改。

---

希望本项目对你有所帮助！
