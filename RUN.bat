@echo off
echo ====================================================
echo        STARTING EMPLOYEE PAYROLL SYSTEM
echo ====================================================

if exist "bin\PayrollSystem.exe" (
    set "PATH=C:\msys64\ucrt64\bin;%PATH%"
    bin\PayrollSystem.exe
) else (
    echo [ERROR] Executable not found!
    echo Please run BUILD.bat first to compile the project.
    pause
)
