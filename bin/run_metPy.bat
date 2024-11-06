@echo off
REM Ensure we're in the project root directory
cd ..

REM Activate the virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Could not find the virtual environment. Make sure it is located in the "venv" folder.
    exit /b
)

REM Run the app_runner.py script with the 'met' argument
echo Running metPy functionality...
python src\core\app_runner.py met

REM Keep the window open to view the results
pause
