@echo off
@chcp 65001 >nul
SETLOCAL ENABLEDELAYEDEXPANSION

REM Crear entorno virtual
python -m venv venv
echo Entorno virtual creado en la carpeta 'venv'.

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar dependencias desde requirements.txt
pip install -r requirements.txt
echo Dependencias instaladas correctamente.

REM Crear archivo .env si no existe
IF NOT EXIST .env (
    echo GITHUB_TOKEN=tu_token_aqui > .env
    echo Archivo .env creado. Por favor, añade tus credenciales en el archivo .env.
) ELSE (
    echo El archivo .env ya existe.
)

echo Configuración inicial completada.
pause
