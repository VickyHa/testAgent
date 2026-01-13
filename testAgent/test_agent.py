"""
测试智能体主类
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from testAgent.config import BROWSER_CONFIG, TARGET_URL, REPORTS_DIR
from testAgent.scenarios.base_scenario import TestScenario
from testAgent.scenarios import HomepageScenario, NavigationScenario
from testAgent.planner import Planner, Plan
from testAgent.actor import Actor
from testAgent.reporter import Reporter


class TestAgent:
    """测试智能体 - 负责执行测试场景并生成报告"""
    
    def __init__(self):
        self.scenarios: List[TestScenario] = []
        self.results: List[Dict[str, Any]] = []
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.planner = Planner()
        self.reporter = Reporter()
        self.last_plan: Optional[Plan] = None
        
    def register_scenario(self, scenario: TestScenario):
        """注册测试场景"""
        self.scenarios.append(scenario)
    
    def initialize_browser(self):
        """初始化浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=BROWSER_CONFIG["headless"],
            slow_mo=BROWSER_CONFIG["slow_mo"]
        )
        self.context = self.browser.new_context(
            viewport=BROWSER_CONFIG["viewport"]
        )
        self.page = self.context.new_page()
    
    def close_browser(self):
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def create_plan(self, instruction: str) -> Dict[str, Any]:
        """Planner: 从自然语言生成结构化计划"""
        self.last_plan = self.planner.create_plan(instruction)
        return self.last_plan.to_dict()

    def run_plan(self, instruction: Optional[str] = None) -> Dict[str, Any]:
        """
        Actor + Reporter: 执行计划并汇总结果
        返回 summary，包含可直接用于报告生成的结构
        """
        plan = self.last_plan
        if instruction:
            plan = self.planner.create_plan(instruction)
            self.last_plan = plan
        if not plan:
            raise ValueError("请先通过 create_plan 生成计划或传入指令")

        self.start_time = datetime.now()
        try:
            self.initialize_browser()
            actor = Actor(self.page, self.context)
            step_results = actor.execute_plan(plan.to_dict()["steps"])
        finally:
            self.close_browser()
            self.end_time = datetime.now()

        scenario = self.reporter.build_scenario_result(
            plan.to_dict(), step_results, self.start_time, self.end_time
        )
        self.results.append(scenario)
        summary = self.reporter.build_summary([scenario])
        return {
            "plan": plan.to_dict(),
            "summary": summary,
            "scenario": scenario,
        }
    
    def run_scenario(self, scenario: TestScenario) -> bool:
        """运行单个测试场景"""
        if not self.page:
            self.initialize_browser()
        
        scenario.start_time = datetime.now()
        scenario.status = "running"
        
        try:
            result = scenario.execute(self.page, self.context)
            scenario.status = "passed" if result else "failed"
        except Exception as e:
            scenario.status = "failed"
            scenario.error_message = str(e)
            result = False
        finally:
            scenario.end_time = datetime.now()
        
        self.results.append(scenario.to_dict())
        return result
    
    def run_all_scenarios(self) -> Dict[str, Any]:
        """运行所有注册的测试场景"""
        self.start_time = datetime.now()
        
        if not self.scenarios:
            return {
                "status": "error",
                "message": "没有注册的测试场景"
            }
        
        try:
            self.initialize_browser()
            
            passed = 0
            failed = 0
            
            for scenario in self.scenarios:
                print(f"\n正在执行: {scenario.name}")
                result = self.run_scenario(scenario)
                if result:
                    passed += 1
                    print(f"✓ {scenario.name} - 通过")
                else:
                    failed += 1
                    print(f"✗ {scenario.name} - 失败")
                    if scenario.error_message:
                        print(f"  错误: {scenario.error_message}")
        
        finally:
            self.close_browser()
            self.end_time = datetime.now()
        
        summary = {
            "total": len(self.scenarios),
            "passed": passed,
            "failed": failed,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0,
            "scenarios": self.results
        }
        
        return summary
    
    def run_scenario_by_name(self, scenario_name: str) -> Optional[Dict[str, Any]]:
        """根据名称运行特定测试场景"""
        scenario = next((s for s in self.scenarios if s.name == scenario_name), None)
        if not scenario:
            return None
        
        try:
            self.initialize_browser()
            result = self.run_scenario(scenario)
            return scenario.to_dict()
        finally:
            self.close_browser()
    
    def get_available_scenarios(self) -> List[Dict[str, str]]:
        """获取所有可用的测试场景"""
        return [
            {
                "name": scenario.name,
                "description": scenario.description
            }
            for scenario in self.scenarios
        ]

