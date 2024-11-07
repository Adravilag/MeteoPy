@echo off
REM Cambia al directorio donde está el script .bat
cd /d "%~dp0"

REM Ejecuta el script de Python en bin/scripts
python bin\scripts\venv_setup.py

REM Mantiene la ventana abierta
echo.
echo Presiona cualquier tecla para salir...
pause
