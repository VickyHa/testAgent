# OpenCSG AgenticHub 自动化测试智能体

这是一个基于 Playwright 的自动化测试智能体，用于对 [OpenCSG AgenticHub](https://opencsg.com/agentichub) 网站进行自动化测试。支持通过对话式界面执行测试并生成详细的测试报告。

## 功能特性

- 🧭 **Planner（规划者）**：将自然语言需求转换为结构化测试计划（JSON）
- 🤖 **Actor（执行者）**：使用 Playwright 执行计划步骤，支持点击、输入、等待、上传、截图
- 📈 **Reporter（分析者）**：汇总执行结果，生成 HTML/文本报告，附带截图证据
- 💬 **对话式交互**：通过命令行对话控制测试流程
- 🧪 **预置场景**：保留示例场景（首页、导航），可继续扩展

## 安装步骤

### 1. 安装 Python

确保您的系统已安装 Python 3.8 或更高版本。

```bash
python --version
```

### 2. 安装依赖

在项目根目录下运行：

```bash
cd testAgent
pip install -r requirements.txt
```

### 3. 安装 Playwright 浏览器

安装 Playwright 所需的浏览器：

```bash
playwright install chromium
```

或者安装所有浏览器：

```bash
playwright install
```

## 使用方法

### 启动测试智能体

在项目根目录下运行：

```bash
python testAgent/main.py
```

或者：

```bash
cd testAgent
python main.py
```

### 可用命令（对话式）

| 命令 | 说明 | 示例 |
|------|------|------|
| `plan <需求>` | 生成结构化测试计划（Planner） | `plan 测试登录流程` |
| `exec <需求>` | 生成并执行计划（Planner + Actor + Reporter） | `exec 测试上传 PDF` |
| `exec` | 执行最近一次生成的计划 | `exec` |
| `report` | 基于最近结果生成报告 | `report` |
| `status` | 查看最近结果摘要 | `status` |
| `list` | 列出预置测试场景 | `list` |
| `run <场景名>` | 运行指定预置场景（旧模式） | `run 首页测试` |
| `run all` | 运行所有预置场景 | `run all` |
| `help` | 显示帮助 | `help` |
| `exit` | 退出程序 | `exit` |

### 使用示例

#### 示例 1: 查看所有测试场景

```
测试智能体> list
```

输出会显示所有可用的测试场景及其描述。

#### 示例 2: Planner + Actor 一键执行

```
测试智能体> exec 测试一下创建知识库并上传 PDF 是否报错
```

智能体会生成结构化计划并立即执行，完成后输出摘要。

#### 示例 3: 先规划后执行

```
测试智能体> plan 测试登录后能否看到 AgentHub 首页
测试智能体> exec
```

#### 示例 4: 生成测试报告

```
测试智能体> report
```

基于最近一次执行结果生成 HTML 与文本报告。

## 测试报告

测试报告会保存在 `testAgent/reports/` 目录下，包括：

- **HTML 报告** (`test_report_YYYYMMDD_HHMMSS.html`) - 美观的可视化报告
- **文本报告** (`test_report_YYYYMMDD_HHMMSS.txt`) - 纯文本格式报告

报告包含：
- 测试摘要（总数、通过、失败、执行时长）
- 每个测试场景的详细结果
- 每个测试步骤的执行情况
- 错误信息（如果有）
- 截图（如果有）

## 项目结构

```
testAgent/
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── test_agent.py          # 测试智能体核心类
├── chat_interface.py      # 对话式交互界面
├── planner.py             # Planner：从自然语言生成计划
├── actor.py               # Actor：执行计划步骤
├── reporter.py            # Reporter：汇总结果、生成报告摘要
├── report_generator.py    # 报告生成器
├── requirements.txt       # Python 依赖
├── scenarios/             # 测试场景目录
│   ├── __init__.py
│   ├── base_scenario.py  # 基础场景类
│   ├── homepage_scenario.py    # 首页测试场景
│   └── navigation_scenario.py  # 导航测试场景
├── reports/               # 测试报告目录（自动创建）
└── screenshots/           # 截图目录（自动创建）
```

## 添加自定义测试场景

### 1. 创建场景文件

在 `testAgent/scenarios/` 目录下创建新的场景文件，例如 `login_scenario.py`：

```python
from testAgent.scenarios.base_scenario import TestScenario
from playwright.sync_api import Page, BrowserContext

class LoginScenario(TestScenario):
    def __init__(self):
        super().__init__(
            name="登录测试",
            description="测试用户登录功能"
        )
        self.add_step("访问登录页", "导航到登录页面", "登录页面成功加载")
        self.add_step("输入用户名", "在用户名输入框中输入", "用户名输入成功")
        self.add_step("输入密码", "在密码输入框中输入", "密码输入成功")
        self.add_step("点击登录", "点击登录按钮", "登录成功")
    
    def execute(self, page: Page, context: BrowserContext) -> bool:
        # 实现测试逻辑
        try:
            # 步骤1: 访问登录页
            self.record_step_result(0, "running")
            page.goto("https://iam.opencsg.com/login")
            self.record_step_result(0, "passed", "登录页面加载成功")
            
            # 步骤2: 输入用户名
            self.record_step_result(1, "running")
            # 在这里添加实际的测试代码
            self.record_step_result(1, "passed", "用户名输入成功")
            
            # ... 其他步骤
            
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
```

### 2. 注册场景

在 `testAgent/scenarios/__init__.py` 中导入新场景：

```python
from testAgent.scenarios.login_scenario import LoginScenario

__all__ = [
    "HomepageScenario",
    "NavigationScenario",
    "LoginScenario",  # 添加新场景
]
```

### 3. 在界面中注册

在 `testAgent/chat_interface.py` 的 `_register_default_scenarios` 方法中添加：

```python
from testAgent.scenarios import HomepageScenario, NavigationScenario, LoginScenario

def _register_default_scenarios(self):
    self.agent.register_scenario(HomepageScenario())
    self.agent.register_scenario(NavigationScenario())
    self.agent.register_scenario(LoginScenario())  # 添加新场景
```

## 配置说明

可以在 `testAgent/config.py` 中修改配置：

- **BROWSER_CONFIG**: 浏览器配置（无头模式、视口大小等）
- **TEST_CONFIG**: 测试配置（截图、重试次数等）
- **LOGIN_CONFIG**: 登录配置（如果需要测试登录功能）

## 常见问题

### Q: 浏览器无法启动？

A: 确保已安装 Playwright 浏览器：
```bash
playwright install chromium
```

### Q: 测试失败但没有截图？

A: 检查 `testAgent/screenshots/` 目录权限，确保程序有写入权限。

### Q: 如何修改测试目标网站？

A: 在 `testAgent/config.py` 中修改 `TARGET_URL` 变量。

### Q: 如何以无头模式运行？

A: 在 `testAgent/config.py` 中将 `BROWSER_CONFIG["headless"]` 设置为 `True`。

## 技术栈

- **Python 3.8+** - 编程语言
- **Playwright** - 浏览器自动化框架
- **Rich** - 终端美化库
- **Jinja2** - 模板引擎（用于报告生成）

## 许可证

本项目基于 MIT 许可证开源。

## 贡献

欢迎提交 Issue 和 Pull Request！
