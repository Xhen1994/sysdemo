import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 4000
    DEBUG = False
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY') or ''
    DEEPSEEK_API_BASE = 'https://api.deepseek.com/v1'
    
    # 数据存储路径
    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    ROLES_FILE = os.path.join(DATA_DIR, 'roles.json')
    OBJECTIVES_FILE = os.path.join(DATA_DIR, 'objectives.json')
    ISSUES_FILE = os.path.join(DATA_DIR, 'issues.jsonl')
    TASKS_FILE = os.path.join(DATA_DIR, 'tasks.jsonl')
    KNOWLEDGE_FILE = os.path.join(DATA_DIR, 'knowledge.json')
    LOGS_FILE = os.path.join(DATA_DIR, 'system_logs.jsonl')
    
    # 上传文件配置
    UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 分页配置
    ITEMS_PER_PAGE = 20

