# 部署指南

## 部署方式

### 方式一：Docker Compose（推荐）

这是最简单快速的部署方式，适合开发和生产环境。

#### 前置要求
- Docker 20.10+
- Docker Compose 2.0+

#### 部署步骤

1. **克隆项目并配置环境变量**

```bash
cd sysdemo

# 配置后端环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入你的配置
```

2. **配置AI API密钥**

编辑 `backend/.env` 文件：

```env
# AI API配置 - 必须配置
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo

# 数据库配置（Docker会自动配置）
DATABASE_URL=postgresql://sysdemo:sysdemo123@db:5432/sysdemo

# JWT密钥（建议修改为更安全的密钥）
SECRET_KEY=your-secret-key-change-this-in-production
```

3. **启动服务**

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

4. **初始化数据库**

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行初始化脚本
python init_db.py

# 退出容器
exit
```

5. **访问应用**

- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

6. **停止服务**

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

---

### 方式二：手动部署

适合需要自定义配置或调试的场景。

#### 后端部署

1. **安装依赖**

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
```

2. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，填入配置
```

3. **初始化数据库**

```bash
python init_db.py
```

4. **启动后端服务**

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 前端部署

1. **安装依赖**

```bash
cd frontend
npm install
```

2. **开发模式**

```bash
npm start
# 访问 http://localhost:3000
```

3. **生产构建**

```bash
npm run build

# 使用静态服务器部署
npm install -g serve
serve -s dist -l 3000
```

---

## 生产环境部署建议

### 1. 使用PostgreSQL数据库

修改 `backend/.env`：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/sysdemo
```

### 2. 使用Nginx反向代理

创建 `/etc/nginx/sites-available/sysdemo`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 后端API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket支持（如需要）
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

启用站点：

```bash
ln -s /etc/nginx/sites-available/sysdemo /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 3. 配置HTTPS

使用 Let's Encrypt：

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

### 4. 配置系统服务

创建 `/etc/systemd/system/sysdemo-backend.service`：

```ini
[Unit]
Description=SysDemo Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/sysdemo/backend
Environment="PATH=/var/www/sysdemo/backend/venv/bin"
ExecStart=/var/www/sysdemo/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
systemctl enable sysdemo-backend
systemctl start sysdemo-backend
systemctl status sysdemo-backend
```

### 5. 配置日志和监控

- 使用 `logrotate` 管理日志文件
- 配置 Prometheus + Grafana 监控
- 使用 Sentry 收集错误日志

### 6. 备份策略

定期备份数据库：

```bash
# 创建备份脚本 /usr/local/bin/backup-sysdemo.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U sysdemo sysdemo > /backup/sysdemo_$DATE.sql
find /backup -name "sysdemo_*.sql" -mtime +7 -delete

# 添加到crontab
crontab -e
# 每天凌晨2点备份
0 2 * * * /usr/local/bin/backup-sysdemo.sh
```

---

## 环境变量说明

### 后端环境变量

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| DATABASE_URL | 数据库连接URL | sqlite:///./sql_app.db | 是 |
| OPENAI_API_KEY | OpenAI API密钥 | - | 是 |
| OPENAI_API_BASE | OpenAI API地址 | https://api.openai.com/v1 | 否 |
| AI_MODEL | AI模型名称 | gpt-3.5-turbo | 否 |
| SECRET_KEY | JWT密钥 | - | 是 |
| ALGORITHM | JWT算法 | HS256 | 否 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token过期时间（分钟） | 30 | 否 |
| REDIS_URL | Redis连接URL | redis://localhost:6379/0 | 否 |
| ALLOWED_ORIGINS | CORS允许的源 | http://localhost:3000 | 否 |

---

## 故障排查

### 1. 数据库连接失败

检查数据库配置和网络连接：

```bash
# 测试PostgreSQL连接
psql -h localhost -U sysdemo -d sysdemo

# 检查Docker网络
docker-compose ps
docker network ls
```

### 2. AI功能不可用

检查API密钥配置：

```bash
# 查看后端日志
docker-compose logs backend

# 测试API调用
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 3. 前端无法连接后端

检查代理配置和CORS设置：

```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 检查前端代理配置
cat frontend/vite.config.ts
```

### 4. 权限问题

```bash
# 修复文件权限
chown -R www-data:www-data /var/www/sysdemo

# 检查SELinux（如果使用）
setenforce 0
```

---

## 性能优化

### 1. 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_issues_status ON issues(status);
CREATE INDEX idx_issues_created_at ON issues(created_at);
CREATE INDEX idx_issues_creator_id ON issues(creator_id);
```

### 2. 启用Redis缓存

配置Redis用于缓存热点数据和会话管理。

### 3. CDN加速

将前端静态资源部署到CDN，提升访问速度。

### 4. 数据库连接池

在 `backend/app/core/database.py` 中配置连接池：

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

---

## 安全建议

1. **修改默认密码**：修改数据库和管理员账号的默认密码
2. **使用强密钥**：为JWT生成强随机密钥
3. **配置防火墙**：限制数据库和Redis的访问
4. **定期更新**：及时更新依赖包和系统补丁
5. **API限流**：配置请求频率限制
6. **输入验证**：严格验证用户输入
7. **日志审计**：记录关键操作日志

---

## 扩展性

### 水平扩展

1. 使用负载均衡器（如Nginx）分发请求
2. 部署多个后端实例
3. 使用共享的PostgreSQL和Redis
4. 配置会话共享

### 垂直扩展

1. 增加服务器CPU和内存
2. 优化数据库配置
3. 使用SSD存储

---

## 监控和告警

推荐工具：

- **Prometheus + Grafana**：系统指标监控
- **ELK Stack**：日志聚合分析
- **Sentry**：错误追踪
- **Uptime Robot**：服务可用性监控

---

## 技术支持

如遇到问题，请：

1. 查看日志文件
2. 查阅项目文档
3. 提交GitHub Issue
4. 联系技术支持团队



