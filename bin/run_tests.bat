@echo off
REM Change to the project root directory
cd /d %~dp0..

REM Verify the current path to ensure we are in the correct directory
echo Current path: %cd%

REM Activate the virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Could not find the virtual environment. Make sure it's in the "venv" folder.
    exit /b
)

REM Message to confirm that we are in the virtual environment
echo Virtual environment activated.

REM Run each test individually
echo Running unit tests...

REM List all test files
for %%f in (tests\*.py) do (
    echo Running test %%f...
    python -m unittest %%f
    if %errorlevel% neq 0 (
        echo An error occurred while running the test %%f.
    ) else (
        echo Test %%f ran successfully.
    )
    REM Pause to view the results before clearing the screen
    pause
    cls
)

REM Final message
echo All tests completed.
pause
