# API文档

## 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token (JWT)
- **Content-Type**: `application/json`

## 认证 (Authentication)

### 用户注册

```http
POST /api/v1/auth/register
```

**请求体**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "full_name": "测试用户",
  "phone": "13800138000",
  "department_id": 1,
  "role": "user"
}
```

**响应**:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "测试用户",
  "role": "user",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00"
}
```

### 用户登录

```http
POST /api/v1/auth/login
Content-Type: multipart/form-data
```

**请求体** (表单数据):
- `username`: testuser
- `password`: password123

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 用户管理 (Users)

所有用户相关接口需要认证。

### 获取当前用户信息

```http
GET /api/v1/users/me
Authorization: Bearer {token}
```

### 获取用户列表

```http
GET /api/v1/users?skip=0&limit=100
Authorization: Bearer {token}
```

### 更新用户信息

```http
PUT /api/v1/users/{user_id}
Authorization: Bearer {token}
```

## 问题管理 (Issues)

### 获取问题列表

```http
GET /api/v1/issues?status=open&priority=high&search=关键词
Authorization: Bearer {token}
```

**查询参数**:
- `skip`: 跳过数量（分页）
- `limit`: 返回数量
- `status`: 问题状态 (open, in_progress, resolved, closed)
- `priority`: 优先级 (low, medium, high, urgent)
- `category`: 分类 (bug, feature, improvement, question, other)
- `search`: 搜索关键词

**响应**:
```json
[
  {
    "id": 1,
    "title": "系统登录问题",
    "description": "用户无法登录系统...",
    "category": "bug",
    "priority": "high",
    "status": "open",
    "ai_summary": "用户登录功能出现异常，需要检查认证模块",
    "ai_tags": "登录,认证,bug",
    "ai_category_suggestion": "bug",
    "creator_id": 1,
    "assignee_id": 2,
    "department_id": 1,
    "project_id": 1,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T01:00:00"
  }
]
```

### 创建问题

```http
POST /api/v1/issues
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "title": "系统登录问题",
  "description": "用户无法登录系统，显示密码错误",
  "category": "bug",
  "priority": "high",
  "department_id": 1,
  "project_id": 1,
  "assignee_id": 2
}
```

**响应**: 创建的问题对象（包含AI自动生成的摘要和标签）

### 获取问题详情

```http
GET /api/v1/issues/{issue_id}
Authorization: Bearer {token}
```

### 更新问题

```http
PUT /api/v1/issues/{issue_id}
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "status": "in_progress",
  "priority": "urgent",
  "assignee_id": 3
}
```

### 删除问题

```http
DELETE /api/v1/issues/{issue_id}
Authorization: Bearer {token}
```

### 获取问题统计

```http
GET /api/v1/issues/stats/summary
Authorization: Bearer {token}
```

**响应**:
```json
{
  "total": 100,
  "open": 20,
  "in_progress": 30,
  "resolved": 40,
  "closed": 10,
  "completion_rate": 50.0
}
```

## 问题评论 (Issue Comments)

### 获取问题评论列表

```http
GET /api/v1/issues/{issue_id}/comments
Authorization: Bearer {token}
```

### 添加评论

```http
POST /api/v1/issues/{issue_id}/comments?content=这是评论内容
Authorization: Bearer {token}
```

## 问题反馈 (Issue Feedbacks)

### 获取问题反馈列表

```http
GET /api/v1/issues/{issue_id}/feedbacks
Authorization: Bearer {token}
```

### 提交反馈

```http
POST /api/v1/issues/feedbacks
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "issue_id": 1,
  "rating": 5,
  "content": "处理速度很快，问题已解决",
  "is_satisfied": true,
  "improvement_suggestions": "希望能提供更详细的进度更新"
}
```

## AI功能 (AI)

### AI文本摘要和标签生成

```http
POST /api/v1/ai/summarize
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "text": "系统登录模块出现严重bug，用户输入正确的用户名和密码后，系统提示密码错误...",
  "max_length": 200
}
```

**响应**:
```json
{
  "summary": "用户登录功能异常，认证失败",
  "tags": ["登录", "认证", "bug", "用户体验"],
  "category_suggestion": "bug"
}
```

### AI分析指定问题

```http
POST /api/v1/ai/analyze/{issue_id}
Authorization: Bearer {token}
```

**响应**:
```json
{
  "issue_id": 1,
  "ai_summary": "用户登录功能异常，认证失败",
  "ai_tags": "登录,认证,bug",
  "ai_category_suggestion": "bug"
}
```

### AI趋势分析

```http
GET /api/v1/ai/trends?limit=50
Authorization: Bearer {token}
```

**响应**:
```json
{
  "analysis_type": "trend",
  "insights": [
    "登录相关问题占比最高，达到30%",
    "高优先级问题主要集中在认证模块",
    "周五和周一是问题提交高峰期"
  ],
  "recommendations": [
    "建议优先优化登录认证模块",
    "增加自动化测试覆盖率",
    "建立问题预警机制"
  ],
  "statistics": {
    "total": 50,
    "by_category": {
      "bug": 20,
      "feature": 15,
      "improvement": 10
    },
    "by_priority": {
      "urgent": 5,
      "high": 15,
      "medium": 20,
      "low": 10
    }
  }
}
```

### AI解决方案建议

```http
GET /api/v1/ai/suggestions/{issue_id}
Authorization: Bearer {token}
```

**响应**:
```json
{
  "issue_id": 1,
  "suggestions": [
    "检查用户认证中间件配置",
    "验证密码加密算法是否正确",
    "查看数据库用户表数据完整性"
  ],
  "similar_issues_count": 3
}
```

## 部门管理 (Departments)

### 获取部门列表

```http
GET /api/v1/departments
Authorization: Bearer {token}
```

### 创建部门（需要管理员权限）

```http
POST /api/v1/departments
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "name": "技术部",
  "code": "TECH",
  "description": "负责技术开发和维护",
  "contact_person": "张三",
  "contact_phone": "13800138000",
  "contact_email": "tech@example.com"
}
```

## 项目管理 (Projects)

### 获取项目列表

```http
GET /api/v1/projects
Authorization: Bearer {token}
```

### 创建项目（需要管理员权限）

```http
POST /api/v1/projects
Authorization: Bearer {token}
```

**请求体**:
```json
{
  "name": "数字化平台建设",
  "code": "PROJ001",
  "description": "构建省专协同数字化平台",
  "status": "in_progress",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "manager_name": "李四",
  "manager_contact": "lisi@example.com"
}
```

## 错误响应

所有API在出错时返回统一格式：

```json
{
  "detail": "错误描述信息"
}
```

**常见HTTP状态码**:
- `200`: 成功
- `201`: 创建成功
- `204`: 删除成功（无内容）
- `400`: 请求参数错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器错误

## 在线API文档

启动后端服务后，可以访问交互式API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

这些文档支持直接在浏览器中测试API接口。



