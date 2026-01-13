"""
主程序入口
"""
import sys
from pathlib import Path

# 添加项目根目录到路径，支持从testAgent目录直接运行
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from testAgent.chat_interface import ChatInterface


def main():
    """主函数"""
    interface = ChatInterface()
    interface.run()


if __name__ == "__main__":
    main()

