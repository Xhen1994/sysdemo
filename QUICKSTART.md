# 快速开始指南

## 🚀 5分钟快速部署

### 前置要求

确保您的系统已安装：
- **Docker** 20.10+ 和 **Docker Compose** 2.0+
- 或 **Python** 3.9+ 和 **Node.js** 18+

---

## 方式一：Docker部署（推荐）

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd sysdemo
```

### 2. 配置AI API密钥

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑配置文件，填入你的OpenAI API密钥
# Windows用户可以用记事本打开
notepad backend/.env
```

在 `.env` 文件中修改：

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看启动日志
docker-compose logs -f
```

### 4. 初始化数据库

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行初始化脚本
python init_db.py

# 退出容器
exit
```

### 5. 访问系统

- 🌐 前端界面：http://localhost:3000
- 🔧 后端API：http://localhost:8000
- 📚 API文档：http://localhost:8000/docs

**默认登录账号**：
- 用户名：`admin`
- 密码：`admin123`

---

## 方式二：本地开发部署

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入OpenAI API密钥

# 初始化数据库
python init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

打开新的终端窗口：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

访问 http://localhost:3000

---

## 📝 首次使用

### 1. 登录系统

使用默认管理员账号登录：
- 用户名：`admin`
- 密码：`admin123`

### 2. 创建第一个问题

1. 点击左侧导航"问题管理"
2. 点击"新建问题"
3. 填写标题和描述，例如：
   - 标题：`测试AI分析功能`
   - 描述：`这是一个测试问题，用于验证AI自动分析和标签生成功能是否正常工作`
4. 点击"AI智能分析"按钮
5. 选择分类和优先级
6. 点击"创建问题"

### 3. 查看AI分析结果

创建成功后，点击问题标题进入详情页，查看：
- AI生成的问题摘要
- AI自动生成的标签
- AI建议的分类

### 4. 体验AI趋势分析

1. 点击左侧导航"AI智能分析"
2. 点击"开始分析"
3. 查看AI生成的趋势洞察和改进建议

---

## 🔧 配置说明

### OpenAI API密钥获取

1. 访问 https://platform.openai.com
2. 注册/登录账号
3. 进入API密钥页面
4. 创建新的API密钥
5. 复制密钥到 `backend/.env` 文件

### 使用其他AI服务

如果想使用其他兼容OpenAI API的服务（如Azure OpenAI、国内API等），修改 `.env`：

```env
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://your-api-endpoint.com/v1
AI_MODEL=your-model-name
```

---

## 🛠️ 常用命令

### Docker Compose

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 重新构建镜像
docker-compose build

# 查看服务状态
docker-compose ps
```

### 数据库管理

```bash
# 备份数据库
docker-compose exec backend python -c "from app.core.database import engine; import sqlite3; conn = sqlite3.connect('sql_app.db'); conn.backup(sqlite3.connect('backup.db'))"

# 重置数据库
docker-compose exec backend python init_db.py
```

---

## 📊 功能验证清单

完成以下操作，确保系统正常运行：

- [ ] 成功登录系统
- [ ] 创建新问题
- [ ] AI自动生成摘要和标签
- [ ] 添加问题评论
- [ ] 提交问题反馈
- [ ] 查看AI趋势分析
- [ ] 更新问题状态

---

## 🐛 故障排查

### 问题：无法启动Docker服务

**解决方案**：
```bash
# 检查Docker是否运行
docker version

# 检查端口占用
# Windows:
netstat -ano | findstr "3000 8000"
# Linux/Mac:
lsof -i :3000
lsof -i :8000
```

### 问题：AI功能不工作

**解决方案**：
1. 检查API密钥是否正确配置
2. 查看后端日志：`docker-compose logs backend`
3. 测试API连接：
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 问题：前端无法连接后端

**解决方案**：
1. 确认后端服务运行：http://localhost:8000/health
2. 检查CORS配置
3. 查看浏览器控制台错误

### 问题：数据库初始化失败

**解决方案**：
```bash
# 删除旧数据库
rm backend/sql_app.db

# 重新初始化
docker-compose exec backend python init_db.py
```

---

## 📚 下一步

- 📖 阅读 [用户使用指南](docs/USER_GUIDE.md)
- 🚀 查看 [部署指南](docs/DEPLOYMENT.md)
- 🔌 了解 [API文档](docs/API.md)
- 💡 探索更多功能特性

---

## 💬 获取帮助

遇到问题？

1. 查看项目文档
2. 检查 [常见问题](docs/USER_GUIDE.md#常见问题)
3. 提交 GitHub Issue
4. 联系技术支持

---

**祝您使用愉快！🎉**



