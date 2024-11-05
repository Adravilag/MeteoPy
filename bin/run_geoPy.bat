@echo off
REM Cambiar al directorio raíz del proyecto
cd ..

REM Verificar la ruta actual para asegurar que estamos en el directorio correcto
echo Ruta actual: %cd%

REM Activar el entorno virtual
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo No se pudo encontrar el entorno virtual. Asegúrate de que está en la carpeta "venv".
    exit /b
)

REM Mensaje para confirmar que estamos en el entorno virtual
echo Entorno virtual activado.

REM Configurar el idioma (opcional)
set LANGUAGE=es

REM Ejecutar el script metPy.py en src\data_processing con el idioma especificado
echo Ejecutando metPy.py con idioma %LANGUAGE%...
python src\visualization\geoPy.py %LANGUAGE%

REM Comprobar si el script se ejecutó correctamente
if %errorlevel% neq 0 (
    echo Hubo un error al ejecutar geoPy.py.
) else (
    echo Script ejecutado correctamente.
)

REM Mantener la ventana abierta para ver los resultados
pause
