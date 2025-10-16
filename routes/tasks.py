from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
@login_required
def index():
    from flask import current_app
    data_manager = current_app.data_manager
    
    tasks = data_manager.get_all_tasks()
    
    # 根据角色过滤
    if current_user.role == 'staff':
        tasks = [t for t in tasks if t.get('assigned_to') == current_user.id]
    elif current_user.role == 'province_manager':
        tasks = [t for t in tasks if t.get('province') == current_user.province]
    
    # 排序
    tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('tasks/list.html', tasks=tasks)

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from flask import current_app
    data_manager = current_app.data_manager
    
    if current_user.role not in ['admin', 'province_manager']:
        flash('无权限创建任务', 'error')
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        task_type = request.form.get('task_type')
        priority = request.form.get('priority')
        assigned_to = request.form.get('assigned_to')
        province = request.form.get('province')
        
        # 自动派单逻辑（如果未指定）
        if not assigned_to and province:
            # 查找该省的可用人员
            users = data_manager.get_all_users()
            available_users = [u for u in users if u.province == province and u.role == 'staff']
            if available_users:
                # 简单的轮询分配
                assigned_to = available_users[0].id
        
        task = data_manager.create_task(
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            creator_id=current_user.id,
            assigned_to=assigned_to,
            province=province
        )
        
        data_manager.add_system_log(
            current_user.id,
            'create_task',
            f'创建任务: {title}'
        )
        
        flash('任务创建成功', 'success')
        return redirect(url_for('tasks.index'))
    
    # 获取用户和省份列表
    users = data_manager.get_all_users()
    provinces = list(set([u.province for u in users if u.province]))
    
    return render_template('tasks/create.html', users=users, provinces=provinces)

@tasks_bp.route('/<task_id>')
@login_required
def detail(task_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    tasks = data_manager.get_all_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        flash('任务不存在', 'error')
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/detail.html', task=task)

@tasks_bp.route('/<task_id>/add-log', methods=['POST'])
@login_required
def add_log(task_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    log_content = request.form.get('log_content')
    
    data_manager.add_task_log(task_id, current_user.id, log_content)
    data_manager.add_system_log(
        current_user.id,
        'add_task_log',
        f'添加任务日志: {task_id}'
    )
    
    flash('日志添加成功', 'success')
    return redirect(url_for('tasks.detail', task_id=task_id))

@tasks_bp.route('/<task_id>/update-status', methods=['POST'])
@login_required
def update_status(task_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    status = request.form.get('status')
    
    update_data = {'status': status}
    if status == 'completed':
        from datetime import datetime
        update_data['completed_at'] = datetime.now().isoformat()
    elif status == 'verified':
        from datetime import datetime
        update_data['verified_at'] = datetime.now().isoformat()
    
    data_manager.update_task(task_id, **update_data)
    data_manager.add_system_log(
        current_user.id,
        'update_task_status',
        f'更新任务 {task_id} 状态为 {status}'
    )
    
    return jsonify({'success': True, 'message': '状态更新成功'})

@tasks_bp.route('/<task_id>/reassign', methods=['POST'])
@login_required
def reassign(task_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    if current_user.role not in ['admin', 'province_manager']:
        return jsonify({'success': False, 'message': '无权限重新分配'})
    
    assigned_to = request.form.get('assigned_to')
    
    data_manager.update_task(task_id, assigned_to=assigned_to, status='assigned')
    data_manager.add_system_log(
        current_user.id,
        'reassign_task',
        f'重新分配任务 {task_id} 给 {assigned_to}'
    )
    
    return jsonify({'success': True, 'message': '重新分配成功'})

