# OpenCSG AgenticHub 自动化测试智能体

这是一个基于 Playwright 的自动化测试智能体，用于对 [OpenCSG AgenticHub](https://opencsg.com/agentichub) 网站进行自动化测试。支持通过对话式界面执行测试并生成详细的测试报告。

## 🚀 快速开始

### Windows 用户

**最简单的方式：双击运行 `testAgent/start.bat`**

或者手动执行：

```bash
cd testAgent
pip install -r requirements.txt
playwright install chromium
cd ..
python testAgent\main.py
```

### Linux/Mac 用户

```bash
chmod +x testAgent/start.sh
./testAgent/start.sh
```

或者手动执行：

```bash
cd testAgent
pip install -r requirements.txt
playwright install chromium
cd ..
python testAgent/main.py
```

## 📖 详细文档

- **完整使用指南**：查看 `testAgent/使用指南.md`
- **技术文档**：查看 `testAgent/README.md`

## 🧠 智能体架构

本测试智能体采用三层架构设计：

- **Planner (规划者)**：理解自然语言需求，生成结构化测试计划
- **Actor (执行者)**：使用 Playwright 执行测试步骤，自动操作浏览器
- **Reporter (分析者)**：对比执行结果与预期结果，生成详细报告

## 💡 快速示例

启动程序后，您可以直接用自然语言描述测试需求：

```
测试智能体> exec 测试首页加载和基本功能
测试智能体> plan 测试登录功能，验证用户名密码输入
测试智能体> exec 测试创建知识库并上传PDF文件
```

更多使用方法请查看 `testAgent/使用指南.md`
