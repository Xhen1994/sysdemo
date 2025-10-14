from pydantic import BaseModel
from typing import Optional, List, Dict


class AISummaryRequest(BaseModel):
    """AI摘要请求"""
    text: str
    max_length: Optional[int] = 200


class AISummaryResponse(BaseModel):
    """AI摘要响应"""
    summary: str
    tags: List[str]
    category_suggestion: Optional[str] = None


class AIAnalysisRequest(BaseModel):
    """AI分析请求"""
    issue_ids: List[int]
    analysis_type: str = "trend"  # trend, pattern, recommendation


class AIAnalysisResponse(BaseModel):
    """AI分析响应"""
    analysis_type: str
    insights: List[str]
    recommendations: List[str]
    statistics: Dict[str, any] = {}



