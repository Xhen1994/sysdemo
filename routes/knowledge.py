from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import markdown

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')

@knowledge_bp.route('/')
@login_required
def index():
    from flask import current_app
    data_manager = current_app.data_manager
    
    knowledge_list = data_manager.get_all_knowledge()
    
    # 搜索和过滤
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    if search:
        knowledge_list = [k for k in knowledge_list 
                         if search.lower() in k['title'].lower() 
                         or search.lower() in k['content'].lower()]
    
    if category:
        knowledge_list = [k for k in knowledge_list if k['category'] == category]
    
    # 排序
    knowledge_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    # 获取所有分类
    all_knowledge = data_manager.get_all_knowledge()
    categories = list(set([k['category'] for k in all_knowledge]))
    
    return render_template('knowledge/list.html', 
                         knowledge_list=knowledge_list,
                         categories=categories)

@knowledge_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from flask import current_app
    data_manager = current_app.data_manager
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags', '').split(',')
        tags = [t.strip() for t in tags if t.strip()]
        
        knowledge = data_manager.create_knowledge(
            title=title,
            content=content,
            category=category,
            author_id=current_user.id,
            tags=tags
        )
        
        data_manager.add_system_log(
            current_user.id,
            'create_knowledge',
            f'创建知识: {title}'
        )
        
        flash('知识创建成功', 'success')
        return redirect(url_for('knowledge.index'))
    
    return render_template('knowledge/create.html')

@knowledge_bp.route('/<knowledge_id>')
@login_required
def detail(knowledge_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    knowledge_list = data_manager.get_all_knowledge()
    knowledge = next((k for k in knowledge_list if k['id'] == knowledge_id), None)
    
    if not knowledge:
        flash('知识不存在', 'error')
        return redirect(url_for('knowledge.index'))
    
    # 增加浏览次数
    data_manager.update_knowledge(knowledge_id, views=knowledge.get('views', 0) + 1)
    
    # 转换Markdown
    knowledge['html_content'] = markdown.markdown(knowledge['content'])
    
    return render_template('knowledge/detail.html', knowledge=knowledge)

@knowledge_bp.route('/<knowledge_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(knowledge_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    knowledge_list = data_manager.get_all_knowledge()
    knowledge = next((k for k in knowledge_list if k['id'] == knowledge_id), None)
    
    if not knowledge:
        flash('知识不存在', 'error')
        return redirect(url_for('knowledge.index'))
    
    # 检查权限
    if current_user.role not in ['admin'] and knowledge['author_id'] != current_user.id:
        flash('无权限编辑', 'error')
        return redirect(url_for('knowledge.detail', knowledge_id=knowledge_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags', '').split(',')
        tags = [t.strip() for t in tags if t.strip()]
        
        data_manager.update_knowledge(
            knowledge_id,
            title=title,
            content=content,
            category=category,
            tags=tags
        )
        
        data_manager.add_system_log(
            current_user.id,
            'update_knowledge',
            f'更新知识: {title}'
        )
        
        flash('知识更新成功', 'success')
        return redirect(url_for('knowledge.detail', knowledge_id=knowledge_id))
    
    return render_template('knowledge/edit.html', knowledge=knowledge)

@knowledge_bp.route('/<knowledge_id>/delete', methods=['POST'])
@login_required
def delete(knowledge_id):
    from flask import current_app
    data_manager = current_app.data_manager
    
    knowledge_list = data_manager.get_all_knowledge()
    knowledge = next((k for k in knowledge_list if k['id'] == knowledge_id), None)
    
    if not knowledge:
        return jsonify({'success': False, 'message': '知识不存在'})
    
    # 检查权限
    if current_user.role not in ['admin'] and knowledge['author_id'] != current_user.id:
        return jsonify({'success': False, 'message': '无权限删除'})
    
    data_manager.delete_knowledge(knowledge_id)
    data_manager.add_system_log(
        current_user.id,
        'delete_knowledge',
        f'删除知识: {knowledge["title"]}'
    )
    
    return jsonify({'success': True, 'message': '删除成功'})

