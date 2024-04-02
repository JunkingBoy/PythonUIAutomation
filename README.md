# PythonUIAutomation

### Python自动化测试的整体框架

**通过Pytest结合Selenium库实现UI自动化并且生成测试报告和测试代码质量报告**

#### 环境准备

- Python解释器
- 程序入口文件 -> `run.bat`文件.这是一个入口文件

##### 文件说明

- `run.bat`文件
    - 调用`env.bat`文件进行环境安装
    - 使用`pip`进行项目所需要的包的下载 -> `check.py`是一个`pip`的检测,如果没有则进行下载

##### 目录结构
---program
  --> src -> 存放浏览器初始化类、工具类代码
  --> tests -> 测试用例代码存放处
      --> conftest.py文件 -> pytest需要的文件
  --> reports -> 测试报告生成存放处
**由于运行后会进行代码质量检测.会创建一个`htmlcov`的目录存放`tests`目录下的代码质量检测报告
