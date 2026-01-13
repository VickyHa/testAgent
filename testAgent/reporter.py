"""
Reporter - 分析者，汇总执行结果并生成报告
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from testAgent.report_generator import ReportGenerator


class Reporter:
    """
    Reporter（分析者）
    - 对比预期与实际
    - 生成报告摘要
    """

    def __init__(self) -> None:
        self.generator = ReportGenerator()

    def build_scenario_result(
        self,
        plan: Dict[str, Any],
        step_results: List[Dict[str, Any]],
        start_time: datetime,
        end_time: datetime,
    ) -> Dict[str, Any]:
        status = "passed"
        error_message: Optional[str] = None
        for step in step_results:
            if step["status"] == "failed":
                status = "failed"
                error_message = step.get("message")
                break

        scenario = {
            "name": f"计划执行: {plan.get('instruction', '')}",
            "description": "Planner 生成的结构化计划，由 Actor 执行",
            "status": status,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration": (end_time - start_time).total_seconds(),
            "steps": [
                {
                    "name": step.get("name") or f"Step {step.get('id')}",
                    "action": step.get("action"),
                    "expected": step.get("expected"),
                    "status": step.get("status"),
                    "message": step.get("message"),
                    "timestamp": step.get("timestamp"),
                    "screenshot": step.get("screenshot"),
                }
                for step in step_results
            ],
            "error_message": error_message,
            "screenshots": [s for s in (step.get("screenshot") for step in step_results) if s],
        }
        return scenario

    def build_summary(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        passed = sum(1 for s in scenarios if s["status"] == "passed")
        failed = sum(1 for s in scenarios if s["status"] == "failed")
        duration = sum(s.get("duration", 0) for s in scenarios)
        return {
            "total": len(scenarios),
            "passed": passed,
            "failed": failed,
            "duration": duration,
            "scenarios": scenarios,
        }

    def generate_reports(self, summary: Dict[str, Any]) -> Dict[str, str]:
        html_path = self.generator.generate_html_report(summary)
        txt_path = self.generator.generate_text_report(summary)
        return {"html": html_path, "txt": txt_path}
