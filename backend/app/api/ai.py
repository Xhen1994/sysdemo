"""
AI功能API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.issue import Issue
from ..schemas.ai import AISummaryRequest, AISummaryResponse, AIAnalysisResponse
from ..services.ai_service import ai_service
from .deps import get_current_active_user

router = APIRouter()


@router.post("/summarize", response_model=AISummaryResponse)
async def generate_summary(
    request: AISummaryRequest,
    current_user = Depends(get_current_active_user)
):
    """
    生成文本摘要和标签
    """
    try:
        summary = await ai_service.generate_summary(request.text, request.max_length)
        tags = await ai_service.generate_tags(request.text)
        category = await ai_service.suggest_category(request.text)
        
        return AISummaryResponse(
            summary=summary,
            tags=tags,
            category_suggestion=category
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI摘要生成失败: {str(e)}"
        )


@router.post("/analyze/{issue_id}")
async def analyze_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    对指定问题进行AI分析
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    try:
        ai_result = await ai_service.analyze_issue_full(issue.title, issue.description)
        
        # 更新问题的AI分析结果
        issue.ai_summary = ai_result["summary"]
        issue.ai_tags = ",".join(ai_result["tags"]) if ai_result["tags"] else None
        issue.ai_category_suggestion = ai_result["category_suggestion"]
        
        db.commit()
        db.refresh(issue)
        
        return {
            "issue_id": issue_id,
            "ai_summary": issue.ai_summary,
            "ai_tags": issue.ai_tags,
            "ai_category_suggestion": issue.ai_category_suggestion
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI分析失败: {str(e)}"
        )


@router.get("/trends", response_model=AIAnalysisResponse)
async def analyze_trends(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    分析问题趋势
    """
    # 获取最近的问题
    issues = db.query(Issue).order_by(Issue.created_at.desc()).limit(limit).all()
    
    if not issues:
        return AIAnalysisResponse(
            analysis_type="trend",
            insights=["暂无足够数据进行分析"],
            recommendations=[]
        )
    
    try:
        # 准备问题数据
        issues_data = [
            {
                "title": issue.title,
                "category": issue.category.value if issue.category else "other",
                "priority": issue.priority.value if issue.priority else "medium",
                "status": issue.status.value if issue.status else "open"
            }
            for issue in issues
        ]
        
        # 调用AI分析
        analysis = await ai_service.analyze_trends(issues_data)
        
        # 计算统计数据
        total = len(issues)
        by_category = {}
        by_priority = {}
        by_status = {}
        
        for issue in issues:
            cat = issue.category.value if issue.category else "other"
            pri = issue.priority.value if issue.priority else "medium"
            sta = issue.status.value if issue.status else "open"
            
            by_category[cat] = by_category.get(cat, 0) + 1
            by_priority[pri] = by_priority.get(pri, 0) + 1
            by_status[sta] = by_status.get(sta, 0) + 1
        
        return AIAnalysisResponse(
            analysis_type="trend",
            insights=analysis.get("insights", []),
            recommendations=analysis.get("recommendations", []),
            statistics={
                "total": total,
                "by_category": by_category,
                "by_priority": by_priority,
                "by_status": by_status
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"趋势分析失败: {str(e)}"
        )


@router.get("/suggestions/{issue_id}")
async def get_solution_suggestions(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    获取问题解决方案建议
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="问题不存在"
        )
    
    try:
        # 查找相似的已解决问题
        similar_issues = db.query(Issue).filter(
            Issue.category == issue.category,
            Issue.status.in_(["resolved", "closed"]),
            Issue.id != issue_id
        ).limit(5).all()
        
        similar_data = [
            {
                "title": si.title,
                "solution": si.ai_summary or "已成功解决"
            }
            for si in similar_issues
        ]
        
        suggestions = await ai_service.generate_solution_suggestions(
            issue.description,
            similar_data
        )
        
        return {
            "issue_id": issue_id,
            "suggestions": suggestions,
            "similar_issues_count": len(similar_issues)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"建议生成失败: {str(e)}"
        )



