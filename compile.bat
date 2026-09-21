@echo off
mkdir bin 2>nul
g++ -std=c++17 src\main.cpp src\models.cpp src\services.cpp src\utils.cpp -o bin\PayrollSystem.exe
if %ERRORLEVEL% EQU 0 (
    echo Compilation successful! Run bin\PayrollSystem.exe
) else (
    echo Compilation failed!
)
