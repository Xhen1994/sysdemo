from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from collections import Counter

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    from flask import current_app
    data_manager = current_app.data_manager
    
    # 获取统计数据
    stats = get_statistics(data_manager, current_user)
    
    return render_template('dashboard/index.html', stats=stats)

@dashboard_bp.route('/api/stats')
@login_required
def api_stats():
    from flask import current_app
    data_manager = current_app.data_manager
    
    stats = get_statistics(data_manager, current_user)
    return jsonify(stats)

@dashboard_bp.route('/api/objective-chart')
@login_required
def objective_chart():
    from flask import current_app
    data_manager = current_app.data_manager
    
    objectives = data_manager.get_all_objectives()
    
    # 根据角色过滤
    if current_user.role == 'staff':
        objectives = [obj for obj in objectives if obj['target_user'] == current_user.id]
    elif current_user.role == 'province_manager':
        objectives = [obj for obj in objectives if obj['target_province'] == current_user.province]
    
    # 按状态统计
    status_count = Counter([obj['status'] for obj in objectives])
    
    return jsonify({
        'labels': list(status_count.keys()),
        'data': list(status_count.values())
    })

@dashboard_bp.route('/api/issue-chart')
@login_required
def issue_chart():
    from flask import current_app
    data_manager = current_app.data_manager
    
    issues = data_manager.get_all_issues()
    
    # 根据角色过滤
    if current_user.role == 'staff':
        issues = [i for i in issues if i['submitter_id'] == current_user.id]
    elif current_user.role == 'province_manager':
        issues = [i for i in issues if i['province'] == current_user.province]
    
    # 按类别统计
    category_count = Counter([i['category'] for i in issues])
    
    return jsonify({
        'labels': list(category_count.keys()),
        'data': list(category_count.values())
    })

@dashboard_bp.route('/api/task-distribution')
@login_required
def task_distribution():
    from flask import current_app
    data_manager = current_app.data_manager
    
    tasks = data_manager.get_all_tasks()
    
    # 根据角色过滤
    if current_user.role == 'province_manager':
        tasks = [t for t in tasks if t.get('province') == current_user.province]
    
    # 按省份统计
    province_count = Counter([t.get('province', '未分配') for t in tasks])
    
    return jsonify({
        'labels': list(province_count.keys()),
        'data': list(province_count.values())
    })

def get_statistics(data_manager, user):
    """获取统计数据"""
    objectives = data_manager.get_all_objectives()
    issues = data_manager.get_all_issues()
    tasks = data_manager.get_all_tasks()
    
    # 根据角色过滤
    if user.role == 'staff':
        objectives = [obj for obj in objectives if obj['target_user'] == user.id]
        issues = [i for i in issues if i['submitter_id'] == user.id]
        tasks = [t for t in tasks if t.get('assigned_to') == user.id]
    elif user.role == 'province_manager':
        objectives = [obj for obj in objectives if obj['target_province'] == user.province]
        issues = [i for i in issues if i['province'] == user.province]
        tasks = [t for t in tasks if t.get('province') == user.province]
    
    # 计算统计数据
    stats = {
        'total_objectives': len(objectives),
        'completed_objectives': len([o for o in objectives if o['status'] == 'completed']),
        'pending_objectives': len([o for o in objectives if o['status'] == 'pending']),
        'in_progress_objectives': len([o for o in objectives if o['status'] == 'in_progress']),
        'total_issues': len(issues),
        'open_issues': len([i for i in issues if i['status'] == 'open']),
        'resolved_issues': len([i for i in issues if i['status'] == 'resolved']),
        'closed_issues': len([i for i in issues if i['status'] == 'closed']),
        'total_tasks': len(tasks),
        'pending_tasks': len([t for t in tasks if t['status'] == 'pending']),
        'in_progress_tasks': len([t for t in tasks if t['status'] == 'in_progress']),
        'completed_tasks': len([t for t in tasks if t['status'] == 'completed']),
        'verified_tasks': len([t for t in tasks if t['status'] == 'verified']),
    }
    
    # 计算完成率
    if stats['total_objectives'] > 0:
        stats['objective_completion_rate'] = round(
            stats['completed_objectives'] / stats['total_objectives'] * 100, 1
        )
    else:
        stats['objective_completion_rate'] = 0
    
    if stats['total_issues'] > 0:
        stats['issue_resolution_rate'] = round(
            (stats['resolved_issues'] + stats['closed_issues']) / stats['total_issues'] * 100, 1
        )
    else:
        stats['issue_resolution_rate'] = 0
    
    if stats['total_tasks'] > 0:
        stats['task_completion_rate'] = round(
            (stats['completed_tasks'] + stats['verified_tasks']) / stats['total_tasks'] * 100, 1
        )
    else:
        stats['task_completion_rate'] = 0
    
    return stats

