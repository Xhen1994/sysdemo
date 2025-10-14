from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.issue import IssuePriority, IssueStatus, IssueCategory


class IssueBase(BaseModel):
    """问题基础模型"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    category: IssueCategory = IssueCategory.OTHER
    priority: IssuePriority = IssuePriority.MEDIUM
    department_id: Optional[int] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None


class IssueCreate(IssueBase):
    """创建问题"""
    pass


class IssueUpdate(BaseModel):
    """更新问题"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[IssueCategory] = None
    priority: Optional[IssuePriority] = None
    status: Optional[IssueStatus] = None
    department_id: Optional[int] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None


class IssueResponse(IssueBase):
    """问题响应"""
    id: int
    status: IssueStatus
    ai_summary: Optional[str] = None
    ai_tags: Optional[str] = None
    ai_category_suggestion: Optional[str] = None
    creator_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class IssueCommentCreate(BaseModel):
    """创建评论"""
    content: str = Field(..., min_length=1)
    issue_id: int


class IssueCommentResponse(BaseModel):
    """评论响应"""
    id: int
    content: str
    issue_id: int
    author_id: int
    is_system: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class IssueFeedbackCreate(BaseModel):
    """创建反馈"""
    issue_id: int
    rating: int = Field(..., ge=1, le=5)
    content: Optional[str] = None
    is_satisfied: bool = True
    improvement_suggestions: Optional[str] = None


class IssueFeedbackResponse(BaseModel):
    """反馈响应"""
    id: int
    issue_id: int
    author_id: int
    rating: int
    content: Optional[str] = None
    is_satisfied: bool
    improvement_suggestions: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True



