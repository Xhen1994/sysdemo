#!/bin/bash

echo "================================"
echo "省专协同数字化平台 - 启动脚本"
echo "================================"
echo ""

echo "[1/4] 检查Docker环境..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✅ Docker环境正常"

echo ""
echo "[2/4] 检查配置文件..."
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到环境配置文件"
    echo "正在复制配置模板..."
    cp backend/.env.example backend/.env
    echo "✅ 已创建 backend/.env"
    echo ""
    echo "⚠️  请编辑 backend/.env 文件，配置你的 OPENAI_API_KEY"
    echo "   配置完成后请重新运行此脚本"
    exit 0
fi
echo "✅ 配置文件存在"

echo ""
echo "[3/4] 启动Docker服务..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ 服务启动失败"
    exit 1
fi

echo ""
echo "[4/4] 等待服务启动..."
sleep 5

echo ""
echo "检查服务状态..."
docker-compose ps

echo ""
echo "================================"
echo "✅ 服务启动成功！"
echo "================================"
echo ""
echo "📱 访问地址："
echo "   前端界面: http://localhost:3000"
echo "   后端API:  http://localhost:8000"
echo "   API文档:  http://localhost:8000/docs"
echo ""
echo "👤 默认账号："
echo "   用户名: admin"
echo "   密码:   admin123"
echo ""
echo "⚠️  首次使用需要初始化数据库："
echo "   运行命令: docker-compose exec backend python init_db.py"
echo ""
echo "💡 常用命令："
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo ""



