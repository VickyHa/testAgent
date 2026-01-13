"""
配置文件 - 测试智能体配置
"""
import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
SCENARIOS_DIR = BASE_DIR / "scenarios"

# 创建必要的目录
REPORTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
SCENARIOS_DIR.mkdir(exist_ok=True)

# 目标网站配置
TARGET_URL = "https://opencsg.com/agentichub"
BASE_URL = "https://opencsg.com"

# 浏览器配置
BROWSER_CONFIG = {
    "headless": False,  # 设置为 True 可无头模式运行
    "slow_mo": 100,  # 操作延迟（毫秒），便于观察
    "viewport": {"width": 1920, "height": 1080},
    "timeout": 30000,  # 默认超时时间（毫秒）
}

# 测试配置
TEST_CONFIG = {
    "screenshot_on_failure": True,
    "screenshot_on_success": False,
    "video_on_failure": True,
    "retry_count": 2,
    "wait_timeout": 5000,
}

# 登录配置（如果需要）
LOGIN_CONFIG = {
    "username": os.getenv("TEST_USERNAME", ""),
    "password": os.getenv("TEST_PASSWORD", ""),
    "login_url": "https://iam.opencsg.com/login",
}

