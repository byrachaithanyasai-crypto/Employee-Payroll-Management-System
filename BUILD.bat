@echo off
echo ====================================================
echo        BUILDING EMPLOYEE PAYROLL SYSTEM
echo ====================================================

set "CXX=g++"
where g++ >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    if exist "C:\msys64\ucrt64\bin\g++.exe" (
        set "CXX=C:\msys64\ucrt64\bin\g++.exe"
    ) else (
        echo [ERROR] g++ is not installed or not in the system PATH.
        echo Please install MinGW-w64 or MSYS2 and ensure g++ is available.
        pause
        exit /b 1
    )
)

:: Create bin directory
if not exist "bin" mkdir bin

:: Set PATH so g++.exe finds its DLLs
set "PATH=C:\msys64\ucrt64\bin;%PATH%"

:: Compile the project using C++17
echo Compiling source files...
%CXX% -std=c++17 src\main.cpp src\models.cpp src\services.cpp src\utils.cpp src\api.cpp -o bin\PayrollSystem.exe -lws2_32 -lbcrypt

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Compilation completed successfully!
    echo Executable is located at: bin\PayrollSystem.exe
    echo You can now run the project using RUN.bat
) else (
    echo [ERROR] Compilation failed. Please check the errors above.
)
pause
