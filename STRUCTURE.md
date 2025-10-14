# 项目结构说明

## 📂 完整目录树

```
sysdemo/
│
├── 📄 README.md                    # 项目说明文档
├── 📄 QUICKSTART.md                # 快速开始指南
├── 📄 PROJECT_SUMMARY.md           # 项目总结文档
├── 📄 STRUCTURE.md                 # 本文件 - 结构说明
├── 📄 .gitignore                   # Git忽略配置
├── 📄 docker-compose.yml           # Docker编排配置
├── 📄 start.bat                    # Windows启动脚本
├── 📄 start.sh                     # Linux/Mac启动脚本
│
├── 📁 docs/                        # 文档目录
│   ├── API.md                      # API接口文档
│   ├── DEPLOYMENT.md               # 部署指南
│   └── USER_GUIDE.md               # 用户使用手册
│
├── 📁 backend/                     # 后端服务目录
│   ├── 📄 requirements.txt         # Python依赖列表
│   ├── 📄 Dockerfile               # Docker镜像配置
│   ├── 📄 init_db.py              # 数据库初始化脚本
│   ├── 📄 env.example.txt         # 环境变量模板
│   │
│   └── 📁 app/                     # 应用主目录
│       ├── 📄 main.py             # FastAPI应用入口
│       │
│       ├── 📁 core/                # 核心模块
│       │   ├── __init__.py
│       │   ├── config.py          # 应用配置（环境变量读取）
│       │   ├── database.py        # 数据库连接和会话
│       │   └── security.py        # 安全模块（JWT、密码加密）
│       │
│       ├── 📁 models/              # 数据模型（SQLAlchemy ORM）
│       │   ├── __init__.py
│       │   ├── user.py            # 用户模型
│       │   ├── department.py      # 部门模型
│       │   ├── project.py         # 项目模型
│       │   └── issue.py           # 问题、评论、反馈模型
│       │
│       ├── 📁 schemas/             # 数据模式（Pydantic）
│       │   ├── __init__.py
│       │   ├── user.py            # 用户相关Schema
│       │   ├── department.py      # 部门相关Schema
│       │   ├── project.py         # 项目相关Schema
│       │   ├── issue.py           # 问题相关Schema
│       │   └── ai.py              # AI功能Schema
│       │
│       ├── 📁 services/            # 业务逻辑层
│       │   ├── __init__.py
│       │   └── ai_service.py      # AI服务（OpenAI集成）
│       │
│       └── 📁 api/                 # API路由层
│           ├── __init__.py        # 路由注册
│           ├── deps.py            # 依赖注入（认证等）
│           ├── auth.py            # 认证API（登录、注册）
│           ├── users.py           # 用户管理API
│           ├── departments.py     # 部门管理API
│           ├── projects.py        # 项目管理API
│           ├── issues.py          # 问题管理API
│           └── ai.py              # AI功能API
│
└── 📁 frontend/                    # 前端应用目录
    ├── 📄 package.json             # Node.js依赖配置
    ├── 📄 tsconfig.json            # TypeScript配置
    ├── 📄 vite.config.ts           # Vite构建配置
    ├── 📄 Dockerfile               # Docker镜像配置
    ├── 📄 index.html               # HTML入口文件
    │
    └── 📁 src/                     # 源代码目录
        ├── 📄 main.tsx             # React应用入口
        ├── 📄 App.tsx              # 主应用组件（路由配置）
        ├── 📄 index.css            # 全局样式
        │
        ├── 📁 pages/               # 页面组件
        │   ├── Login.tsx           # 登录页面
        │   ├── Dashboard.tsx       # 工作台（首页）
        │   ├── IssueList.tsx       # 问题列表页
        │   ├── IssueDetail.tsx     # 问题详情页
        │   ├── IssueCreate.tsx     # 创建问题页
        │   ├── AIAnalysis.tsx      # AI分析页面
        │   ├── DepartmentList.tsx  # 部门列表页
        │   └── ProjectList.tsx     # 项目列表页
        │
        ├── 📁 components/          # 可复用组件
        │   └── Layout/
        │       └── AppLayout.tsx   # 应用布局组件
        │
        ├── 📁 services/            # API服务层
        │   └── api.ts              # Axios配置和拦截器
        │
        └── 📁 context/             # React Context
            └── AuthContext.tsx     # 认证上下文
```

## 🔍 关键文件说明

### 后端核心文件

#### 1. `backend/app/main.py`
**作用**：FastAPI应用的入口文件
**内容**：
- 创建FastAPI应用实例
- 配置CORS中间件
- 注册API路由
- 定义健康检查端点

#### 2. `backend/app/core/config.py`
**作用**：应用配置管理
**内容**：
- 定义Settings类（继承自Pydantic BaseSettings）
- 读取环境变量
- 提供配置单例

#### 3. `backend/app/core/database.py`
**作用**：数据库连接管理
**内容**：
- 创建SQLAlchemy引擎
- 定义会话工厂
- 提供数据库会话依赖

#### 4. `backend/app/core/security.py`
**作用**：安全功能实现
**内容**：
- 密码哈希和验证（bcrypt）
- JWT令牌创建和验证

#### 5. `backend/app/services/ai_service.py`
**作用**：AI功能核心实现
**内容**：
- OpenAI API集成
- 摘要生成
- 标签提取
- 分类建议
- 趋势分析
- 解决方案推荐

#### 6. `backend/app/models/issue.py`
**作用**：问题相关数据模型
**内容**：
- Issue模型（问题表）
- IssueComment模型（评论表）
- IssueFeedback模型（反馈表）
- 定义枚举类型（状态、优先级、分类）

#### 7. `backend/app/api/issues.py`
**作用**：问题管理API实现
**内容**：
- CRUD操作
- 搜索和筛选
- 评论管理
- 反馈管理
- 自动调用AI分析

### 前端核心文件

#### 1. `frontend/src/main.tsx`
**作用**：React应用入口
**内容**：
- 创建React根节点
- 配置Ant Design中文语言包
- 渲染App组件

#### 2. `frontend/src/App.tsx`
**作用**：应用主组件
**内容**：
- 路由配置（React Router）
- 认证状态管理
- 保护路由实现

#### 3. `frontend/src/context/AuthContext.tsx`
**作用**：认证状态管理
**内容**：
- 用户登录/登出逻辑
- Token管理
- 用户信息获取
- 认证状态共享

#### 4. `frontend/src/services/api.ts`
**作用**：HTTP客户端配置
**内容**：
- Axios实例创建
- 请求拦截器（添加Token）
- 响应拦截器（错误处理）

#### 5. `frontend/src/pages/IssueList.tsx`
**作用**：问题列表页面
**内容**：
- 问题列表展示
- 搜索和筛选
- 分页处理

#### 6. `frontend/src/pages/IssueCreate.tsx`
**作用**：创建问题页面
**内容**：
- 问题表单
- AI分析按钮
- 表单验证

#### 7. `frontend/src/pages/AIAnalysis.tsx`
**作用**：AI分析页面
**内容**：
- 触发趋势分析
- 展示分析结果
- 数据可视化

## 🔗 模块依赖关系

### 后端依赖流

```
main.py
  ↓
api/ (路由层)
  ↓
deps.py (依赖注入) ←→ core/security.py (认证)
  ↓
models/ (数据模型) ←→ schemas/ (数据验证)
  ↓
core/database.py (数据库)
  ↓
services/ (业务逻辑)
  ↓
外部服务 (OpenAI API)
```

### 前端依赖流

```
main.tsx
  ↓
App.tsx
  ↓
AuthContext (认证管理)
  ↓
pages/ (页面组件)
  ↓
components/ (复用组件)
  ↓
services/api.ts (HTTP客户端)
  ↓
后端API
```

## 📝 数据流向

### 创建问题的完整流程

1. **用户操作**：在 `IssueCreate.tsx` 填写表单
2. **前端处理**：调用 `api.post('/issues', data)`
3. **HTTP请求**：通过 `api.ts` 拦截器添加Token
4. **后端接收**：`api/issues.py` 的 `create_issue` 端点
5. **依赖注入**：`deps.py` 验证Token，获取当前用户
6. **数据验证**：`schemas/issue.py` 验证请求数据
7. **创建记录**：`models/issue.py` 在数据库创建记录
8. **AI分析**：异步调用 `services/ai_service.py`
9. **更新记录**：将AI分析结果写入数据库
10. **返回响应**：返回完整的问题对象（含AI结果）
11. **前端展示**：跳转到问题详情页

### AI趋势分析流程

1. **用户操作**：点击"AI智能分析"页面的"开始分析"
2. **API调用**：`api.get('/ai/trends')`
3. **后端处理**：`api/ai.py` 的 `analyze_trends` 端点
4. **数据查询**：从数据库获取最近的问题记录
5. **AI分析**：调用 `ai_service.analyze_trends()`
6. **OpenAI调用**：发送问题数据到OpenAI API
7. **结果解析**：解析AI返回的JSON结果
8. **统计计算**：计算问题分布等统计数据
9. **返回结果**：包含洞察、建议和统计的完整对象
10. **前端展示**：在页面上展示分析结果

## 🎨 设计模式

### 后端设计模式

1. **三层架构**
   - API层（api/）：处理HTTP请求
   - 服务层（services/）：业务逻辑
   - 数据层（models/）：数据持久化

2. **依赖注入**
   - 使用FastAPI的Depends实现
   - 在deps.py中定义可复用的依赖

3. **单例模式**
   - 配置对象（settings）
   - AI服务实例（ai_service）

4. **工厂模式**
   - 数据库会话工厂（SessionLocal）

### 前端设计模式

1. **容器/展示组件**
   - pages/ 为容器组件（有状态）
   - components/ 为展示组件（无状态）

2. **Context模式**
   - AuthContext 管理全局认证状态

3. **Hooks模式**
   - 使用React Hooks管理状态和副作用

## 🔧 扩展指南

### 添加新的API端点

1. 在 `backend/app/api/` 创建新的路由文件
2. 定义路由函数和端点
3. 在 `backend/app/api/__init__.py` 注册路由
4. 在 `backend/app/schemas/` 定义请求/响应模型
5. 更新 `docs/API.md` 文档

### 添加新的页面

1. 在 `frontend/src/pages/` 创建新的页面组件
2. 在 `frontend/src/App.tsx` 添加路由配置
3. 在布局的导航菜单中添加入口
4. 创建对应的API服务函数

### 添加新的数据模型

1. 在 `backend/app/models/` 定义SQLAlchemy模型
2. 在 `backend/app/schemas/` 定义Pydantic模型
3. 运行数据库迁移（如使用Alembic）
4. 创建对应的CRUD API
5. 更新前端TypeScript类型定义

## 📚 相关文档

- [项目总结](PROJECT_SUMMARY.md) - 技术架构详解
- [API文档](docs/API.md) - 接口说明
- [部署指南](docs/DEPLOYMENT.md) - 部署方案

---

**提示**：本文档帮助开发者快速理解项目结构，便于代码导航和功能扩展。



