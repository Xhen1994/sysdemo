# 快速参考卡片 🚀

> 一页纸搞定常用操作

## 🎯 一分钟启动

```bash
# 1. 配置API密钥
cp backend/env.example.txt backend/.env
# 编辑backend/.env，填入OPENAI_API_KEY

# 2. 启动服务
docker-compose up -d

# 3. 初始化数据库
docker-compose exec backend python init_db.py

# 4. 访问 http://localhost:3000
# 账号: admin / admin123
```

## 📍 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端 | http://localhost:3000 | Web界面 |
| 后端 | http://localhost:8000 | API服务 |
| API文档 | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | API文档（ReDoc） |

## 🔑 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |

## 💻 常用命令

### Docker操作

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 查看某个服务的日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 重新构建
docker-compose build

# 查看服务状态
docker-compose ps
```

### 数据库操作

```bash
# 初始化数据库
docker-compose exec backend python init_db.py

# 进入后端容器
docker-compose exec backend bash

# 进入数据库（SQLite）
docker-compose exec backend sqlite3 sql_app.db
```

### 本地开发

```bash
# 后端开发
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload

# 前端开发
cd frontend
npm install
npm start
```

## 📁 重要文件位置

| 文件/目录 | 路径 | 说明 |
|----------|------|------|
| 环境变量 | `backend/.env` | API密钥等配置 |
| 数据库 | `backend/sql_app.db` | SQLite数据库文件 |
| 后端日志 | `docker-compose logs backend` | 后端运行日志 |
| 前端配置 | `frontend/vite.config.ts` | Vite配置 |

## 🔧 环境变量速查

```env
# 必须配置
OPENAI_API_KEY=sk-your-key-here

# 可选配置
DATABASE_URL=sqlite:///./sql_app.db
AI_MODEL=gpt-3.5-turbo
SECRET_KEY=your-secret-key
```

## 🌐 API端点速查

### 认证
- POST `/api/v1/auth/register` - 注册
- POST `/api/v1/auth/login` - 登录

### 问题管理
- GET `/api/v1/issues` - 获取问题列表
- POST `/api/v1/issues` - 创建问题
- GET `/api/v1/issues/{id}` - 获取问题详情
- PUT `/api/v1/issues/{id}` - 更新问题
- DELETE `/api/v1/issues/{id}` - 删除问题

### AI功能
- POST `/api/v1/ai/summarize` - AI摘要
- POST `/api/v1/ai/analyze/{id}` - 分析问题
- GET `/api/v1/ai/trends` - 趋势分析
- GET `/api/v1/ai/suggestions/{id}` - 解决方案建议

## 🐛 常见问题快速解决

### 问题1：无法启动Docker
```bash
# 检查Docker是否运行
docker version

# 检查端口占用
netstat -ano | findstr "3000 8000"  # Windows
lsof -i :3000  # Linux/Mac
```

### 问题2：AI功能不工作
```bash
# 1. 检查API密钥配置
cat backend/.env | grep OPENAI_API_KEY

# 2. 查看后端日志
docker-compose logs backend | grep -i error

# 3. 测试API连接
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

### 问题3：前端无法连接后端
```bash
# 1. 检查后端是否运行
curl http://localhost:8000/health

# 2. 检查CORS配置
grep ALLOWED_ORIGINS backend/.env

# 3. 查看浏览器控制台错误
```

### 问题4：数据库连接失败
```bash
# 删除旧数据库，重新初始化
rm backend/sql_app.db
docker-compose exec backend python init_db.py
```

## 📊 功能清单

### 核心功能
- ✅ 用户认证和授权
- ✅ 问题CRUD操作
- ✅ 问题搜索和筛选
- ✅ AI自动摘要
- ✅ AI标签生成
- ✅ AI分类建议
- ✅ AI趋势分析
- ✅ 问题评论
- ✅ 问题反馈
- ✅ 数据统计

### 管理功能
- ✅ 部门管理
- ✅ 项目管理
- ✅ 用户管理
- ✅ 权限控制

## 🎨 页面导航

```
登录页 (/login)
  ↓
工作台 (/)
  ├── 问题管理 (/issues)
  │   ├── 问题列表
  │   ├── 创建问题 (/issues/create)
  │   └── 问题详情 (/issues/:id)
  ├── 部门管理 (/departments)
  ├── 项目管理 (/projects)
  └── AI智能分析 (/ai-analysis)
```

## 📚 文档速查

| 文档 | 用途 | 适合人群 |
|------|------|----------|
| [README.md](README.md) | 项目介绍 | 所有人 |
| [QUICKSTART.md](QUICKSTART.md) | 5分钟上手 | 新用户 |
| [USER_GUIDE.md](docs/USER_GUIDE.md) | 功能使用 | 普通用户 |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | 生产部署 | 运维人员 |
| [API.md](docs/API.md) | API说明 | 开发者 |
| [STRUCTURE.md](STRUCTURE.md) | 代码结构 | 开发者 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 技术架构 | 技术人员 |

## 🔥 快捷键

### 开发调试
```bash
# 快速重启后端
docker-compose restart backend

# 快速重启前端
docker-compose restart frontend

# 查看实时日志
docker-compose logs -f --tail=100

# 清理并重新开始
docker-compose down -v
docker-compose up -d
```

## 💡 最佳实践

1. **定期备份数据库**
   ```bash
   cp backend/sql_app.db backup_$(date +%Y%m%d).db
   ```

2. **生产环境修改默认密码**
   ```bash
   # 登录后立即修改admin密码
   ```

3. **配置强密钥**
   ```env
   SECRET_KEY=使用随机生成的长密钥
   ```

4. **监控AI API使用量**
   - 定期检查OpenAI账单
   - 设置使用限制

5. **定期更新依赖**
   ```bash
   pip list --outdated  # 后端
   npm outdated         # 前端
   ```

## 📞 获取帮助

1. 📖 查看相关文档
2. 🔍 搜索GitHub Issues
3. 💬 提交新Issue
4. 📧 联系技术支持

## ⚡ 性能优化提示

- 使用PostgreSQL替代SQLite（生产环境）
- 启用Redis缓存
- 配置CDN加速前端资源
- 调整AI API超时时间
- 优化数据库索引

## 🎯 下一步

1. ✅ 项目已100%完成
2. 📖 阅读用户手册了解详细功能
3. 🚀 部署到生产环境
4. 💡 根据需求定制开发

---

**保存此页面，快速查找常用信息！** ⭐



