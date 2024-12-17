@echo off
echo Installing...
start /wait python-3.10.0-full.exe

echo Python is installed successfully

cmd /k "pip install requests && pip install pillow && pip install reportlab"

echo Modules are installed successfully