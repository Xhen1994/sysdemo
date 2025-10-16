from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        from flask import current_app
        data_manager = current_app.data_manager
        
        user = data_manager.get_user_by_username(username)
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            data_manager.add_system_log(user.id, 'login', f'用户 {username} 登录系统')
            return redirect(url_for('dashboard.index'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    from flask import current_app
    data_manager = current_app.data_manager
    data_manager.add_system_log(current_user.id, 'logout', f'用户 {current_user.username} 退出系统')
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    from flask import current_app
    from werkzeug.security import generate_password_hash
    
    data_manager = current_app.data_manager
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    
    if check_password_hash(current_user.password_hash, old_password):
        data_manager.update_user(
            current_user.id, 
            password_hash=generate_password_hash(new_password)
        )
        flash('密码修改成功', 'success')
    else:
        flash('原密码错误', 'error')
    
    return redirect(url_for('dashboard.index'))

