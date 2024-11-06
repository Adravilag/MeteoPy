@echo off
@chcp 65001 >nul
SETLOCAL ENABLEDELAYEDEXPANSION

REM Crear entorno virtual si no existe
if not exist "venv" (
    python -m venv venv
    echo Entorno virtual creado en la carpeta 'venv'.
) else (
    echo Entorno virtual ya existe.
)

REM Activar el entorno virtual
if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo Entorno virtual activado.
) else (
    echo Error: No se pudo activar el entorno virtual.
    pause
    exit /b
)

REM Usar ruta absoluta para python en el entorno virtual y forzar instalación de pip
set "VENV_PYTHON=venv\Scripts\python.exe"
if exist %VENV_PYTHON% (
    echo Python encontrado en el entorno virtual. Instalando dependencias...
    %VENV_PYTHON% -m ensurepip --upgrade
    %VENV_PYTHON% -m pip install --upgrade pip
    %VENV_PYTHON% -m pip install -r requirements.txt
    echo Dependencias instaladas correctamente.
) else (
    echo Error: No se pudo encontrar python en el entorno virtual.
    echo Verifica si el entorno virtual contiene python.exe en venv\Scripts.
    echo Si el archivo no está presente, intenta recrear el entorno virtual.
    pause
    exit /b
)

REM Crear o actualizar archivo .env con GITHUB_TOKEN, TEMPLATE_PATH y OPENAI_API_KEY
set "env_path=.env"
set "template_path=%cd%\config\templates\MeteoData_Template.xlsm"

REM Añadir GITHUB_TOKEN, TEMPLATE_PATH y OPENAI_API_KEY si no están presentes en .env
set "found_template_path=false"
set "found_openai_api_key=false"

REM Verificar existencia de TEMPLATE_PATH y OPENAI_API_KEY
for /f "tokens=1* delims==" %%i in ('type "%env_path%"') do (
    if /i "%%i"=="TEMPLATE_PATH" set "found_template_path=true"
    if /i "%%i"=="OPENAI_API_KEY" set "found_openai_api_key=true"
)

REM Añadir TEMPLATE_PATH si no se encontró
if "%found_template_path%"=="false" (
    echo TEMPLATE_PATH=%template_path% >> "%env_path%"
    echo TEMPLATE_PATH agregado a .env
)

REM Añadir OPENAI_API_KEY si no se encontró
if "%found_openai_api_key%"=="false" (
    echo OPENAI_API_KEY=your_openai_api_key_here >> "%env_path%"
    echo OPENAI_API_KEY agregado a .env
)

echo Configuración inicial completada.
pause
