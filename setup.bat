@echo off
@chcp 65001 >nul

REM Inicializar estado de activación
set "VIRTUAL_ENV_ACTIVE=1"  REM 1 para activado, 0 para desactivado

:MENU
cls
echo ------------------------------------
echo          Menu de Configuracion
echo ------------------------------------
echo 1. Crear entorno virtual
echo 2. Activar/Desactivar entorno virtual (actualmente %VIRTUAL_ENV_ACTIVE_STATUS%)
echo 3. Instalar dependencias
echo 4. Actualizar archivo .env
echo 5. Salir
echo ------------------------------------

REM Cambiar el estado a ON/OFF para mostrar en el menú
if "%VIRTUAL_ENV_ACTIVE%"=="1" (
    set "VIRTUAL_ENV_ACTIVE_STATUS=ON"
) else (
    set "VIRTUAL_ENV_ACTIVE_STATUS=OFF"
)

set /p option="Selecciona una opción: "

REM Ejecuta la opción correspondiente
if "%option%"=="1" (
    python bin\scripts\setup_cli.py --crear
    pause
    goto MENU
) else if "%option%"=="2" (
    if "%VIRTUAL_ENV_ACTIVE%"=="1" (
        set "VIRTUAL_ENV_ACTIVE=0"
        echo Entorno virtual desactivado.
    ) else (
        set "VIRTUAL_ENV_ACTIVE=1"
        echo Entorno virtual activado.
    )
    pause
    goto MENU
) else if "%option%"=="3" (
    python bin\scripts\setup_cli.py --instalar
    pause
    goto MENU
) else if "%option%"=="4" (
    python bin\scripts\setup_cli.py --actualizar-env
    pause
    goto MENU
) else if "%option%"=="5" (
    echo Saliendo...
    exit /b
) else (
    echo Opcion invalida, por favor selecciona una opcion correcta.
    pause
    goto MENU
)
