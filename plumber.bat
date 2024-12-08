@echo off
set SCRIPT_DIR=%~dp0

if "%1"=="" (
    echo "Usage: plumber [new|build] [project_name]"
    exit /b 1
)

python "%SCRIPT_DIR%plumber.py" %*
