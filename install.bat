@echo off
echo ========================================
echo    WOW BOT INSTALLER
echo ========================================
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ first
    echo Download at: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing pyautogui...
pip install pyautogui==0.9.54

echo Installing keyboard...
pip install keyboard==0.13.5

echo Installing pywin32...
pip install pywin32==306

echo.
echo ========================================
echo    INSTALLATION COMPLETED!
echo ========================================
echo.
echo To run the bot, use:
echo python adv_bot.py
echo.
echo Remember to use at your own risk!
echo.
pause 