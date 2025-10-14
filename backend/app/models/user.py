from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    
    # 部门关联
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="users")
    
    # 角色和权限
    role = Column(String(20), default="user")  # admin, manager, user
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    created_issues = relationship("Issue", back_populates="creator", foreign_keys="Issue.creator_id")
    assigned_issues = relationship("Issue", back_populates="assignee", foreign_keys="Issue.assignee_id")
    comments = relationship("IssueComment", back_populates="author")
    feedbacks = relationship("IssueFeedback", back_populates="author")
    
    def __repr__(self):
        return f"<User {self.username}>"


