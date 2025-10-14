# 省专协同数字化平台

一个集成AI智能分析的协同数字化管理平台，支持问题管理、智能总结和反馈追踪。

## 功能特性

### 核心功能
- 📊 **协同工作管理** - 多部门、多项目协同工作管理
- 📝 **问题管理系统** - 问题提交、追踪、分配和解决
- 🤖 **AI智能总结** - 自动总结问题、生成分析报告
- 💬 **反馈系统** - 问题反馈、评价和改进建议
- 👥 **用户管理** - 用户认证、权限管理
- 📈 **数据统计** - 可视化数据分析和报表

### AI功能
- 问题智能分类和标签生成
- 自动生成问题摘要
- 问题趋势分析
- 智能推荐解决方案

## 技术栈

### 后端
- Python 3.9+
- FastAPI - 高性能Web框架
- SQLAlchemy - ORM
- PostgreSQL/SQLite - 数据库
- Redis - 缓存
- OpenAI API / 其他AI API - AI功能集成

### 前端
- React 18
- TypeScript
- Ant Design - UI组件库
- Axios - HTTP客户端
- React Router - 路由管理
- Recharts - 数据可视化

## 项目结构

```
sysdemo/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   ├── schemas/        # Pydantic模型
│   │   └── core/           # 核心配置
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # React组件
│   │   ├── pages/          # 页面
│   │   ├── services/       # API服务
│   │   ├── utils/          # 工具函数
│   │   └── App.tsx         # 主应用
│   └── package.json        # Node依赖
└── docs/                   # 文档
```

## 快速开始

### 🚀 一键启动（Docker）

**Windows用户**：
```bash
# 双击运行 start.bat 或在命令行执行：
start.bat
```

**Linux/Mac用户**：
```bash
# 赋予执行权限
chmod +x start.sh
# 运行启动脚本
./start.sh
```

**首次启动需要初始化数据库**：
```bash
docker-compose exec backend python init_db.py
```

### 📝 手动启动

#### 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入你的AI API密钥

# 初始化数据库
python init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

### 🌐 访问系统

- **前端界面**：http://localhost:3000
- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs

**默认登录账号**：
- 用户名：`admin`
- 密码：`admin123`

> 💡 **提示**：首次使用前请配置 `backend/.env` 文件中的 `OPENAI_API_KEY`

## API文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 环境变量配置

首次运行会自动创建 `backend/.env` 文件，请编辑填入配置：

```env
# 数据库配置
DATABASE_URL=sqlite:///./sql_app.db
# 或使用PostgreSQL: postgresql://user:password@localhost/dbname

# AI API配置（必须配置）
OPENAI_API_KEY=sk-your-actual-api-key-here  # 👈 在这里填入你的API密钥
OPENAI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo
AI_MAX_TOKENS=2000

# JWT密钥（生产环境请修改）
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis配置（可选）
REDIS_URL=redis://localhost:6379/0

# CORS配置
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 如何获取OpenAI API密钥？

1. 访问 https://platform.openai.com
2. 注册/登录账号
3. 进入API密钥管理页面
4. 创建新的API密钥
5. 复制密钥到 `.env` 文件

> 💡 也支持使用兼容OpenAI API的其他服务（如Azure OpenAI、国内API等）

## 主要功能说明

### 1. 问题管理
- 创建问题：提交问题描述、优先级、负责人
- 问题追踪：查看问题状态、历史记录
- 问题分配：分配给相关部门或人员
- 问题解决：更新进度、关闭问题

### 2. AI智能总结
- **自动摘要**：AI自动生成问题摘要
- **分类标签**：智能分类和打标签
- **趋势分析**：分析问题趋势和模式
- **解决方案推荐**：基于历史数据推荐解决方案

### 3. 反馈系统
- 提交反馈：对问题处理进行评价
- 追踪反馈：查看反馈处理状态
- 改进建议：收集和管理改进建议

## 部署

### Docker一键部署（推荐）

```bash
# 1. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 OPENAI_API_KEY

# 2. 启动所有服务
docker-compose up -d

# 3. 初始化数据库
docker-compose exec backend python init_db.py

# 4. 访问系统
# 前端: http://localhost:3000
# 后端: http://localhost:8000
```

### 生产环境部署

详细的生产环境部署指南请查看：
- 📖 [完整部署指南](docs/DEPLOYMENT.md)
- 🔧 包含Nginx配置、HTTPS、系统服务等

## 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 📚 相关文档

- 📖 [快速开始指南](QUICKSTART.md) - 5分钟上手
- 🚀 [部署指南](docs/DEPLOYMENT.md) - 生产环境部署
- 🔌 [API文档](docs/API.md) - 完整API说明
- 📱 [用户手册](docs/USER_GUIDE.md) - 功能使用说明
- 📋 [项目总结](PROJECT_SUMMARY.md) - 技术架构和实现

## 🎯 快速导航

**新手用户**：
1. 阅读 [快速开始指南](QUICKSTART.md)
2. 运行启动脚本 `start.bat` 或 `start.sh`
3. 查看 [用户手册](docs/USER_GUIDE.md) 了解功能

**开发者**：
1. 查看 [项目总结](PROJECT_SUMMARY.md) 了解架构
2. 阅读 [API文档](docs/API.md) 了解接口
3. 参考代码注释进行二次开发

**运维人员**：
1. 阅读 [部署指南](docs/DEPLOYMENT.md)
2. 配置生产环境
3. 设置监控和备份

## 🐛 故障排查

遇到问题？请查看：
1. [快速开始指南](QUICKSTART.md) 的故障排查章节
2. [部署指南](docs/DEPLOYMENT.md) 的故障排查章节
3. GitHub Issues

## 🤝 贡献

欢迎提交 Pull Request 或 Issue！

## 📞 联系方式

如有问题或建议，请：
- 📧 提交GitHub Issue
- 📖 查阅项目文档
- 💬 联系项目维护团队

## ⭐ Star History

如果这个项目对你有帮助，请给它一个⭐！

