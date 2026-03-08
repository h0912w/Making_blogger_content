@echo off
title SEO Blog AI Optimizer

cd /d "%~dp0"

echo ========================================
echo SEO Blog AI Optimizer
echo ========================================
echo.

python run.py

if %errorlevel% neq 0 (
    echo.
    echo Error occurred. Press any key to exit.
)
pause
