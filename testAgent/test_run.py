"""
简单测试脚本 - 验证核心功能
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    print("Testing imports...")
    from testAgent.planner import Planner
    print("[OK] Planner imported")
    
    from testAgent.actor import Actor
    print("[OK] Actor imported")
    
    from testAgent.reporter import Reporter
    print("[OK] Reporter imported")
    
    from testAgent.test_agent import TestAgent
    print("[OK] TestAgent imported")
    
    from testAgent.config import TARGET_URL
    print(f"[OK] Config loaded - Target URL: {TARGET_URL}")
    
    print("\n" + "="*50)
    print("All core modules imported successfully!")
    print("="*50)
    
    # 测试Planner
    print("\nTesting Planner...")
    planner = Planner()
    test_plan = planner.create_plan("测试首页加载")
    print(f"[OK] Plan created")
    print(f"  Instruction: {test_plan.instruction}")
    print(f"  Steps: {len(test_plan.steps)}")
    if test_plan.steps:
        print(f"  First step: {test_plan.steps[0].action}")
    
    print("\n" + "="*50)
    print("SUCCESS: TestAgent is ready to use!")
    print("="*50)
    print("\nTo run the full interface:")
    print("  python testAgent\\main.py")
    print("\nOr use the batch file:")
    print("  testAgent\\start.bat")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
