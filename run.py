import pytest
import os
from datetime import datetime

if __name__ == "__main__":
    project_root: str = os.path.dirname(os.path.abspath(__file__))
    test_dir: str = os.path.join(project_root, "tests")
    report_dir: str = os.path.join(project_root, "reports")
    os.makedirs(report_dir, exist_ok=True)

    # 计算今日测试报告数量
    today: str = datetime.now().strftime("%Y-%m-%d")
    today_test_count: int = sum(1 for item in os.listdir(report_dir) if item.startswith(today))

    # 生成年-月-日-时-分-秒-今日测试次数.html文件名
    report_filename: str = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')} - TestTime{today_test_count + 1}.html"
    report_path: str = os.path.join(report_dir, report_filename)

    pytest.main(["-v", "-s", f"--html={report_path}",f"--cov={test_dir}", "--cov-report=html", test_dir])