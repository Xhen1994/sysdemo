#!/bin/bash

# 协同数字化平台启动脚本
# 用于在Linux服务器上启动应用

echo "========================================="
echo "  协同数字化平台启动脚本"
echo "========================================="
echo ""

# 设置项目路径
PROJECT_DIR="/home/xhen/myprojects/sysdemo"
CONDA_ENV="sysdemo"
CONDA_PATH="/home/xhen/miniconda3"

# 切换到项目目录
cd $PROJECT_DIR

# 激活conda环境
echo "正在激活conda环境: $CONDA_ENV"
source $CONDA_PATH/bin/activate $CONDA_ENV

# 检查Python版本
echo ""
echo "Python版本:"
python --version

# 检查依赖
echo ""
echo "检查依赖..."
pip install -r requirements.txt

# 设置环境变量（可选）
# export DEEPSEEK_API_KEY="your_api_key_here"

# 创建数据目录
mkdir -p data
mkdir -p data/uploads

# 启动应用
echo ""
echo "========================================="
echo "  正在启动应用..."
echo "  访问地址: http://14.103.165.46:4000"
echo "  默认管理员账号: admin / admin123"
echo "========================================="
echo ""

# 使用nohup在后台运行
nohup python app.py > logs/app.log 2>&1 &

echo "应用已启动，PID: $!"
echo "日志文件: logs/app.log"
echo ""
echo "停止应用请运行: ./stop.sh"

