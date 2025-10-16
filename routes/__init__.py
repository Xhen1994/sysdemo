from routes.auth import auth_bp
from routes.objectives import objectives_bp
from routes.issues import issues_bp
from routes.tasks import tasks_bp
from routes.knowledge import knowledge_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp

def register_routes(app, data_manager):
    """注册所有路由蓝图"""
    app.data_manager = data_manager
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(objectives_bp)
    app.register_blueprint(issues_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

