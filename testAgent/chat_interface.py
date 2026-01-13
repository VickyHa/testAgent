"""
对话式测试交互界面
"""
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from testAgent.test_agent import TestAgent
from testAgent.report_generator import ReportGenerator
from testAgent.scenarios import HomepageScenario, NavigationScenario


class ChatInterface:
    """对话式测试交互界面"""
    
    def __init__(self):
        self.console = Console()
        self.agent = TestAgent()
        self.report_generator = ReportGenerator()
        self._register_default_scenarios()
        self.last_plan: Optional[Dict[str, Any]] = None
        self.last_summary: Optional[Dict[str, Any]] = None
    
    def _register_default_scenarios(self):
        """注册默认测试场景"""
        self.agent.register_scenario(HomepageScenario())
        self.agent.register_scenario(NavigationScenario())
    
    def print_welcome(self):
        """打印欢迎信息"""
        welcome_text = """
🧪 OpenCSG AgenticHub 自动化测试智能体

这个智能体可以帮助您：
  • Planner：将自然语言转为结构化测试计划
  • Actor：用 Playwright 执行计划步骤
  • Reporter：生成可读的测试报告

输入 'help' 查看可用命令
输入 'exit' 退出程序
        """
        self.console.print(Panel(welcome_text, title="欢迎", border_style="blue"))
    
    def print_help(self):
        """打印帮助信息"""
        help_text = """
可用命令：

  list          - 列出所有可用的测试场景
  run <name>    - 运行指定的测试场景（旧模式）
  run all       - 运行所有测试场景（旧模式）
  plan <需求>   - 生成结构化测试计划
  exec          - 执行最近一次生成的计划
  exec <需求>   - 直接生成并执行计划
  report        - 生成测试报告（基于最近结果）
  status        - 查看最近结果摘要
  help          - 显示此帮助信息
  exit          - 退出程序

示例：
  > list
  > run 首页测试
  > run all
  > plan 测试登录流程
  > exec 测试上传 PDF
  > report
        """
        self.console.print(Panel(help_text, title="帮助", border_style="green"))
    
    def list_scenarios(self):
        """列出所有测试场景"""
        scenarios = self.agent.get_available_scenarios()
        
        if not scenarios:
            self.console.print("[yellow]没有可用的测试场景[/yellow]")
            return
        
        table = Table(title="可用的测试场景")
        table.add_column("名称", style="cyan", no_wrap=True)
        table.add_column("描述", style="magenta")
        
        for scenario in scenarios:
            table.add_row(scenario["name"], scenario["description"])
        
        self.console.print(table)

    def show_plan(self, plan: Dict[str, Any]):
        """展示 Planner 生成的计划"""
        table = Table(title="测试计划 (Planner 输出)")
        table.add_column("步骤")
        table.add_column("动作")
        table.add_column("目标/值")
        table.add_column("预期")

        for step in plan.get("steps", []):
            target_value = step.get("target", "")
            if step.get("value"):
                target_value = f"{target_value}\n值: {step.get('value')}"
            table.add_row(
                f"Step {step.get('id')}",
                step.get("action", ""),
                target_value,
                step.get("expect", ""),
            )

        self.console.print(table)
        self.last_plan = plan
    
    def run_scenario(self, scenario_name: str):
        """运行测试场景"""
        if scenario_name.lower() == "all":
            self.console.print("[bold blue]开始运行所有测试场景...[/bold blue]")
            summary = self.agent.run_all_scenarios()
            self._display_summary(summary)
            return summary
        else:
            self.console.print(f"[bold blue]开始运行测试场景: {scenario_name}[/bold blue]")
            result = self.agent.run_scenario_by_name(scenario_name)
            
            if result:
                self._display_scenario_result(result)
                return {"scenarios": [result], "total": 1, "passed": 1 if result["status"] == "passed" else 0, "failed": 1 if result["status"] == "failed" else 0, "duration": result["duration"]}
            else:
                self.console.print(f"[red]未找到测试场景: {scenario_name}[/red]")
                return None
    
    def generate_report(self, summary: Optional[Dict[str, Any]] = None):
        """生成测试报告"""
        if summary is None:
            if not self.agent.results:
                self.console.print("[yellow]没有测试结果，请先运行测试[/yellow]")
                return
            
            summary = {
                "total": len(self.agent.results),
                "passed": sum(1 for r in self.agent.results if r["status"] == "passed"),
                "failed": sum(1 for r in self.agent.results if r["status"] == "failed"),
                "duration": sum(r["duration"] for r in self.agent.results),
                "scenarios": self.agent.results
            }
        
        self.console.print("[bold blue]正在生成测试报告...[/bold blue]")
        
        # 生成HTML报告
        html_path = self.report_generator.generate_html_report(summary)
        self.console.print(f"[green]✓ HTML报告已生成: {html_path}[/green]")
        
        # 生成文本报告
        txt_path = self.report_generator.generate_text_report(summary)
        self.console.print(f"[green]✓ 文本报告已生成: {txt_path}[/green]")
        
        # 询问是否打开报告
        if Confirm.ask("是否在浏览器中打开HTML报告？"):
            import webbrowser
            import os
            webbrowser.open(f"file://{os.path.abspath(html_path)}")
    
    def _display_summary(self, summary: Dict[str, Any]):
        """显示测试摘要"""
        self.console.print("\n[bold]测试摘要:[/bold]")
        self.console.print(f"  总测试数: [cyan]{summary['total']}[/cyan]")
        self.console.print(f"  通过: [green]{summary['passed']}[/green]")
        self.console.print(f"  失败: [red]{summary['failed']}[/red]")
        self.console.print(f"  执行时长: [yellow]{summary['duration']:.2f} 秒[/yellow]")
        
        # 显示每个场景的结果
        self.console.print("\n[bold]测试场景结果:[/bold]")
        for scenario in summary['scenarios']:
            status_color = "green" if scenario['status'] == "passed" else "red"
            status_symbol = "✓" if scenario['status'] == "passed" else "✗"
            self.console.print(f"  {status_symbol} [{status_color}]{scenario['name']}[/{status_color}] - {scenario['status']} ({scenario['duration']:.2f}s)")
            if scenario.get('error_message'):
                self.console.print(f"    错误: [red]{scenario['error_message']}[/red]")
    
    def _display_scenario_result(self, result: Dict[str, Any]):
        """显示单个场景的测试结果"""
        status_color = "green" if result['status'] == "passed" else "red"
        status_symbol = "✓" if result['status'] == "passed" else "✗"
        
        self.console.print(f"\n{status_symbol} [{status_color}]{result['name']}[/{status_color}] - {result['status']}")
        self.console.print(f"  描述: {result['description']}")
        self.console.print(f"  时长: {result['duration']:.2f} 秒")
        
        if result.get('error_message'):
            self.console.print(f"  错误: [red]{result['error_message']}[/red]")
        
        self.console.print("\n  测试步骤:")
        for i, step in enumerate(result['steps'], 1):
            step_status_color = "green" if step['status'] == "passed" else "red" if step['status'] == "failed" else "yellow"
            step_symbol = "✓" if step['status'] == "passed" else "✗" if step['status'] == "failed" else "○"
            self.console.print(f"    {step_symbol} [{step_status_color}]{i}. {step['name']}[/{step_status_color}] - {step['status']}")
            if step.get('message'):
                self.console.print(f"        {step['message']}")
    
    def run(self):
        """运行对话式界面"""
        self.print_welcome()
        
        last_summary = None
        
        while True:
            try:
                command = Prompt.ask("\n[bold cyan]测试智能体[/bold cyan]").strip()
                
                if not command:
                    continue
                
                if command.lower() == "exit" or command.lower() == "quit":
                    self.console.print("[yellow]再见！[/yellow]")
                    break
                
                elif command.lower() == "help":
                    self.print_help()
                
                elif command.lower() == "list":
                    self.list_scenarios()
                
                elif command.lower().startswith("run "):
                    scenario_name = command[4:].strip()
                    last_summary = self.run_scenario(scenario_name)
                
                elif command.lower().startswith("plan "):
                    instruction = command[5:].strip()
                    plan = self.agent.create_plan(instruction)
                    self.show_plan(plan)
                
                elif command.lower().startswith("exec"):
                    # 支持 exec <需求> 或直接 exec 使用最近计划
                    parts = command.split(" ", 1)
                    instruction = parts[1].strip() if len(parts) > 1 else None
                    self.console.print("[bold blue]执行计划...[/bold blue]")
                    result = self.agent.run_plan(instruction)
                    self.last_plan = result["plan"]
                    self.last_summary = result["summary"]
                    self._display_summary(result["summary"])
                
                elif command.lower() == "report":
                    # 优先使用最近的计划结果
                    summary_to_use = self.last_summary or last_summary
                    self.generate_report(summary_to_use)
                
                elif command.lower() == "status":
                    summary_to_use = self.last_summary or last_summary
                    if summary_to_use:
                        self._display_summary(summary_to_use)
                    elif self.agent.results:
                        from testAgent.reporter import Reporter

                        reporter = Reporter()
                        summary = reporter.build_summary(self.agent.results)
                        self._display_summary(summary)
                    else:
                        self.console.print("[yellow]还没有运行任何测试[/yellow]")
                
                else:
                    self.console.print(f"[red]未知命令: {command}[/red]")
                    self.console.print("[yellow]输入 'help' 查看可用命令[/yellow]")
            
            except KeyboardInterrupt:
                self.console.print("\n[yellow]程序已中断[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]发生错误: {str(e)}[/red]")

