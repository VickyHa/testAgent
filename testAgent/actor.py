"""
Actor - 执行器，使用 Playwright 执行计划步骤
"""
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime
from playwright.sync_api import Page, BrowserContext, TimeoutError as PlaywrightTimeoutError
from testAgent.config import SCREENSHOTS_DIR, TEST_CONFIG


class Actor:
    """
    Actor（执行者）
    - 接收结构化步骤
    - 调用 Playwright 执行
    - 返回每步的状态、消息、截图
    """

    def __init__(self, page: Page, context: BrowserContext):
        self.page = page
        self.context = context

    def execute_plan(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for step in steps:
            result = self._execute_step(step)
            results.append(result)
            if result["status"] == "failed":
                # 失败则根据配置决定是否继续，这里简单地继续执行剩余步骤
                continue
        return results

    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        action = step.get("action")
        target = step.get("target", "")
        value = step.get("value", "")
        expect = step.get("expect", "")

        start = datetime.now()
        status = "passed"
        message = ""
        screenshot_path = ""

        try:
            if action == "goto":
                self.page.goto(target, wait_until="networkidle")
                message = "页面导航成功"

            elif action == "click":
                self.page.click(target, timeout=TEST_CONFIG["wait_timeout"])
                message = f"点击 {target} 成功"

            elif action == "fill":
                # value 中如果包含占位变量，从环境变量读取
                resolved = self._resolve_value(value)
                self.page.fill(target, resolved, timeout=TEST_CONFIG["wait_timeout"])
                message = "输入完成"

            elif action == "upload":
                resolved_path = Path(value)
                if not resolved_path.exists():
                    raise FileNotFoundError(f"未找到上传文件: {resolved_path}")
                input_handle = self.page.locator(target).first
                input_handle.set_input_files(str(resolved_path))
                message = f"上传 {resolved_path.name} 成功"

            elif action == "wait_for_text":
                self.page.get_by_text(target).wait_for(timeout=TEST_CONFIG["wait_timeout"])
                message = f"找到文本: {target}"

            elif action == "wait_for_selector":
                self.page.locator(target).first.wait_for(timeout=TEST_CONFIG["wait_timeout"])
                message = f"找到元素: {target}"

            elif action == "screenshot":
                screenshot_path = self._screenshot(step.get("target", "step"))
                message = f"截图已保存: {screenshot_path}"

            else:
                status = "skipped"
                message = f"未知动作: {action}"

        except PlaywrightTimeoutError:
            status = "failed"
            message = f"超时: {action} -> {target}"
        except Exception as exc:
            status = "failed"
            message = f"异常: {exc}"

        end = datetime.now()
        duration = (end - start).total_seconds()

        if status == "failed" and TEST_CONFIG["screenshot_on_failure"]:
            screenshot_path = screenshot_path or self._screenshot(f"error_step_{step.get('id', 'x')}")

        return {
            "id": step.get("id"),
            "name": step.get("note") or step.get("action"),
            "action": action,
            "target": target,
            "expected": expect,
            "value": value,
            "status": status,
            "message": message,
            "screenshot": screenshot_path,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }

    def _resolve_value(self, value: str) -> str:
        """解析占位符，如 {{TEST_USERNAME}}"""
        import os

        if value.startswith("{{") and value.endswith("}}"):
            env_key = value.strip("{} ")
            return os.getenv(env_key, "")
        return value

    def _screenshot(self, name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = SCREENSHOTS_DIR / f"{name}_{timestamp}.png"
        self.page.screenshot(path=str(filepath))
        return str(filepath)
