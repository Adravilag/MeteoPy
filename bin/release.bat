@echo off
@chcp 65001 >nul
SETLOCAL ENABLEDELAYEDEXPANSION

REM Cambiar a la rama main si no estamos en ella
for /f %%i in ('git rev-parse --abbrev-ref HEAD') do set BRANCH_NAME=%%i
if not "%BRANCH_NAME%"=="main" (
    echo Cambiando a la rama main...
    git checkout main
    IF ERRORLEVEL 1 (
        echo Error: No se pudo cambiar a la rama main.
        pause
        exit /b
    )
)

REM Ruta al archivo .env
SET ENV_FILE=../.env

REM Leer el archivo .env y extraer el token
if exist %ENV_FILE% (
    for /f "tokens=1,2 delims==" %%a in (%ENV_FILE%) do (
        if "%%a"=="GITHUB_TOKEN" set TOKEN=%%b
    )
) else (
    echo Error: No se encontró el archivo .env en %ENV_FILE%.
    pause
    exit /b
)

REM Verificar si el token se cargó correctamente
if "%TOKEN%"=="" (
    echo Error: No se pudo cargar el token desde el archivo .env.
    pause
    exit /b
) else (
    echo Token cargado correctamente.
)

REM Configuración inicial
SET REPO=Adravilag/MeteoWave

REM Obtener la última etiqueta creada
echo Obteniendo la última etiqueta en el repositorio...
for /f %%i in ('git tag --sort=-creatordate') do (set VERSION=%%i & goto :found_version)

:found_version
REM Verificar si se obtuvo una versión; establecer versión inicial si está vacía
IF "%VERSION%"=="" (
    set VERSION=0.1.0
    echo No se encontró ninguna etiqueta previa. Estableciendo versión inicial: !VERSION!
) else (
    REM Limpiar el prefijo "v" si está presente en la etiqueta
    set VERSION=%VERSION:v=%
    echo Versión actual de la aplicación: !VERSION!
)

REM Solicitar la nueva versión manualmente
SET /P NEW_VERSION="Introduce la nueva versión (formato x.x.x): "

REM Validar que la nueva versión no esté vacía
IF "!NEW_VERSION!"=="" (
    echo Error: La versión introducida no es válida.
    pause
    exit /b
)

echo Nueva versión: !NEW_VERSION!

REM Pedir una descripción de los cambios
SET /P CHANGE_DESCRIPTION="Introduce la descripción de los cambios: "

REM Agregar todos los archivos, incluyendo los no rastreados
git add -A

REM Confirmar todos los cambios
git commit -m "Release version !NEW_VERSION! - !CHANGE_DESCRIPTION!"

REM Empujar todos los cambios al repositorio
git push origin main
IF ERRORLEVEL 1 (
    echo Error al hacer push de los cambios al repositorio.
    pause
    exit /b
)

REM Verificar si el tag existe antes de eliminarlo
git tag -l "v!NEW_VERSION!" >nul 2>&1
IF NOT ERRORLEVEL 1 (
    git tag -d v!NEW_VERSION!
    git push origin :refs/tags/v!NEW_VERSION!
)

REM Crear un nuevo tag
git tag -a v!NEW_VERSION! -m "Release version !NEW_VERSION! - !CHANGE_DESCRIPTION!"
git push origin v!NEW_VERSION!
IF ERRORLEVEL 1 (
    echo Error al hacer push del tag al repositorio.
    pause
    exit /b
)

REM Crear un release en GitHub usando curl y guardar la respuesta en la carpeta temporal del sistema
set TEMP_RESPONSE="%TEMP%\response.json"
curl -X POST -H "Authorization: Bearer %TOKEN%" ^
    -H "Accept: application/vnd.github.v3+json" ^
    https://api.github.com/repos/%REPO%/releases ^
    -d "{\"tag_name\": \"v!NEW_VERSION!\", \"name\": \"v!NEW_VERSION!\", \"body\": \"!CHANGE_DESCRIPTION!\", \"draft\": false, \"prerelease\": false}" ^
    -o %TEMP_RESPONSE%

REM Verificar si el release se creó correctamente buscando "html_url"
set RESULT=fail
for /f "tokens=1,2 delims=: " %%A in (%TEMP_RESPONSE%) do (
    if "%%A"=="\"html_url\"" (
        set RESULT=success
    )
)

if "!RESULT!"=="success" (
    echo Release completado con éxito en GitHub.
) else (
    echo Error: La creación del release falló. Verifique el token o el repositorio.
    type %TEMP_RESPONSE%
    pause
    exit /b
)

REM Borrar el archivo temporal response.json
del /f /q %TEMP_RESPONSE%

REM Mensaje de confirmación final
echo El release y la nueva versión se han creado correctamente en GitHub.
pause
