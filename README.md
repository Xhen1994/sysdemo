# 协同数字化平台

## 项目简介

这是一个面向省级单位的协同数字化平台，提供目标管理、问题反馈、工作流管理、知识库和数据看板等功能。

## 主要功能

### 1. 目标管理
- 目标下发与分解
- 进度上报与跟踪
- 目标审核与统计分析
- 支持父子目标关系

### 2. 需求与问题反馈
- 问题分类管理
- 优先级设置
- 流转与闭环管理
- AI智能总结（基于DeepSeek）

### 3. 工作流管理
- 支撑任务创建与派单
- 自动派单与人工调整
- 工作日志记录
- 任务验收流程

### 4. 知识库
- 支持Markdown格式
- 分类与标签管理
- 搜索功能
- 浏览统计

### 5. 数据看板
- 可视化图表展示
- 目标完成率统计
- 问题处理效率分析
- 任务分布概览

### 6. 系统管理
- 用户与角色管理
- 权限配置
- 系统日志查看
- 参数设置

## 技术栈

- **后端框架**: Flask 3.0
- **前端**: Bootstrap 5, Chart.js
- **数据存储**: JSON/JSONL文件
- **AI集成**: DeepSeek API
- **Python版本**: 3.11

## 部署说明

### 1. 环境准备

```bash
# 创建conda环境
conda create -n sysdemo python=3.11
conda activate sysdemo

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，设置必要的配置
nano .env
```

重要配置项：
- `SECRET_KEY`: 应用密钥，生产环境必须修改
- `DEEPSEEK_API_KEY`: DeepSeek API密钥（可选，用于AI功能）

### 3. 启动应用

#### Linux服务器部署

```bash
# 赋予执行权限
chmod +x start.sh stop.sh restart.sh

# 启动应用
./start.sh

# 停止应用
./stop.sh

# 重启应用
./restart.sh
```

#### 本地开发模式

```bash
# 直接运行
python app.py
```

### 4. 访问应用

- 服务器地址: http://14.103.165.46:4000
- 默认管理员账号: `admin`
- 默认密码: `admin123`

**⚠️ 重要提示**: 首次登录后请立即修改默认密码！

## 目录结构

```
sysdemo/
├── app.py              # 应用入口
├── config.py           # 配置文件
├── requirements.txt    # Python依赖
├── models/             # 数据模型
│   ├── user.py
│   └── data_manager.py
├── routes/             # 路由模块
│   ├── auth.py        # 认证
│   ├── objectives.py  # 目标管理
│   ├── issues.py      # 问题反馈
│   ├── tasks.py       # 工作流
│   ├── knowledge.py   # 知识库
│   ├── dashboard.py   # 数据看板
│   └── admin.py       # 系统管理
├── services/           # 服务层
│   └── ai_service.py  # AI服务
├── templates/          # HTML模板
│   ├── base.html
│   ├── auth/
│   ├── objectives/
│   ├── issues/
│   ├── tasks/
│   ├── knowledge/
│   ├── dashboard/
│   └── admin/
├── data/               # 数据存储目录
│   ├── users.json
│   ├── objectives.json
│   ├── issues.jsonl
│   ├── tasks.jsonl
│   ├── knowledge.json
│   └── system_logs.jsonl
├── logs/               # 日志目录
├── start.sh            # 启动脚本
├── stop.sh             # 停止脚本
└── restart.sh          # 重启脚本
```

## 用户角色

### 系统管理员 (admin)
- 拥有所有权限
- 管理用户和角色
- 查看系统日志
- 配置系统参数

### 省级管理员 (province_manager)
- 管理本省目标和任务
- 审核本省目标进度
- 分配问题和任务
- 使用AI功能

### 普通员工 (staff)
- 查看和更新自己的目标
- 提交问题反馈
- 执行分配的任务
- 访问知识库

## 数据备份

数据存储在 `data/` 目录下，建议定期备份：

```bash
# 备份数据
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# 恢复数据
tar -xzf backup-YYYYMMDD.tar.gz
```

## 故障排查

### 应用无法启动

1. 检查端口4000是否被占用：
```bash
netstat -tuln | grep 4000
```

2. 检查日志文件：
```bash
tail -f logs/app.log
```

3. 确认conda环境已激活：
```bash
conda env list
```

### AI功能无法使用

1. 确认已设置DeepSeek API密钥
2. 检查网络连接
3. 查看系统日志获取详细错误信息

## 安全建议

1. **修改默认密码**: 首次登录后立即修改admin账号密码
2. **设置SECRET_KEY**: 生产环境使用随机生成的密钥
3. **配置防火墙**: 限制4000端口的访问来源
4. **定期备份**: 定期备份data目录
5. **更新依赖**: 定期更新Python依赖包

## 开发说明

### 添加新功能

1. 在 `routes/` 目录创建新的路由文件
2. 在 `templates/` 目录创建对应的HTML模板
3. 在 `routes/__init__.py` 中注册新的蓝图

### 数据模型

数据使用JSON/JSONL格式存储：
- JSON: 用于存储列表数据（如用户、角色、目标、知识库）
- JSONL: 用于存储日志型数据（如问题反馈、任务、系统日志）

## 联系支持

如有问题或建议，请联系系统管理员。

## 许可证

本项目为内部使用系统。

