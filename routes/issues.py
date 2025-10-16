from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from services.ai_service import AIService

issues_bp = Blueprint('issues', __name__, url_prefix='/issues')

@issues_bp.route('/')
@login_required
def index():
    from flask import current_app
    data_manager = current_app.data_manager
    
    issues = data_manager.get_all_issues()
    
    # 根据角色过滤
    if current_user.role == 'staff':
        issues = [issue for issue in issues if issue['submitter_id'] == current_user.id]
    elif current_user.role == 'province_manager':
        issues = [issue for issue in issues if issue['province'] == current_user.province]
    
    # 排序（最新的在前）
    issues.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('issues/list.html', issues=issues)

@issues_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from flask import current_app
    data_manager = current_app.data_manager
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        priority = request.form.get('priority')
        
        issue = data_manager.create_issue(
            title=title,
            description=description,
            category=category,
            priority=priority,
            submitter_id=current_user.id,
            province=current_user.province
        )
        
        data_manager.add_system_log(
            current_user.id,
            'create_issue',
            f'创建问题: {title}'
        )
        
        flash('问题提交成功', 'success')
        return redirect(url_for('issues.index'))
    
    return render_template('issues/create.html')

@issues_bp.route('/<issue_id>')
@login_required
def detail(issue_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    issues = data_manager.get_all_issues()
    issue = next((i for i in issues if i['id'] == issue_id), None)
    
    if not issue:
        flash('问题不存在', 'error')
        return redirect(url_for('issues.index'))
    
    return render_template('issues/detail.html', issue=issue)

@issues_bp.route('/<issue_id>/comment', methods=['POST'])
@login_required
def add_comment(issue_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    comment = request.form.get('comment')
    
    data_manager.add_issue_comment(issue_id, current_user.id, comment)
    data_manager.add_system_log(
        current_user.id,
        'comment_issue',
        f'评论问题: {issue_id}'
    )
    
    flash('评论添加成功', 'success')
    return redirect(url_for('issues.detail', issue_id=issue_id))

@issues_bp.route('/<issue_id>/assign', methods=['POST'])
@login_required
def assign(issue_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    if current_user.role not in ['admin', 'province_manager']:
        return jsonify({'success': False, 'message': '无权限分配'})
    
    assigned_to = request.form.get('assigned_to')
    
    data_manager.update_issue(issue_id, assigned_to=assigned_to, status='assigned')
    data_manager.add_system_log(
        current_user.id,
        'assign_issue',
        f'分配问题 {issue_id} 给 {assigned_to}'
    )
    
    return jsonify({'success': True, 'message': '分配成功'})

@issues_bp.route('/<issue_id>/update-status', methods=['POST'])
@login_required
def update_status(issue_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    status = request.form.get('status')
    
    data_manager.update_issue(issue_id, status=status)
    data_manager.add_system_log(
        current_user.id,
        'update_issue_status',
        f'更新问题 {issue_id} 状态为 {status}'
    )
    
    return jsonify({'success': True, 'message': '状态更新成功'})

@issues_bp.route('/ai-summary', methods=['POST'])
@login_required
def ai_summary():
    from flask import current_app
    
    if current_user.role not in ['admin', 'province_manager']:
        return jsonify({'success': False, 'message': '无权限使用AI功能'})
    
    data_manager = current_app.data_manager
    issues = data_manager.get_all_issues()
    
    # 过滤要总结的问题
    filter_province = request.form.get('province')
    filter_category = request.form.get('category')
    filter_status = request.form.get('status')
    
    filtered_issues = issues
    if filter_province:
        filtered_issues = [i for i in filtered_issues if i.get('province') == filter_province]
    if filter_category:
        filtered_issues = [i for i in filtered_issues if i.get('category') == filter_category]
    if filter_status:
        filtered_issues = [i for i in filtered_issues if i.get('status') == filter_status]
    
    # 调用AI服务
    ai_service = AIService(current_app.config['DEEPSEEK_API_KEY'])
    summary = ai_service.summarize_issues(filtered_issues)
    
    data_manager.add_system_log(
        current_user.id,
        'ai_summary',
        f'生成问题AI总结，共 {len(filtered_issues)} 条'
    )
    
    return jsonify({'success': True, 'summary': summary})

