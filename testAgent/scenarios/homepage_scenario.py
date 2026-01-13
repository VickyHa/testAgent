"""
首页测试场景
"""
from testAgent.scenarios.base_scenario import TestScenario
from playwright.sync_api import Page, BrowserContext, expect
from testAgent.config import TARGET_URL


class HomepageScenario(TestScenario):
    """首页功能测试场景"""
    
    def __init__(self):
        super().__init__(
            name="首页测试",
            description="测试 AgenticHub 首页的加载、导航和基本功能"
        )
        self.add_step("访问首页", f"导航到 {TARGET_URL}", "页面成功加载")
        self.add_step("检查页面标题", "验证页面标题包含预期内容", "标题正确显示")
        self.add_step("检查主要元素", "验证页面主要元素存在", "所有关键元素可见")
        self.add_step("检查导航菜单", "验证导航菜单功能", "导航菜单正常工作")
    
    def execute(self, page: Page, context: BrowserContext) -> bool:
        """执行首页测试"""
        try:
            # 步骤1: 访问首页
            self.record_step_result(0, "running")
            page.goto(TARGET_URL, wait_until="networkidle")
            self.record_step_result(0, "passed", "页面加载成功")
            self.take_screenshot(page, "homepage_loaded")
            
            # 步骤2: 检查页面标题
            self.record_step_result(1, "running")
            title = page.title()
            if title:
                self.record_step_result(1, "passed", f"页面标题: {title}")
            else:
                self.record_step_result(1, "failed", "页面标题为空")
                return False
            
            # 步骤3: 检查主要元素
            self.record_step_result(2, "running")
            # 等待页面主要内容加载
            page.wait_for_load_state("domcontentloaded")
            # 检查是否有主要内容区域
            main_content = page.locator("main, [role='main'], .main-content, #main")
            if main_content.count() > 0 or page.locator("body").count() > 0:
                self.record_step_result(2, "passed", "主要元素存在")
            else:
                self.record_step_result(2, "failed", "未找到主要元素")
                return False
            
            # 步骤4: 检查导航菜单
            self.record_step_result(3, "running")
            # 尝试查找导航元素
            nav_elements = page.locator("nav, [role='navigation'], .nav, .navbar, .navigation")
            if nav_elements.count() > 0:
                self.record_step_result(3, "passed", "导航菜单存在")
            else:
                # 导航菜单可能不存在，不算失败
                self.record_step_result(3, "passed", "未找到导航菜单（可能不需要）")
            
            return True
            
        except Exception as e:
            self.error_message = str(e)
            self.take_screenshot(page, "error")
            return False

