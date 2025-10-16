import os
import json
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

class DataManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.roles_file = os.path.join(data_dir, 'roles.json')
        self.objectives_file = os.path.join(data_dir, 'objectives.json')
        self.issues_file = os.path.join(data_dir, 'issues.jsonl')
        self.tasks_file = os.path.join(data_dir, 'tasks.jsonl')
        self.knowledge_file = os.path.join(data_dir, 'knowledge.json')
        self.logs_file = os.path.join(data_dir, 'system_logs.jsonl')
    
    def init_data(self):
        """初始化数据文件"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化用户数据
        if not os.path.exists(self.users_file):
            default_users = [
                {
                    'id': str(uuid.uuid4()),
                    'username': 'admin',
                    'email': 'admin@sysdemo.com',
                    'password_hash': generate_password_hash('admin123'),
                    'role': 'admin',
                    'province': None,
                    'department': '系统管理部',
                    'created_at': datetime.now().isoformat(),
                    'is_active': True
                }
            ]
            self._write_json(self.users_file, default_users)
        
        # 初始化角色数据
        if not os.path.exists(self.roles_file):
            default_roles = [
                {
                    'id': 'admin',
                    'name': '系统管理员',
                    'permissions': ['all']
                },
                {
                    'id': 'province_manager',
                    'name': '省级管理员',
                    'permissions': ['view_all', 'manage_province', 'create_objective', 'assign_task']
                },
                {
                    'id': 'staff',
                    'name': '普通员工',
                    'permissions': ['view_own', 'report_progress', 'submit_issue', 'view_knowledge']
                }
            ]
            self._write_json(self.roles_file, default_roles)
        
        # 初始化其他数据文件
        for file in [self.objectives_file, self.knowledge_file]:
            if not os.path.exists(file):
                self._write_json(file, [])
        
        for file in [self.issues_file, self.tasks_file, self.logs_file]:
            if not os.path.exists(file):
                open(file, 'w').close()
    
    def _read_json(self, filepath):
        """读取JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_json(self, filepath, data):
        """写入JSON文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _read_jsonl(self, filepath):
        """读取JSONL文件"""
        data = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
        except FileNotFoundError:
            pass
        return data
    
    def _append_jsonl(self, filepath, data):
        """追加到JSONL文件"""
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _update_jsonl(self, filepath, data_list):
        """更新JSONL文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for data in data_list:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    # 用户管理
    def get_all_users(self):
        """获取所有用户"""
        users_data = self._read_json(self.users_file)
        users = []
        for u in users_data:
            try:
                # 确保必要字段存在
                if 'is_active' not in u:
                    u['is_active'] = True
                users.append(User.from_dict(u))
            except Exception as e:
                print(f"Error loading user {u.get('username', 'unknown')}: {e}")
                continue
        return users
    
    def get_user_by_id(self, user_id):
        """根据ID获取用户"""
        users_data = self._read_json(self.users_file)
        for user in users_data:
            if user['id'] == user_id:
                # 确保必要字段存在
                if 'is_active' not in user:
                    user['is_active'] = True
                return User.from_dict(user)
        return None
    
    def get_user_by_username(self, username):
        """根据用户名获取用户"""
        users_data = self._read_json(self.users_file)
        for user in users_data:
            if user['username'] == username:
                # 确保必要字段存在
                if 'is_active' not in user:
                    user['is_active'] = True
                return User.from_dict(user)
        return None
    
    def create_user(self, username, email, password, role, province=None, department=None):
        """创建用户"""
        users_data = self._read_json(self.users_file)
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,
            'province': province,
            'department': department,
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        users_data.append(new_user)
        self._write_json(self.users_file, users_data)
        return User.from_dict(new_user)
    
    def update_user(self, user_id, **kwargs):
        """更新用户"""
        users_data = self._read_json(self.users_file)
        for user in users_data:
            if user['id'] == user_id:
                # 更新所有提供的字段（不再检查是否已存在）
                for key, value in kwargs.items():
                    user[key] = value
                # 确保关键字段存在
                if 'is_active' not in user:
                    user['is_active'] = True
                self._write_json(self.users_file, users_data)
                return True
        return False
    
    def delete_user(self, user_id):
        """删除用户"""
        users_data = self._read_json(self.users_file)
        users_data = [u for u in users_data if u['id'] != user_id]
        self._write_json(self.users_file, users_data)
    
    # 角色管理
    def get_all_roles(self):
        """获取所有角色"""
        return self._read_json(self.roles_file)
    
    # 目标管理
    def get_all_objectives(self):
        """获取所有目标"""
        return self._read_json(self.objectives_file)
    
    def create_objective(self, title, description, target_province, target_user, 
                        deadline, creator_id, parent_id=None):
        """创建目标"""
        objectives = self._read_json(self.objectives_file)
        new_objective = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'target_province': target_province,
            'target_user': target_user,
            'deadline': deadline,
            'creator_id': creator_id,
            'parent_id': parent_id,
            'status': 'pending',  # pending, in_progress, completed, overdue
            'progress': 0,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'sub_objectives': []
        }
        objectives.append(new_objective)
        self._write_json(self.objectives_file, objectives)
        return new_objective
    
    def update_objective(self, objective_id, **kwargs):
        """更新目标"""
        objectives = self._read_json(self.objectives_file)
        for obj in objectives:
            if obj['id'] == objective_id:
                for key, value in kwargs.items():
                    if key in obj:
                        obj[key] = value
                obj['updated_at'] = datetime.now().isoformat()
                self._write_json(self.objectives_file, objectives)
                return True
        return False
    
    def get_objective_by_id(self, objective_id):
        """根据ID获取目标"""
        objectives = self._read_json(self.objectives_file)
        for obj in objectives:
            if obj['id'] == objective_id:
                return obj
        return None
    
    # 问题反馈管理
    def get_all_issues(self):
        """获取所有问题"""
        return self._read_jsonl(self.issues_file)
    
    def create_issue(self, title, description, category, priority, submitter_id, province):
        """创建问题"""
        new_issue = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'category': category,  # bug, feature, improvement, question
            'priority': priority,  # low, medium, high, urgent
            'status': 'open',  # open, assigned, in_progress, resolved, closed
            'submitter_id': submitter_id,
            'province': province,
            'assigned_to': None,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'comments': []
        }
        self._append_jsonl(self.issues_file, new_issue)
        return new_issue
    
    def update_issue(self, issue_id, **kwargs):
        """更新问题"""
        issues = self._read_jsonl(self.issues_file)
        for issue in issues:
            if issue['id'] == issue_id:
                for key, value in kwargs.items():
                    if key in issue:
                        issue[key] = value
                issue['updated_at'] = datetime.now().isoformat()
                self._update_jsonl(self.issues_file, issues)
                return True
        return False
    
    def add_issue_comment(self, issue_id, user_id, comment):
        """添加问题评论"""
        issues = self._read_jsonl(self.issues_file)
        for issue in issues:
            if issue['id'] == issue_id:
                issue['comments'].append({
                    'id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'comment': comment,
                    'created_at': datetime.now().isoformat()
                })
                issue['updated_at'] = datetime.now().isoformat()
                self._update_jsonl(self.issues_file, issues)
                return True
        return False
    
    # 任务管理（工作流）
    def get_all_tasks(self):
        """获取所有任务"""
        return self._read_jsonl(self.tasks_file)
    
    def create_task(self, title, description, task_type, priority, creator_id, 
                    assigned_to=None, province=None):
        """创建任务"""
        new_task = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'task_type': task_type,  # support, maintenance, deployment, other
            'priority': priority,
            'status': 'pending',  # pending, assigned, in_progress, completed, verified
            'creator_id': creator_id,
            'assigned_to': assigned_to,
            'province': province,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'logs': [],
            'completed_at': None,
            'verified_at': None
        }
        self._append_jsonl(self.tasks_file, new_task)
        return new_task
    
    def update_task(self, task_id, **kwargs):
        """更新任务"""
        tasks = self._read_jsonl(self.tasks_file)
        for task in tasks:
            if task['id'] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                task['updated_at'] = datetime.now().isoformat()
                self._update_jsonl(self.tasks_file, tasks)
                return True
        return False
    
    def add_task_log(self, task_id, user_id, log_content):
        """添加任务日志"""
        tasks = self._read_jsonl(self.tasks_file)
        for task in tasks:
            if task['id'] == task_id:
                task['logs'].append({
                    'id': str(uuid.uuid4()),
                    'user_id': user_id,
                    'content': log_content,
                    'created_at': datetime.now().isoformat()
                })
                task['updated_at'] = datetime.now().isoformat()
                self._update_jsonl(self.tasks_file, tasks)
                return True
        return False
    
    # 知识库管理
    def get_all_knowledge(self):
        """获取所有知识"""
        return self._read_json(self.knowledge_file)
    
    def create_knowledge(self, title, content, category, author_id, tags=None):
        """创建知识"""
        knowledge_list = self._read_json(self.knowledge_file)
        new_knowledge = {
            'id': str(uuid.uuid4()),
            'title': title,
            'content': content,
            'category': category,
            'author_id': author_id,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'views': 0
        }
        knowledge_list.append(new_knowledge)
        self._write_json(self.knowledge_file, knowledge_list)
        return new_knowledge
    
    def update_knowledge(self, knowledge_id, **kwargs):
        """更新知识"""
        knowledge_list = self._read_json(self.knowledge_file)
        for knowledge in knowledge_list:
            if knowledge['id'] == knowledge_id:
                for key, value in kwargs.items():
                    if key in knowledge:
                        knowledge[key] = value
                knowledge['updated_at'] = datetime.now().isoformat()
                self._write_json(self.knowledge_file, knowledge_list)
                return True
        return False
    
    def delete_knowledge(self, knowledge_id):
        """删除知识"""
        knowledge_list = self._read_json(self.knowledge_file)
        knowledge_list = [k for k in knowledge_list if k['id'] != knowledge_id]
        self._write_json(self.knowledge_file, knowledge_list)
    
    # 系统日志
    def add_system_log(self, user_id, action, details):
        """添加系统日志"""
        log_entry = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self._append_jsonl(self.logs_file, log_entry)
    
    def get_system_logs(self, limit=100):
        """获取系统日志"""
        logs = self._read_jsonl(self.logs_file)
        return logs[-limit:] if len(logs) > limit else logs

