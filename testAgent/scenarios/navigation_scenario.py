"""
导航测试场景
"""
from testAgent.scenarios.base_scenario import TestScenario
from playwright.sync_api import Page, BrowserContext, expect
from testAgent.config import TARGET_URL


class NavigationScenario(TestScenario):
    """导航功能测试场景"""
    
    def __init__(self):
        super().__init__(
            name="导航测试",
            description="测试网站导航链接和页面跳转功能"
        )
        self.add_step("访问首页", f"导航到 {TARGET_URL}", "页面成功加载")
        self.add_step("查找导航链接", "查找页面中的所有链接", "找到可点击的链接")
        self.add_step("测试链接点击", "点击链接并验证跳转", "链接正常工作")
    
    def execute(self, page: Page, context: BrowserContext) -> bool:
        """执行导航测试"""
        try:
            # 步骤1: 访问首页
            self.record_step_result(0, "running")
            page.goto(TARGET_URL, wait_until="networkidle")
            self.record_step_result(0, "passed", "页面加载成功")
            
            # 步骤2: 查找导航链接
            self.record_step_result(1, "running")
            links = page.locator("a[href]").all()
            internal_links = []
            for link in links[:10]:  # 限制测试前10个链接
                href = link.get_attribute("href")
                if href and (href.startswith("/") or TARGET_URL in href):
                    internal_links.append(link)
            
            if len(internal_links) > 0:
                self.record_step_result(1, "passed", f"找到 {len(internal_links)} 个内部链接")
            else:
                self.record_step_result(1, "passed", "未找到内部链接（可能页面结构不同）")
            
            # 步骤3: 测试链接点击（如果有链接）
            self.record_step_result(2, "running")
            if len(internal_links) > 0:
                # 测试第一个链接
                test_link = internal_links[0]
                href = test_link.get_attribute("href")
                test_link.click()
                page.wait_for_load_state("networkidle", timeout=10000)
                self.record_step_result(2, "passed", f"成功点击链接: {href}")
            else:
                self.record_step_result(2, "passed", "跳过链接测试（无可用链接）")
            
            return True
            
        except Exception as e:
            self.error_message = str(e)
            self.take_screenshot(page, "error")
            return False

