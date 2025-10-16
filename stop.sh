#!/bin/bash

# 协同数字化平台停止脚本

echo "正在停止应用..."

# 查找Python进程
PID=$(ps aux | grep "python app.py" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "应用未在运行"
else
    kill $PID
    echo "应用已停止 (PID: $PID)"
fi

