1. 使用 conftest.py 文件来管理公共配置
定义全局 fixture： 在 conftest.py 中定义一些常用的 fixture，如基础 URL、认证信息等。

# conftest.py
import requests

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="http://localhost:8000")

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture
def session(base_url):
    session = requests.Session()
    session.base_url = base_url
    return session

2. 模块化测试用例
将测试用例拆分成多个模块： 将不同的 API 测试用例拆分到不同的文件中，每个文件负责一组相关的 API 测试。
tests/
├── __init__.py
├── conftest.py
├── test_auth.py
├── test_users.py
├── test_products.py

3. 使用 pytest.mark.parametrize 来处理数据驱动测试
参数化测试用例： 对于重复性的测试用例，可以使用 pytest.mark.parametrize 来批量执行。

# test_auth.py
import pytest
from conftest import session

@pytest.mark.parametrize("username, password, expected_status", [
    ("user1", "pass1", 200),
    ("user2", "pass2", 401),
    ("user3", "pass3", 401)
])
def test_login(session, username, password, expected_status):
    response = session.post("/login", json={"username": username, "password": password})
    assert response.status_code == expected_status

4. 使用 fixture 来管理前置条件
定义 setup 和 teardown fixture： 用于处理测试前后的初始化和清理工作。
# conftest.py
@pytest.fixture
def setup_test(session):
    # 初始化数据库或其他资源
    yield
    # 清理资源

5. 使用 pytest 插件来增强功能
报告插件： 使用 pytest-html 或 pytest-xdist 等插件来生成详细的测试报告或并行执行测试。
pip install pytest-html pytest-xdist
命令行选项： 可以通过 pytest_addoption 添加自定义命令行选项。
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="http://localhost:8000")

6. 组织测试数据
将测试数据放在单独的文件中： 将测试数据存储在 YAML 或 JSON 文件中，便于维护和修改。
# data/auth_data.yaml
- username: user1
  password: pass1
  expected_status: 200
- username: user2
  password: pass2
  expected_status: 401
读取测试数据： 在测试用例中读取这些数据文件。
import pytest
import yaml

@pytest.fixture
def auth_data():
    with open("data/auth_data.yaml", "r") as f:
        return yaml.safe_load(f)

@pytest.mark.parametrize("test_case", auth_data())
def test_login(session, test_case):
    response = session.post("/login", json=test_case)
    assert response.status_code == test_case["expected_status"]

创建一个日志目录结构：

遍历 /logs 目录，检查是否存在当天的日期目录。
如果不存在，则创建当天的日期目录。
在当天的日期目录下生成以时分秒命名的日志文件。
捕获异常并记录日志：

使用 pytest 的钩子函数来捕获异常。
将异常信息记录到相应的日志文件中。
下面是一个完整的示例代码，包括 conftest.py 和一个简单的日志处理脚本：

1. 创建 conftest.py 文件
# conftest.py
import os
import datetime
import logging
import pytest

# 日志目录
LOG_DIR = 'logs'

def create_log_directory():
    today = datetime.datetime.now().strftime('%Y%m%d')
    log_path = os.path.join(LOG_DIR, today)
    
    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    return log_path

def create_log_file(log_path):
    now = datetime.datetime.now().strftime('%H-%M-%S')
    log_file = os.path.join(log_path, f'{now}.log')
    return log_file

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 执行测试用例
    outcome = yield
    report = outcome.get_result()
    
    # 捕获失败的测试用例
    if report.when == 'call' and report.failed:
        log_path = create_log_directory()
        log_file = create_log_file(log_path)
        
        # 记录异常信息到日志文件
        with open(log_file, 'w') as f:
            f.write(f"Test Name: {item.name}\n")
            f.write(f"Test Function: {item.function.__name__}\n")
            f.write(f"Error Message: {report.longreprtext}\n")
            f.write(f"Traceback: {report.longrepr.reprcrash.message}\n")
            f.write(f"Traceback Details: {report.longrepr.reprtraceback}\n")

# 初始化日志目录
create_log_directory()

pytest_runtest_makereport 钩子函数
pytest_runtest_makereport 是 pytest 提供的一个钩子函数，它在测试用例执行后被调用，用于生成测试报告。这个钩子函数的主要目的是获取测试用例的执行结果，并根据结果做一些额外的操作，比如记录日志。

钩子函数详解
1. @pytest.hookimpl(tryfirst=True, hookwrapper=True)
tryfirst=True：确保这个钩子函数优先执行。
hookwrapper=True：表示这是一个包装器钩子，它会先执行自己的逻辑，然后再执行其他注册的钩子函数。
2. def pytest_runtest_makereport(item, call):
item：表示当前正在执行的测试项。
call：表示当前测试项的执行过程。
3. outcome = yield
yield：这是 pytest 钩子函数的一个特殊用法，它会暂停当前函数的执行，等待其他钩子函数执行完毕后再继续。这里 yield 返回了一个 outcome 对象，包含了测试用例的执行结果。
4. report = outcome.get_result()
get_result()：从 outcome 对象中获取测试用例的执行结果。
5. if report.when == 'call' and report.failed:
report.when：表示测试用例的哪个阶段。通常有三个阶段：setup、call 和 teardown。
setup：测试用例的前置条件。
call：测试用例的实际执行。
teardown：测试用例的后置条件。
report.failed：表示测试用例是否失败。
6. log_path = create_log_directory()
调用 create_log_directory 函数创建日志目录。
7. log_file = create_log_file(log_path)
调用 create_log_file 函数生成日志文件名。
8. with open(log_file, 'w') as f:
打开日志文件进行写入。
9. 写入日志信息
f.write(f"Test Name: {item.name}\n")：写入测试用例的名字。
f.write(f"Test Function: {item.function.__name__}\n")：写入测试函数的名字。
f.write(f"Error Message: {report.longreprtext}\n")：写入错误消息。
f.write(f"Traceback: {report.longrepr.reprcrash.message}\n")：写入异常消息。
f.write(f"Traceback Details: {report.longrepr.reprtraceback}\n")：写入详细的堆栈跟踪信息。
总结
通过这个钩子函数，我们可以在测试用例失败时捕获异常信息，并将其记录到指定的日志文件中。具体步骤如下：

捕获测试结果：通过 yield 获取测试结果。
检查测试失败：判断测试用例是否在 call 阶段失败。
创建日志目录：根据当前日期创建日志目录。
生成日志文件名：根据当前时间生成日志文件名。
记录日志信息：将测试用例的详细信息写入日志文件。
这样，每次运行 pytest 时，失败的测试用例的相关信息会被记录到 /logs 目录下的相应文件中。

在 pytest 中，可以通过以下几种方式来管理 session 级别的数据，例如登录接口的 token 值。这些方法可以帮助你在整个测试会话期间共享数据，从而避免重复登录或其他不必要的操作。

1. 使用 fixtures 和 scope='session'
你可以定义一个 fixture，并将其作用域设置为 session，这样在整个测试会话期间只会执行一次该 fixture 的初始化逻辑。
import pytest
import requests

# 定义一个 session 级别的 fixture 来获取 token
@pytest.fixture(scope='session')
def login_token():
    # 模拟登录接口请求
    response = requests.post('https://example.com/login', json={'username': 'user1', 'password': 'password1'})
    assert response.status_code == 200
    token = response.json()['token']
    return token

# 使用 fixture 的测试函数
def test_api_endpoint(login_token):
    headers = {'Authorization': f'Bearer {login_token}'}
    response = requests.get('https://example.com/api/data', headers=headers)
    assert response.status_code == 200
    assert 'data' in response.json()

# 另一个使用相同 token 的测试函数
def test_another_api_endpoint(login_token):
    headers = {'Authorization': f'Bearer {login_token}'}
    response = requests.get('https://example.com/api/more-data', headers=headers)
    assert response.status_code == 200
    assert 'more_data' in response.json()

2. 使用 session 级别的 fixture 并传递给其他 fixtures
你还可以将 session 级别的 fixture 作为其他 fixtures 的依赖项，这样可以在多个测试函数中共享同一个 token。
import pytest
import requests

# 定义一个 session 级别的 fixture 来获取 token
@pytest.fixture(scope='session')
def login_token():
    # 模拟登录接口请求
    response = requests.post('https://example.com/login', json={'username': 'user1', 'password': 'password1'})
    assert response.status_code == 200
    token = response.json()['token']
    return token

# 定义一个使用 token 的 fixture
@pytest.fixture
def authenticated_client(login_token):
    headers = {'Authorization': f'Bearer {login_token}'}
    return requests.Session(), headers

# 使用 fixture 的测试函数
def test_api_endpoint(authenticated_client):
    client, headers = authenticated_client
    response = client.get('https://example.com/api/data', headers=headers)
    assert response.status_code == 200
    assert 'data' in response.json()

# 另一个使用相同 token 的测试函数
def test_another_api_endpoint(authenticated_client):
    client, headers = authenticated_client
    response = client.get('https://example.com/api/more-data', headers=headers)
    assert response.status_code == 200
    assert 'more_data' in response.json()

3. 使用 session 级别的 fixture 并在测试类中使用
如果你有多个测试类需要共享同一个 token，也可以在测试类中使用 session 级别的 fixture。
import pytest
import requests

# 定义一个 session 级别的 fixture 来获取 token
@pytest.fixture(scope='session')
def login_token():
    # 模拟登录接口请求
    response = requests.post('https://example.com/login', json={'username': 'user1', 'password': 'password1'})
    assert response.status_code == 200
    token = response.json()['token']
    return token

class TestAPI:
    @pytest.fixture(autouse=True)
    def setup(self, login_token):
        self.headers = {'Authorization': f'Bearer {login_token}'}

    def test_api_endpoint(self):
        response = requests.get('https://example.com/api/data', headers=self.headers)
        assert response.status_code == 200
        assert 'data' in response.json()

    def test_another_api_endpoint(self):
        response = requests.get('https://example.com/api/more-data', headers=self.headers)
        assert response.status_code == 200
        assert 'more_data' in response.json()

步骤概述
创建 YAML 文件：定义接口地址和测试用例数据。
读取 YAML 文件：使用 Python 的 PyYAML 库读取 YAML 文件中的数据。
使用 parametrize 装饰器：将读取到的测试数据传递给测试用例。
示例代码
1. 创建 YAML 文件
首先，创建一个名为 test_data.yaml 的文件，用于存储接口地址和测试用例数据：
api:
  base_url: https://example.com

auth_data:
  - username: user1
    password: password1
    expected: true
  - username: user2
    password: wrong_password
    expected: false
  - username: nonexistent_user
    password: any_password
    expected: false

2. 读取 YAML 文件并定义测试用例
接下来，在 Python 测试脚本中读取 YAML 文件，并使用 parametrize 装饰器来定义测试用例。
import pytest
import yaml
import requests

# 读取 YAML 文件
def load_test_data(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['api']['base_url'], data['auth_data']

# 读取接口地址和测试数据
base_url, auth_data = load_test_data('test_data.yaml')

# 使用 parametrize 装饰器来定义测试用例
@pytest.mark.parametrize("username, password, expected", auth_data)
def test_authentication(base_url, username, password, expected):
    # 构造完整的 URL
    url = f"{base_url}/login"
    
    # 模拟登录接口请求
    response = requests.post(url, json={'username': username, 'password': password})
    
    # 检查响应状态码
    assert response.status_code == 200
    
    # 获取实际结果
    actual_result = response.json().get('authenticated', False)
    
    # 断言实际结果与预期结果一致
    assert actual_result == expected
解释
读取 YAML 文件：

使用 yaml.safe_load 方法从 YAML 文件中加载数据。
load_test_data 函数返回两个值：base_url 和 auth_data 列表。
使用 parametrize 装饰器：

@pytest.mark.parametrize 装饰器接受三个参数：username, password, expected，并将它们分别传递给 test_authentication 函数。
每组测试数据都会运行一次 test_authentication 函数。
测试用例：

test_authentication 函数构造完整的 URL，并模拟登录接口请求。
检查响应状态码和实际结果是否符合预期。
import pytest
import yaml
import requests

# 读取 YAML 文件
def load_test_data(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['api']['base_url'], data['auth_data']

# 读取接口地址和测试数据
base_url, auth_data = load_test_data('test_data.yaml')

# 使用 parametrize 装饰器来定义测试用例
@pytest.mark.parametrize("username, password, expected", auth_data)
def test_authentication(base_url, username, password, expected):
    # 构造完整的 URL
    url = f"{base_url}/login"
    
    # 模拟登录接口请求
    response = requests.post(url, json={'username': username, 'password': password})
    
    # 检查响应状态码
    assert response.status_code == 200
    
    # 获取实际结果
    actual_result = response.json().get('authenticated', False)
    
    # 断言实际结果与预期结果一致
    assert actual_result == expected

2. 环境配置文件
如果你希望持久化地设置环境变量，可以在项目的根目录下创建一个 .env 文件，并使用第三方库如 python-dotenv 来读取这些环境变量。
echo "BASE_URL=https://example.com" > .env

pip install python-dotenv

from dotenv import load_dotenv
import os
import pytest
import yaml
import requests

# 加载环境变量
load_dotenv()

# 读取服务器地址
base_url = os.getenv('BASE_URL', 'http://localhost:8000')

# 读取 YAML 文件
def load_test_data(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['auth_data']

# 读取测试数据
auth_data = load_test_data('test_data.yaml')

# 使用 parametrize 装饰器来定义测试用例
@pytest.mark.parametrize("path, username, password, expected", auth_data)
def test_authentication(base_url, path, username, password, expected):
    # 构造完整的 URL
    url = f"{base_url}{path}"
    
    # 模拟登录接口请求
    response = requests.post(url, json={'username': username, 'password': password})
    
    # 检查响应状态码
    assert response.status_code == 200
    
    # 获取实际结果
    actual_result = response.json().get('authenticated', False)
    
    # 断言实际结果与预期结果一致
    assert actual_result == expected
