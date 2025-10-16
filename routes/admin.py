from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """管理员权限装饰器"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('需要管理员权限', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    from flask import current_app
    data_manager = current_app.data_manager
    
    users = data_manager.get_all_users()
    roles = data_manager.get_all_roles()
    
    return render_template('admin/users.html', users=users, roles=roles)

@admin_bp.route('/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    from flask import current_app
    data_manager = current_app.data_manager
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    province = request.form.get('province')
    department = request.form.get('department')
    
    # 检查用户名是否存在
    if data_manager.get_user_by_username(username):
        flash('用户名已存在', 'error')
        return redirect(url_for('admin.users'))
    
    data_manager.create_user(
        username=username,
        email=email,
        password=password,
        role=role,
        province=province,
        department=department
    )
    
    data_manager.add_system_log(
        current_user.id,
        'create_user',
        f'创建用户: {username}'
    )
    
    flash('用户创建成功', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<user_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    email = request.form.get('email')
    role = request.form.get('role')
    province = request.form.get('province')
    department = request.form.get('department')
    is_active = request.form.get('is_active') == 'true'
    
    data_manager.update_user(
        user_id,
        email=email,
        role=role,
        province=province,
        department=department,
        is_active=is_active
    )
    
    data_manager.add_system_log(
        current_user.id,
        'update_user',
        f'更新用户: {user_id}'
    )
    
    flash('用户更新成功', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': '不能删除自己'})
    
    data_manager.delete_user(user_id)
    data_manager.add_system_log(
        current_user.id,
        'delete_user',
        f'删除用户: {user_id}'
    )
    
    return jsonify({'success': True, 'message': '删除成功'})

@admin_bp.route('/users/<user_id>/reset-password', methods=['POST'])
@login_required
@admin_required
def reset_password(user_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    new_password = request.form.get('new_password', '123456')
    
    data_manager.update_user(
        user_id,
        password_hash=generate_password_hash(new_password)
    )
    
    data_manager.add_system_log(
        current_user.id,
        'reset_password',
        f'重置用户密码: {user_id}'
    )
    
    return jsonify({'success': True, 'message': '密码重置成功'})

@admin_bp.route('/logs')
@login_required
@admin_required
def logs():
    from flask import current_app
    data_manager = current_app.data_manager
    
    limit = int(request.args.get('limit', 100))
    logs = data_manager.get_system_logs(limit=limit)
    logs.reverse()  # 最新的在前
    
    return render_template('admin/logs.html', logs=logs)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def settings():
    if request.method == 'POST':
        # 这里可以保存系统设置
        flash('设置保存成功', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html')

