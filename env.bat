@echo off

REM 检测是否安装 pip 包管理工具
pip --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Error: pip is not installed. Running check.py..."
    python .\check.py
    IF %ERRORLEVEL% NEQ 0 (
        echo "Error: check.py failed to install pip."
        exit /b 1
    )
) ELSE (
    echo "pip is installed."
)

REM 检测是否安装 selenium 库
pip show selenium > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Installing selenium package..."
    pip install selenium
) ELSE (
    echo "selenium is installed"
)

REM 检测是否安装 pytest-cov 库
pip show pytest-cov > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Installing pytest-cov package..."
    pip install pytest-cov
) ELSE (
    echo "pytest-cov is installed"
)

REM 检测是否安装 pytest 库
pip show pytest > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Installing pytest package..."
    pip install pytest
) ELSE (
    echo "pytest is installed"
)

REM 检测并安装 pyyaml 库
pip show pyyaml > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Installing pyyaml package..."
    pip install pyyaml
) ELSE (
    echo "pyyaml is installed"
)

REM 检测并安装pytest-html
pip show pytest-html > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo "Installing pytest-html package..."
    pip install pytest-html
) ELSE (
    echo "pytest-html is installed"
)

echo "All required packages are installed."
exit /b 0