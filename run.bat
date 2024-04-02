@echo off

REM 运行env.bat文件
call env.bat
IF %ERRORLEVEL% NEQ 0 (
    echo "Error: env.bat failed to run."
    exit \b 1
)

REM 运行run.py文件
echo "Running run.py..."
python .\run.py