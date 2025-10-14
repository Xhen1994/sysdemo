from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):
    """部门基础模型"""
    name: str
    code: str
    description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None


class DepartmentCreate(DepartmentBase):
    """创建部门"""
    pass


class DepartmentUpdate(BaseModel):
    """更新部门"""
    name: Optional[str] = None
    description: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None


class DepartmentResponse(DepartmentBase):
    """部门响应"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True



