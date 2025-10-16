from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime

objectives_bp = Blueprint('objectives', __name__, url_prefix='/objectives')

@objectives_bp.route('/')
@login_required
def index():
    from flask import current_app
    data_manager = current_app.data_manager
    
    objectives = data_manager.get_all_objectives()
    
    # 根据用户角色过滤目标
    if current_user.role == 'staff':
        objectives = [obj for obj in objectives if obj['target_user'] == current_user.id]
    elif current_user.role == 'province_manager':
        objectives = [obj for obj in objectives if obj['target_province'] == current_user.province]
    
    return render_template('objectives/list.html', objectives=objectives)

@objectives_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from flask import current_app
    data_manager = current_app.data_manager
    
    if current_user.role not in ['admin', 'province_manager']:
        flash('无权限创建目标', 'error')
        return redirect(url_for('objectives.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        target_province = request.form.get('target_province')
        target_user = request.form.get('target_user')
        deadline = request.form.get('deadline')
        parent_id = request.form.get('parent_id')
        
        objective = data_manager.create_objective(
            title=title,
            description=description,
            target_province=target_province,
            target_user=target_user,
            deadline=deadline,
            creator_id=current_user.id,
            parent_id=parent_id
        )
        
        data_manager.add_system_log(
            current_user.id, 
            'create_objective', 
            f'创建目标: {title}'
        )
        
        flash('目标创建成功', 'success')
        return redirect(url_for('objectives.index'))
    
    # 获取可选的用户和省份
    users = data_manager.get_all_users()
    provinces = list(set([u.province for u in users if u.province]))
    parent_objectives = data_manager.get_all_objectives()
    
    return render_template('objectives/create.html', 
                         users=users, 
                         provinces=provinces,
                         parent_objectives=parent_objectives)

@objectives_bp.route('/<objective_id>')
@login_required
def detail(objective_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    objective = data_manager.get_objective_by_id(objective_id)
    if not objective:
        flash('目标不存在', 'error')
        return redirect(url_for('objectives.index'))
    
    # 获取子目标
    all_objectives = data_manager.get_all_objectives()
    sub_objectives = [obj for obj in all_objectives if obj.get('parent_id') == objective_id]
    
    return render_template('objectives/detail.html', 
                         objective=objective,
                         sub_objectives=sub_objectives)

@objectives_bp.route('/<objective_id>/update-progress', methods=['POST'])
@login_required
def update_progress(objective_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    objective = data_manager.get_objective_by_id(objective_id)
    if not objective:
        return jsonify({'success': False, 'message': '目标不存在'})
    
    progress = int(request.form.get('progress', 0))
    status = request.form.get('status', 'in_progress')
    
    data_manager.update_objective(objective_id, progress=progress, status=status)
    data_manager.add_system_log(
        current_user.id,
        'update_objective_progress',
        f'更新目标进度: {objective["title"]} -> {progress}%'
    )
    
    return jsonify({'success': True, 'message': '进度更新成功'})

@objectives_bp.route('/<objective_id>/approve', methods=['POST'])
@login_required
def approve(objective_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    if current_user.role not in ['admin', 'province_manager']:
        return jsonify({'success': False, 'message': '无权限审核'})
    
    objective = data_manager.get_objective_by_id(objective_id)
    if not objective:
        return jsonify({'success': False, 'message': '目标不存在'})
    
    approved = request.form.get('approved') == 'true'
    comment = request.form.get('comment', '')
    
    if approved:
        data_manager.update_objective(objective_id, status='completed')
        message = '目标审核通过'
    else:
        data_manager.update_objective(objective_id, status='in_progress')
        message = '目标审核未通过'
    
    data_manager.add_system_log(
        current_user.id,
        'approve_objective',
        f'{message}: {objective["title"]}, 评论: {comment}'
    )
    
    return jsonify({'success': True, 'message': message})

