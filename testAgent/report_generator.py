"""
测试报告生成器
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from testAgent.config import REPORTS_DIR


class ReportGenerator:
    """测试报告生成器"""
    
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_html_report(self, summary: Dict[str, Any], output_file: Optional[str] = None) -> str:
        """生成HTML格式的测试报告"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_report_{timestamp}.html"
        
        output_path = self.reports_dir / output_file
        
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - {{ timestamp }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .summary-card.passed {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
        .summary-card.failed {
            background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        }
        .summary-card.total {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        }
        .summary-card h3 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .summary-card p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .scenario {
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        .scenario-header {
            background: #f8f9fa;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #ddd;
        }
        .scenario-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
        }
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        .status-badge.passed {
            background: #d4edda;
            color: #155724;
        }
        .status-badge.failed {
            background: #f8d7da;
            color: #721c24;
        }
        .status-badge.running {
            background: #fff3cd;
            color: #856404;
        }
        .scenario-body {
            padding: 20px;
        }
        .scenario-description {
            color: #666;
            margin-bottom: 20px;
            font-style: italic;
        }
        .steps {
            margin-top: 20px;
        }
        .step {
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #ddd;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .step.passed {
            border-left-color: #28a745;
        }
        .step.failed {
            border-left-color: #dc3545;
        }
        .step.running {
            border-left-color: #ffc107;
        }
        .step-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        .step-name {
            font-weight: bold;
            color: #2c3e50;
        }
        .step-details {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
            border-left: 4px solid #dc3545;
        }
        .screenshots {
            margin-top: 15px;
        }
        .screenshot {
            margin-top: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
        }
        .screenshot img {
            width: 100%;
            height: auto;
            display: block;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 自动化测试报告</h1>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>{{ summary.total }}</h3>
                <p>总测试数</p>
            </div>
            <div class="summary-card passed">
                <h3>{{ summary.passed }}</h3>
                <p>通过</p>
            </div>
            <div class="summary-card failed">
                <h3>{{ summary.failed }}</h3>
                <p>失败</p>
            </div>
            <div class="summary-card">
                <h3>{{ "%.2f"|format(summary.duration) }}s</h3>
                <p>执行时长</p>
            </div>
        </div>
        
        {% for scenario in summary.scenarios %}
        <div class="scenario">
            <div class="scenario-header">
                <div>
                    <div class="scenario-title">{{ scenario.name }}</div>
                    <div class="scenario-description">{{ scenario.description }}</div>
                </div>
                <span class="status-badge {{ scenario.status }}">{{ scenario.status }}</span>
            </div>
            <div class="scenario-body">
                <div class="steps">
                    {% for step in scenario.steps %}
                    <div class="step {{ step.status }}">
                        <div class="step-header">
                            <span class="step-name">{{ step.name }}</span>
                            <span class="status-badge {{ step.status }}">{{ step.status }}</span>
                        </div>
                        <div class="step-details">
                            <strong>操作:</strong> {{ step.action }}<br>
                            {% if step.expected %}
                            <strong>预期:</strong> {{ step.expected }}<br>
                            {% endif %}
                            {% if step.message %}
                            <strong>结果:</strong> {{ step.message }}<br>
                            {% endif %}
                            {% if step.timestamp %}
                            <strong>时间:</strong> {{ step.timestamp }}<br>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                {% if scenario.error_message %}
                <div class="error-message">
                    <strong>错误信息:</strong> {{ scenario.error_message }}
                </div>
                {% endif %}
                
                {% if scenario.screenshots %}
                <div class="screenshots">
                    <h4>截图:</h4>
                    {% for screenshot in scenario.screenshots %}
                    <div class="screenshot">
                        <img src="{{ screenshot }}" alt="Screenshot">
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
        
        <div class="footer">
            <p>报告生成时间: {{ timestamp }}</p>
            <p>测试目标: https://opencsg.com/agentichub</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            summary=summary,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        output_path.write_text(html_content, encoding="utf-8")
        return str(output_path)
    
    def generate_text_report(self, summary: Dict[str, Any], output_file: Optional[str] = None) -> str:
        """生成文本格式的测试报告"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_report_{timestamp}.txt"
        
        output_path = self.reports_dir / output_file
        
        lines = []
        lines.append("=" * 80)
        lines.append("自动化测试报告")
        lines.append("=" * 80)
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"测试目标: https://opencsg.com/agentichub")
        lines.append("")
        lines.append("测试摘要:")
        lines.append(f"  总测试数: {summary['total']}")
        lines.append(f"  通过: {summary['passed']}")
        lines.append(f"  失败: {summary['failed']}")
        lines.append(f"  执行时长: {summary['duration']:.2f} 秒")
        lines.append("")
        lines.append("=" * 80)
        lines.append("详细结果:")
        lines.append("=" * 80)
        
        for scenario in summary['scenarios']:
            lines.append("")
            lines.append(f"场景: {scenario['name']}")
            lines.append(f"描述: {scenario['description']}")
            lines.append(f"状态: {scenario['status']}")
            lines.append(f"时长: {scenario['duration']:.2f} 秒")
            
            if scenario['error_message']:
                lines.append(f"错误: {scenario['error_message']}")
            
            lines.append("步骤:")
            for i, step in enumerate(scenario['steps'], 1):
                lines.append(f"  {i}. {step['name']} - {step['status']}")
                lines.append(f"     操作: {step['action']}")
                if step.get('message'):
                    lines.append(f"     结果: {step['message']}")
            
            if scenario['screenshots']:
                lines.append("截图:")
                for screenshot in scenario['screenshots']:
                    lines.append(f"  - {screenshot}")
            
            lines.append("-" * 80)
        
        content = "\n".join(lines)
        output_path.write_text(content, encoding="utf-8")
        return str(output_path)

