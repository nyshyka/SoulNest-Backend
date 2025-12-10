@echo off
echo ================================================
echo SoulNest Database Setup
echo ================================================
echo.

REM Try to find MySQL in common locations
set MYSQL_PATH=
if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" (
    set MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
) else if exist "C:\Program Files\MySQL\MySQL Server 8.1\bin\mysql.exe" (
    set MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.1\bin\mysql.exe
) else if exist "C:\Program Files\MySQL\MySQL Server 8.2\bin\mysql.exe" (
    set MYSQL_PATH=C:\Program Files\MySQL\MySQL Server 8.2\bin\mysql.exe
) else if exist "C:\xampp\mysql\bin\mysql.exe" (
    set MYSQL_PATH=C:\xampp\mysql\bin\mysql.exe
) else (
    echo MySQL not found in common locations.
    echo.
    echo Please provide the full path to mysql.exe:
    echo (e.g., C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe)
    set /p MYSQL_PATH="MySQL path: "
)

if "%MYSQL_PATH%"=="" (
    echo Error: MySQL path not specified
    pause
    exit /b 1
)

echo.
echo Using MySQL at: %MYSQL_PATH%
echo.
echo This will create the database and seed it with initial data.
echo You will be prompted for your MySQL root password.
echo.
pause

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

echo.
echo Running seed script...
"%MYSQL_PATH%" -u root -p < "%SCRIPT_DIR%seeds\mysql_seed.sql"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo Database setup completed successfully!
    echo ================================================
    echo.
    echo Next steps:
    echo 1. Make sure your backend server is running
    echo 2. Test the API: curl http://127.0.0.1:8000/api/products/bestsellers
    echo.
) else (
    echo.
    echo ================================================
    echo Database setup failed!
    echo ================================================
    echo.
    echo Common issues:
    echo - Wrong MySQL password
    echo - MySQL server not running
    echo - MySQL user doesn't have permission to create databases
    echo.
)

pause





