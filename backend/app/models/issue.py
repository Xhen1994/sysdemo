from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class IssuePriority(str, enum.Enum):
    """问题优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class IssueStatus(str, enum.Enum):
    """问题状态"""
    OPEN = "open"           # 待处理
    IN_PROGRESS = "in_progress"  # 处理中
    RESOLVED = "resolved"   # 已解决
    CLOSED = "closed"       # 已关闭
    REJECTED = "rejected"   # 已拒绝


class IssueCategory(str, enum.Enum):
    """问题分类"""
    BUG = "bug"                    # 缺陷
    FEATURE = "feature"            # 功能需求
    IMPROVEMENT = "improvement"    # 改进
    QUESTION = "question"          # 疑问
    OTHER = "other"                # 其他


class Issue(Base):
    """问题/工单模型"""
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # 分类和状态
    category = Column(SQLEnum(IssueCategory), default=IssueCategory.OTHER)
    priority = Column(SQLEnum(IssuePriority), default=IssuePriority.MEDIUM)
    status = Column(SQLEnum(IssueStatus), default=IssueStatus.OPEN)
    
    # AI生成的摘要和标签
    ai_summary = Column(Text)  # AI生成的摘要
    ai_tags = Column(String(500))  # AI生成的标签，逗号分隔
    ai_category_suggestion = Column(String(50))  # AI建议的分类
    
    # 关联
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="created_issues", foreign_keys=[creator_id])
    
    assignee_id = Column(Integer, ForeignKey("users.id"))
    assignee = relationship("User", back_populates="assigned_issues", foreign_keys=[assignee_id])
    
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="issues")
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="issues")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    
    # 关系
    comments = relationship("IssueComment", back_populates="issue", cascade="all, delete-orphan")
    feedbacks = relationship("IssueFeedback", back_populates="issue", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Issue {self.id}: {self.title}>"


class IssueComment(Base):
    """问题评论模型"""
    __tablename__ = "issue_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    # 关联
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    issue = relationship("Issue", back_populates="comments")
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="comments")
    
    # 是否为系统生成的评论
    is_system = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<IssueComment {self.id}>"


class IssueFeedback(Base):
    """问题反馈模型"""
    __tablename__ = "issue_feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 评分（1-5星）
    rating = Column(Integer, nullable=False)
    
    # 反馈内容
    content = Column(Text)
    
    # 是否满意
    is_satisfied = Column(Boolean, default=True)
    
    # 改进建议
    improvement_suggestions = Column(Text)
    
    # 关联
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    issue = relationship("Issue", back_populates="feedbacks")
    
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="feedbacks")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<IssueFeedback {self.id}>"


