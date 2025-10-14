from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .issues import router as issues_router
from .departments import router as departments_router
from .projects import router as projects_router
from .ai import router as ai_router

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(users_router, prefix="/users", tags=["用户管理"])
api_router.include_router(departments_router, prefix="/departments", tags=["部门管理"])
api_router.include_router(projects_router, prefix="/projects", tags=["项目管理"])
api_router.include_router(issues_router, prefix="/issues", tags=["问题管理"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI功能"])

__all__ = ["api_router"]



