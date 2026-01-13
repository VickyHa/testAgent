#!/bin/bash

echo "========================================"
echo "OpenCSG AgenticHub 测试智能体"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

# 确定 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# 检查依赖是否安装
echo "检查依赖..."
if ! $PYTHON_CMD -c "import playwright" 2>/dev/null; then
    echo "[提示] 正在安装依赖..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
    echo "[提示] 正在安装 Playwright 浏览器..."
    $PYTHON_CMD -m playwright install chromium
fi

# 启动程序
echo ""
echo "启动测试智能体..."
echo ""
$PYTHON_CMD main.py
