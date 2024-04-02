import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.browser import Chrome_test
from src.tools import Tools
from datetime import datetime

today_test_count: int = 0

@pytest.fixture(scope="module")
def webdriver():
    chrome_test = Chrome_test()
    driver = chrome_test.browser()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def config():
    return Tools.check_and_load("./config.yaml")

def pytest_configure(config):
    global today_test_count
    today = datetime.now().strftime("%Y-%m-%d")
    # 统计今日测试报告数量
    today_test_count = sum(1 for item in os.listdir(config.rootdir) if item.startswith(f'reports/test_report_{today}'))

def pytest_html_report_title(report):
    global today_test_count
    today = datetime.now().strftime("%Y-%m-%d")
    report.title = f"Test Report:{today} - Test Time:{today_test_count + 1}"
    today_test_count += 1

def pytest_html_results_table_header(cells) -> None:
    cells.insert(2, '<th class="sortable">Date</th>')

def pytest_html_results_table_row(report, cells):
    cells.insert(2, '<td>{}</td>'.format(datetime.now()))
