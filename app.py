from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json

from config import Config
from models.data_manager import DataManager
from models.user import User
from routes import register_routes

# 创建应用实例
app = Flask(__name__)
app.config.from_object(Config)

# 跨域配置
CORS(app)

# 登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# 初始化数据管理器
data_manager = DataManager(app.config['DATA_DIR'])

@login_manager.user_loader
def load_user(user_id):
    return data_manager.get_user_by_id(user_id)

# 注册所有路由
register_routes(app, data_manager)

# 主页路由
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 确保数据目录存在
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化数据
    data_manager.init_data()
    
    # 启动应用
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

