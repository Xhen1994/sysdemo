"""
问题管理API路由 - 集成AI功能
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..core.database import get_db
from ..models.issue import Issue, IssueComment, IssueFeedback, IssueStatus
from ..models.user import User
from ..schemas.issue import (
    IssueCreate, IssueUpdate, IssueResponse,
    IssueCommentCreate, IssueCommentResponse,
    IssueFeedbackCreate, IssueFeedbackResponse
)
from ..services.ai_service import ai_service
from .deps import get_current_active_user

router = APIRouter()


@router.get("", response_model=List[IssueResponse])
async def list_issues(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取问题列表（支持筛选和搜索）"""
    query = db.query(Issue)
    
    # 筛选条件
    if status:
        query = query.filter(Issue.status == status)
    if priority:
        query = query.filter(Issue.priority == priority)
    if category:
        query = query.filter(Issue.category == category)
    if assignee_id:
        query = query.filter(Issue.assignee_id == assignee_id)
    
    # 搜索
    if search:
        query = query.filter(
            or_(
                Issue.title.contains(search),
                Issue.description.contains(search),
                Issue.ai_tags.contains(search)
            )
        )
    
    issues = query.order_by(Issue.created_at.desc()).offset(skip).limit(limit).all()
    return issues


@router.post("", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue(
    issue_data: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建问题（自动调用AI生成摘要和标签）"""
    # 创建问题
    issue = Issue(
        **issue_data.model_dump(),
        creator_id=current_user.id
    )
    
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    # 异步调用AI分析（不阻塞响应）
    try:
        ai_result = await ai_service.analyze_issue_full(issue.title, issue.description)
        
        issue.ai_summary = ai_result["summary"]
        issue.ai_tags = ",".join(ai_result["tags"]) if ai_result["tags"] else None
        issue.ai_category_suggestion = ai_result["category_suggestion"]
        
        db.commit()
        db.refresh(issue)
    except Exception as e:
        print(f"AI分析失败: {str(e)}")
    
    return issue


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取问题详情"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    return issue


@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(
    issue_id: int,
    issue_data: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新问题"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    # 更新问题
    update_data = issue_data.model_dump(exclude_unset=True)
    old_status = issue.status
    
    for field, value in update_data.items():
        setattr(issue, field, value)
    
    # 如果状态改变，更新时间戳
    if "status" in update_data:
        if update_data["status"] == IssueStatus.RESOLVED and old_status != IssueStatus.RESOLVED:
            issue.resolved_at = datetime.utcnow()
        elif update_data["status"] == IssueStatus.CLOSED and old_status != IssueStatus.CLOSED:
            issue.closed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(issue)
    
    return issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除问题"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    # 只有创建者或管理员可以删除
    if issue.creator_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此问题"
        )
    
    db.delete(issue)
    db.commit()
    
    return None


# 评论相关API
@router.get("/{issue_id}/comments", response_model=List[IssueCommentResponse])
async def list_issue_comments(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取问题评论列表"""
    comments = db.query(IssueComment).filter(
        IssueComment.issue_id == issue_id
    ).order_by(IssueComment.created_at.asc()).all()
    
    return comments


@router.post("/{issue_id}/comments", response_model=IssueCommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    issue_id: int,
    content: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """添加评论"""
    # 检查问题是否存在
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    comment = IssueComment(
        content=content,
        issue_id=issue_id,
        author_id=current_user.id
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment


# 反馈相关API
@router.get("/{issue_id}/feedbacks", response_model=List[IssueFeedbackResponse])
async def list_issue_feedbacks(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取问题反馈列表"""
    feedbacks = db.query(IssueFeedback).filter(
        IssueFeedback.issue_id == issue_id
    ).order_by(IssueFeedback.created_at.desc()).all()
    
    return feedbacks


@router.post("/feedbacks", response_model=IssueFeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: IssueFeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """提交问题反馈"""
    # 检查问题是否存在
    issue = db.query(Issue).filter(Issue.id == feedback_data.issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    feedback = IssueFeedback(
        **feedback_data.model_dump(),
        author_id=current_user.id
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback


@router.get("/stats/summary")
async def get_issue_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取问题统计数据"""
    total = db.query(Issue).count()
    open_count = db.query(Issue).filter(Issue.status == IssueStatus.OPEN).count()
    in_progress = db.query(Issue).filter(Issue.status == IssueStatus.IN_PROGRESS).count()
    resolved = db.query(Issue).filter(Issue.status == IssueStatus.RESOLVED).count()
    closed = db.query(Issue).filter(Issue.status == IssueStatus.CLOSED).count()
    
    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved,
        "closed": closed,
        "completion_rate": round(closed / total * 100, 2) if total > 0 else 0
    }



