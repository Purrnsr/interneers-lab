@echo off

echo Activating virtual environment...
call venv\Scripts\activate

echo Running tests...
coverage run manage.py test
IF %ERRORLEVEL% NEQ 0 (
    echo Tests failed! 
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Coverage Report:
coverage report

echo.
echo All tests passed 
pause