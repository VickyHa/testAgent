"""
Planner - 从自然语言需求生成结构化测试计划
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
from testAgent.config import TARGET_URL


@dataclass
class PlanStep:
    """单个测试步骤"""
    id: int
    action: str
    target: str = ""
    value: str = ""
    expect: str = ""
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "action": self.action,
            "target": self.target,
            "value": self.value,
            "expect": self.expect,
            "note": self.note,
        }


@dataclass
class Plan:
    """完整的测试计划"""
    instruction: str
    steps: List[PlanStep] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instruction": self.instruction,
            "created_at": self.created_at,
            "steps": [s.to_dict() for s in self.steps],
        }


class Planner:
    """
    Planner（规划者）
    - 接收自然语言指令
    - 输出结构化测试计划（JSON）
    """

    def __init__(self) -> None:
        self.default_steps = [
            PlanStep(
                id=1,
                action="goto",
                target=TARGET_URL,
                expect="页面加载成功，核心区域可见",
                note="打开 AgentHub 首页",
            ),
            PlanStep(
                id=2,
                action="wait_for_selector",
                target="main, [role='main'], .main-content, #main",
                expect="主内容区域出现",
                note="等待主内容渲染完成",
            ),
            PlanStep(
                id=3,
                action="screenshot",
                target="homepage_loaded",
                expect="保存首页截图",
                note="用于报告展示",
            ),
        ]

    def create_plan(self, instruction: str) -> Plan:
        """
        根据自然语言生成计划。
        为保证可运行性，此处使用关键词映射生成确定性计划，可根据需要接入 LLM。
        """
        normalized = instruction.lower()
        steps: List[PlanStep] = []

        # 登录相关
        if "登录" in instruction or "login" in normalized:
            steps.extend(
                [
                    PlanStep(
                        id=1,
                        action="goto",
                        target="https://iam.opencsg.com/login",
                        expect="登录页加载成功",
                        note="打开统一认证登录页",
                    ),
                    PlanStep(
                        id=2,
                        action="fill",
                        target="input[name='username'], #username, input[type='email']",
                        value="{{TEST_USERNAME}}",
                        expect="用户名输入成功",
                        note="使用环境变量 TEST_USERNAME",
                    ),
                    PlanStep(
                        id=3,
                        action="fill",
                        target="input[name='password'], #password, input[type='password']",
                        value="{{TEST_PASSWORD}}",
                        expect="密码输入成功",
                        note="使用环境变量 TEST_PASSWORD",
                    ),
                    PlanStep(
                        id=4,
                        action="click",
                        target="button[type='submit'], button:has-text('登录'), .login-btn",
                        expect="提交登录表单",
                        note="点击登录按钮",
                    ),
                    PlanStep(
                        id=5,
                        action="wait_for_text",
                        target="AgentHub",
                        expect="登录后看到 AgentHub 关键字",
                        note="验证跳转到 AgentHub",
                    ),
                    PlanStep(
                        id=6,
                        action="screenshot",
                        target="after_login",
                        expect="登录结果截图",
                        note="报告中展示",
                    ),
                ]
            )

        # 知识库/上传 PDF 场景
        elif "知识库" in instruction or "pdf" in normalized or "上传" in instruction:
            steps.extend(
                [
                    PlanStep(
                        id=1,
                        action="goto",
                        target=TARGET_URL,
                        expect="AgentHub 首页加载成功",
                        note="进入 AgentHub",
                    ),
                    PlanStep(
                        id=2,
                        action="click",
                        target="text=创建知识库, button:has-text('创建'), .create-btn",
                        expect="打开创建知识库弹窗或页面",
                        note="入口按钮文案可能因版本而异",
                    ),
                    PlanStep(
                        id=3,
                        action="fill",
                        target="input[name='name'], input[placeholder*='名称'], input[placeholder*='Name']",
                        value="AutoKB Demo",
                        expect="输入知识库名称",
                        note="示例名称，可调整",
                    ),
                    PlanStep(
                        id=4,
                        action="upload",
                        target="input[type='file']",
                        value="sample.pdf",
                        expect="PDF 上传成功或显示进度完成",
                        note="需要在项目根目录准备 sample.pdf",
                    ),
                    PlanStep(
                        id=5,
                        action="click",
                        target="button:has-text('保存'), button:has-text('创建'), .submit-btn",
                        expect="提交创建知识库",
                        note="提交后等待状态变化",
                    ),
                    PlanStep(
                        id=6,
                        action="wait_for_text",
                        target="AutoKB Demo",
                        expect="列表中出现新建的知识库",
                        note="验证创建成功",
                    ),
                    PlanStep(
                        id=7,
                        action="screenshot",
                        target="kb_created",
                        expect="保存创建结果截图",
                        note="报告展示",
                    ),
                ]
            )

        # 默认回退计划：访问首页并检查主内容
        else:
            steps.extend(self.default_steps)

        return Plan(instruction=instruction, steps=steps)
