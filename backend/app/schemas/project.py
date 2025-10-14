from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.project import ProjectStatus


class ProjectBase(BaseModel):
    """项目基础模型"""
    name: str
    code: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    manager_name: Optional[str] = None
    manager_contact: Optional[str] = None


class ProjectCreate(ProjectBase):
    """创建项目"""
    pass


class ProjectUpdate(BaseModel):
    """更新项目"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    manager_name: Optional[str] = None
    manager_contact: Optional[str] = None


class ProjectResponse(ProjectBase):
    """项目响应"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True



