"""
数据库初始化脚本
"""
from app.core.database import Base, engine, SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.department import Department
from app.models.project import Project
from app.models.issue import Issue


def init_db():
    """初始化数据库"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")
    
    # 创建初始数据
    db = SessionLocal()
    
    try:
        # 检查是否已有管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("创建管理员用户...")
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="系统管理员",
                role="admin",
                is_superuser=True,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("管理员用户创建完成！")
            print("用户名: admin")
            print("密码: admin123")
        
        # 创建示例部门
        dept_count = db.query(Department).count()
        if dept_count == 0:
            print("创建示例部门...")
            departments = [
                Department(
                    name="技术部",
                    code="TECH",
                    description="负责技术开发和维护",
                    contact_person="张三",
                    contact_phone="13800138001",
                    contact_email="tech@example.com"
                ),
                Department(
                    name="运营部",
                    code="OPS",
                    description="负责日常运营管理",
                    contact_person="李四",
                    contact_phone="13800138002",
                    contact_email="ops@example.com"
                ),
                Department(
                    name="客服部",
                    code="CS",
                    description="负责客户服务",
                    contact_person="王五",
                    contact_phone="13800138003",
                    contact_email="cs@example.com"
                )
            ]
            for dept in departments:
                db.add(dept)
            db.commit()
            print("示例部门创建完成！")
        
        # 创建示例项目
        project_count = db.query(Project).count()
        if project_count == 0:
            print("创建示例项目...")
            projects = [
                Project(
                    name="数字化平台建设",
                    code="PROJ001",
                    description="构建省专协同数字化平台",
                    status="in_progress",
                    manager_name="赵六",
                    manager_contact="zhaoliu@example.com"
                ),
                Project(
                    name="系统优化升级",
                    code="PROJ002",
                    description="优化现有系统性能",
                    status="planning",
                    manager_name="孙七",
                    manager_contact="sunqi@example.com"
                )
            ]
            for project in projects:
                db.add(project)
            db.commit()
            print("示例项目创建完成！")
        
        print("\n数据库初始化完成！")
        print("\n可以使用以下命令启动服务：")
        print("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()



