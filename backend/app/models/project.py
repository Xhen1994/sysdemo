from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..core.database import Base


class ProjectStatus(str, enum.Enum):
    """项目状态"""
    PLANNING = "planning"      # 规划中
    IN_PROGRESS = "in_progress"  # 进行中
    ON_HOLD = "on_hold"        # 暂停
    COMPLETED = "completed"    # 已完成
    CANCELLED = "cancelled"    # 已取消


class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # 项目状态
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PLANNING)
    
    # 项目时间
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # 项目负责人
    manager_name = Column(String(100))
    manager_contact = Column(String(100))
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    issues = relationship("Issue", back_populates="project")
    
    def __repr__(self):
        return f"<Project {self.name}>"


