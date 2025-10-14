@echo off
chcp 65001 >nul
echo ================================
echo 省专协同数字化平台 - 启动脚本
echo ================================
echo.

echo [1/4] 检查Docker环境...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未安装或未启动
    echo 请先安装Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker环境正常

echo.
echo [2/4] 检查配置文件...
if not exist "backend\.env" (
    echo ⚠️  未找到环境配置文件
    echo 正在复制配置模板...
    copy "backend\.env.example" "backend\.env" >nul
    echo ✅ 已创建 backend\.env
    echo.
    echo ⚠️  请编辑 backend\.env 文件，配置你的 OPENAI_API_KEY
    echo    配置完成后请重新运行此脚本
    pause
    exit /b 0
)
echo ✅ 配置文件存在

echo.
echo [3/4] 启动Docker服务...
docker-compose up -d
if errorlevel 1 (
    echo ❌ 服务启动失败
    pause
    exit /b 1
)

echo.
echo [4/4] 等待服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 检查服务状态...
docker-compose ps

echo.
echo ================================
echo ✅ 服务启动成功！
echo ================================
echo.
echo 📱 访问地址：
echo    前端界面: http://localhost:3000
echo    后端API:  http://localhost:8000
echo    API文档:  http://localhost:8000/docs
echo.
echo 👤 默认账号：
echo    用户名: admin
echo    密码:   admin123
echo.
echo ⚠️  首次使用需要初始化数据库：
echo    运行命令: docker-compose exec backend python init_db.py
echo.
echo 💡 常用命令：
echo    查看日志: docker-compose logs -f
echo    停止服务: docker-compose down
echo    重启服务: docker-compose restart
echo.
pause



