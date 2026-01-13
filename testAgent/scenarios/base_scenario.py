"""
基础测试场景类
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from playwright.sync_api import Page, BrowserContext


class TestScenario(ABC):
    """测试场景基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.steps: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.status: str = "pending"  # pending, running, passed, failed, skipped
        self.error_message: Optional[str] = None
        self.screenshots: List[str] = []
        
    @abstractmethod
    def execute(self, page: Page, context: BrowserContext) -> bool:
        """
        执行测试场景
        返回: True 表示测试通过，False 表示测试失败
        """
        pass
    
    def add_step(self, step_name: str, action: str, expected: str = ""):
        """添加测试步骤"""
        self.steps.append({
            "name": step_name,
            "action": action,
            "expected": expected,
            "status": "pending",
            "timestamp": None,
        })
    
    def record_step_result(self, step_index: int, status: str, message: str = ""):
        """记录步骤执行结果"""
        if 0 <= step_index < len(self.steps):
            self.steps[step_index]["status"] = status
            self.steps[step_index]["timestamp"] = datetime.now().isoformat()
            self.steps[step_index]["message"] = message
    
    def take_screenshot(self, page: Page, name: str) -> str:
        """截图并保存"""
        from pathlib import Path
        from testAgent.config import SCREENSHOTS_DIR
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.name}_{name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        page.screenshot(path=str(filepath))
        self.screenshots.append(str(filepath))
        return str(filepath)
    
    def get_duration(self) -> float:
        """获取测试执行时长（秒）"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，用于报告生成"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.get_duration(),
            "steps": self.steps,
            "error_message": self.error_message,
            "screenshots": self.screenshots,
        }

