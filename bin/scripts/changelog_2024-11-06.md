Changelog generado:

Commit Message: Cambios en la estructura
Changes:
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index dc03e8a..da91515 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -21,4 +21,6 @@ jobs:
         run: |
           python -m venv venv
           . venv/bin/activate
-          pip install -r requirements.txt
\ No newline at end of file
+          pip install -r requirements.txt
+          # Eliminar pywin32 en entornos no Windows
+          sed -i '/pywin32/d' requirements.txt
diff --git a/bin/run_geoPy.bat b/bin/run_geoPy.bat
index bb0ad83..3f4be20 100644
--- a/bin/run_geoPy.bat
+++ b/bin/run_geoPy.bat
@@ -1,34 +1,18 @@
 @echo off
-REM Cambiar al directorio raÃ­z del proyecto
+REM Ensure we're in the project root directory
 cd ..
 
-REM Verificar la ruta actual para asegurar que estamos en el directorio correcto
-echo Ruta actual: %cd%
-
-REM Activar el entorno virtual
+REM Activate the virtual environment
 if exist venv\Scripts\activate (
     call venv\Scripts\activate
 ) else (
-    echo No se pudo encontrar el entorno virtual. AsegÃºrate de que estÃ¡ en la carpeta "venv".
+    echo Could not find the virtual environment. Make sure it is located in the "venv" folder.
     exit /b
 )
 
-REM Mensaje para confirmar que estamos en el entorno virtual
-echo Entorno virtual activado.
-
-REM Configurar el idioma (opcional)
-set LANGUAGE=es
-
-REM Ejecutar el script metPy.py en src\data_processing con el idioma especificado
-echo Ejecutando metPy.py con idioma %LANGUAGE%...
-python src\visualization\geoPy.py %LANGUAGE%
-
-REM Comprobar si el script se ejecutÃ³ correctamente
-if %errorlevel% neq 0 (
-    echo Hubo un error al ejecutar geoPy.py.
-) else (
-    echo Script ejecutado correctamente.
-)
+REM Run the app_runner.py script with the 'geo' argument
+echo Running geoPy functionality...
+python src\core\app_runner.py geo
 
-REM Mantener la ventana abierta para ver los resultados
+REM Keep the window open to view the results
 pause
diff --git a/bin/run_metPy.bat b/bin/run_metPy.bat
index ecff588..c5df065 100644
--- a/bin/run_metPy.bat
+++ b/bin/run_metPy.bat
@@ -1,35 +1,18 @@
 @echo off
-REM Cambiar al directorio raÃ­z del proyecto
+REM Ensure we're in the project root directory
 cd ..
 
-REM Verificar la ruta actual para asegurar que estamos en el directorio correcto
-echo Ruta actual: %cd%
-
-REM Activar el entorno virtual
+REM Activate the virtual environment
 if exist venv\Scripts\activate (
     call venv\Scripts\activate
 ) else (
-    echo No se pudo encontrar el entorno virtual. AsegÃºrate de que estÃ¡ en la carpeta "venv".
+    echo Could not find the virtual environment. Make sure it is located in the "venv" folder.
     exit /b
 )
 
-REM Mensaje para confirmar que estamos en el entorno virtual
-echo Entorno virtual activado.
-
-REM Configurar el idioma (opcional)
-REM Cambia "es" por "en" si deseas ejecutar en inglÃ©s
-set LANGUAGE=es
-
-REM Ejecutar el script metPy.py en src\data_processing con el idioma especificado
-echo Ejecutando metPy.py con idioma %LANGUAGE%...
-python src\data_processing\metPy.py %LANGUAGE%
-
-REM Comprobar si el script se ejecutÃ³ correctamente
-if %errorlevel% neq 0 (
-    echo Hubo un error al ejecutar metPy.py.
-) else (
-    echo Script ejecutado correctamente.
-)
+REM Run the app_runner.py script with the 'met' argument
+echo Running metPy functionality...
+python src\core\app_runner.py met
 
-REM Mantener la ventana abierta para ver los resultados
+REM Keep the window open to view the results
 pause
diff --git a/config/config.json b/config/config.json
index b808e2a..e740a09 100644
--- a/config/config.json
+++ b/config/config.json
@@ -13,15 +13,12 @@
         39
     ],
     "shapefile_path": "config/shp/gadm41_ESP_4.shp",
-    "language": "en",
+    "language": "es",
     "data_directory": "data",
     "version": "1.1.4",
     "comunidades": [
         "ANDALUCIA",
-        "VALENCIA",
-        "CATALUÃ‘A",
-        "MADRID",
-        "GALICIA"
+        "VALENCIA"
     ],
     "api_settings": {
         "base_url": "https://api.open-meteo.com/v1/forecast",
@@ -35,4 +32,4 @@
         ],
         "timezone": "Europe/Madrid"
     }
-}
\ No newline at end of file
+}
diff --git a/doc/changelog.md b/doc/changelog.md
index 0424a47..acb3e2d 100644
--- a/doc/changelog.md
+++ b/doc/changelog.md
@@ -1,56 +1,58 @@
+# Changelog - 2024-11-06
 
-# Changelog
+## Version 1.4.0 - Project Architecture Updates
 
-All notable changes to this project will be documented in this file.
+### Summary of Changes
 
-The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
-and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
+This update introduces significant modifications to the project structure, dependency management, and automated changelog generation. Below are detailed changes for each relevant file.
 
-## [1.1.4] - 2024-11-06
-### Added
-- Added support for configurable visualization parameters in `config.json`.
-- Implemented `ci.yml` GitHub Actions workflow for continuous integration.
-- New `bin` batch files for running `geoPy.py` and `metPy.py` scripts with localization options.
+### Detailed Changes by File
 
-### Changed
-- Refactored `core.py` and `metPy.py` to use modular functions from `utils.py`.
-- Moved `geoPy.py` and `metPy.py` to `src` directory for a clearer project structure.
+#### `.gitignore`
+- Added `temp` to exclude temporary files from version control.
+- Adjusted the `__pycache__` entry to improve handling of Python cache files.
 
-### Fixed
-- Corrected issues with Excel file handling in `metPy.py` to avoid file locks.
+#### `bin/scripts/generate_changelog.py`
+- **New file**: Created `generate_changelog.py` in the `bin/scripts/` directory to automate changelog generation.
+- **Key functionalities**:
+  - Extraction of recent commits from the repository using `git log`.
+  - Retrieval of differences in each commit using `git diff`.
+  - Generation and storage of a detailed Markdown file documenting changes.
 
-## [1.1.3] - 2024-11-05
-### Added
-- Integrated `.env` configuration file support for sensitive information like `GITHUB_TOKEN`.
-- Added error handling for API rate limits and network issues in `data_acquisition` module.
+#### `README.md`
+- Updated documentation to reflect changes in the project structure and new automation scripts.
+- Added details on environment configuration and the use of the changelog generation script.
 
-### Changed
-- Updated `architecture.md` to reflect new modules and functions.
+#### `src/core.py`
+- Refactored to improve modularity and facilitate interaction between modules.
+- **New functions**:
+  - `menu_principal()` to organize user navigation through various application options.
+  - `seleccionar_comunidad()` added to allow dynamic selection of the autonomous community.
 
-### Fixed
-- Fixed `data_processing` module to handle missing or outlier values in API data.
+#### `config/config.json`
+- Updated default configurations.
+- **New parameters added**:
+  - `language`: Defines the interface language.
+  - `api_settings`: Contains configurations for interaction with the Open-Meteo API, such as `base_url` and `daily_params`.
 
-## [1.1.2] - 2024-11-05
-### Added
-- Included initial CI/CD setup for GitHub Actions.
-- Introduced locale support for English and Spanish (`locales/en.json` and `locales/es.json`).
+#### `.github/workflows/ci.yml`
+- Modified CI/CD workflow steps to integrate unit and integration tests.
+- **Key changes**:
+  - Removed redundant steps.
+  - Updated Python version used in tests.
+  - Improved setup steps for dependency installation and test execution.
 
-### Changed
-- Refined project structure with modular directories for core, data processing, and visualization.
-- Updated `config.json` to include `comunidades` list and API settings.
+#### `MeteoWave_License.txt`
+- Updated license to reflect the current project version.
+- Resolved version conflicts within the license file.
 
-### Fixed
-- Resolved issues with data formatting in Excel templates.
+### Error Handling Improvements
+- Added exception handling in multiple parts of the code to manage common errors, such as missing configuration files or HTTP request failures.
 
-## [1.1.1] - 2024-11-05
-### Added
-- Implemented data visualization with dynamic map interaction in `visualization/geoPy.py`.
+### General Refactoring
+- Restructured directories for better project organization.
+- Modularized code in `core.py`, `data_acquisition.py`, and `data_processing.py` to enhance maintainability and scalability.
 
-### Changed
-- Reorganized `config` directory to include `templates` for Excel files.
+---
 
-## [1.1.0] - 2024-11-01
-### Added
-- Initial release of **MeteoWave** with modules for data acquisition, processing, and visualization.
-- Basic batch files for executing Python scripts.
-- Added `config.json` for centralized project configuration.
+**Note:** This update marks a significant milestone in the evolution of **MeteoWave**, focusing on automation and continuous improvement of integration and deployment processes, as well as better project organization to facilitate future expansions and collaborations.
\ No newline at end of file
diff --git a/locales/en.json b/locales/en.json
index a36014b..7940e22 100644
--- a/locales/en.json
+++ b/locales/en.json
@@ -32,11 +32,20 @@
     "wind_gusts_title": "Wind Gusts (km/h)",
     "wind_speed_title": "Wind Speed (km/h)",
     "precipitation_sum_title": "Precipitation Accumulated (mm)",
-    "temp_min_button": "Temp Min",
-    "temp_max_button": "Temp Max",
+    "temperature_min_button": "Temp Min",
+    "temperature_max_button": "Temp Max",
     "wind_gusts_button": "Wind Gusts",
     "wind_speed_button": "Wind Speed",
     "precipitation_sum_button": "Precipitation",
-    "main_menu": "Main Menu",
-    "invalid_selection": "Invalid selection."
+    "invalid_selection": "Invalid selection.",
+    "provide_argument": "Please provide an argument (â€˜geoâ€™ or â€˜metâ€™).",
+    "running_geo": "Running geo...",
+    "running_met": "Running met...",
+    "invalid_argument": "Invalid argument.",
+    "shapefile_not_found": "Error: Shape file not found in",
+    "file_exists": "File already exists:",
+    "template_copied": "Template copied to:",
+    "error_copy_template": "Error copying the template:",
+    "error_processing_data": "Error processing the data:",
+    "file_selected": "File selected"
 }
diff --git a/locales/es.json b/locales/es.json
index a148869..0ce119c 100644
--- a/locales/es.json
+++ b/locales/es.json
@@ -1,42 +1,51 @@
 {
     "welcome_message": "Bienvenido a MeteoWave",
-    "select_option": "Selecciona una opciÃ³n:",
-    "select_community": "Selecciona una comunidad autÃ³noma:",
-    "select_community_option": "Selecciona la comunidad autÃ³noma (por nÃºmero):",
+    "select_option": "Seleccione una opciÃ³n:",
+    "select_community": "Seleccione una comunidad autÃ³noma:",
+    "select_community_option": "Seleccione la comunidad autÃ³noma (por nÃºmero):",
     "available_dates": "Fechas disponibles:",
     "process_data": "Procesar datos meteorolÃ³gicos",
     "exit": "Salir",
     "no_files_available": "No hay archivos disponibles en el directorio 'data/2024'.",
     "available_files": "Archivos disponibles:",
-    "select_file": "Selecciona el nÃºmero del archivo a utilizar:",
-    "selection_out_of_range": "SelecciÃ³n fuera de rango. Intenta nuevamente.",
-    "invalid_input": "Entrada no vÃ¡lida. Por favor, introduce un nÃºmero.",
+    "select_file": "Seleccione el nÃºmero del archivo a utilizar:",
+    "selection_out_of_range": "SelecciÃ³n fuera de rango. Intente de nuevo.",
+    "invalid_input": "Entrada no vÃ¡lida. Por favor, ingrese un nÃºmero.",
     "error_file_date_format": "Error: El archivo seleccionado no tiene la fecha en el formato esperado.",
     "no_communities_found": "No se encontraron comunidades.",
     "date_not_found": "Fecha {date} no encontrada en los datos meteorolÃ³gicos.",
-    "processing_error": "Error al procesar la fila {row}: {error}",
+    "processing_error": "Error procesando la fila {row}: {error}",
     "data_saved": "Datos meteorolÃ³gicos guardados en {archivo}",
     "too_many_requests": "Demasiadas solicitudes. Esperando antes de reintentar...",
     "request_error": "Error en la solicitud: CÃ³digo {code}",
-    "max_retries_reached": "No se pudo obtener las fechas disponibles despuÃ©s de varios intentos.",
-    "exists": "Existente",
+    "max_retries_reached": "No se pudieron obtener fechas disponibles despuÃ©s de varios intentos.",
+    "exists": "Existe",
     "last_update": "Ãšltima actualizaciÃ³n",
-    "data_filled": "Datos llenos",
+    "data_filled": "Datos completados",
     "does_not_exist": "No existe",
-    "select_date_option": "Selecciona la fecha (por nÃºmero):",
+    "select_date_option": "Seleccione la fecha (por nÃºmero):",
     "exiting": "Saliendo del programa...",
     "available_autonomous_communities": "Comunidades AutÃ³nomas disponibles:",
     "error_loading_shapefile": "Error al cargar el archivo de shapes.",
     "temperature_min_title": "Temperatura MÃ­nima (Â°C)",
     "temperature_max_title": "Temperatura MÃ¡xima (Â°C)",
-    "wind_gusts_title": "Rachas de Viento (km/h)",
+    "wind_gusts_title": "RÃ¡fagas de Viento (km/h)",
     "wind_speed_title": "Velocidad del Viento (km/h)",
     "precipitation_sum_title": "PrecipitaciÃ³n Acumulada (mm)",
-    "temp_min_button": "Temp Min",
-    "temp_max_button": "Temp Max",
-    "wind_gusts_button": "Rachas Viento",
-    "wind_speed_button": "Velocidad Viento",
+    "temperature_min_button": "Temp MÃ­n",
+    "temperature_max_button": "Temp MÃ¡x",
+    "wind_gusts_button": "RÃ¡fagas de Viento",
+    "wind_speed_button": "Velocidad del Viento",
     "precipitation_sum_button": "PrecipitaciÃ³n",
-    "main_menu": "MenÃº Principal",
-    "invalid_selection": "SelecciÃ³n invÃ¡lida."
+    "invalid_selection": "SelecciÃ³n invÃ¡lida.",
+    "provide_argument": "Por favor, proporcione un argumento (â€˜geoâ€™ o â€˜metâ€™).",
+    "running_geo": "Ejecutando geo...",
+    "running_met": "Ejecutando met...",
+    "invalid_argument": "Argumento no vÃ¡lido.",
+    "shapefile_not_found": "Error: No se encontrÃ³ el archivo de shapes en",
+    "file_exists": "El archivo ya existe:",
+    "template_copied": "Plantilla copiada en:",
+    "error_copy_template": "Error al copiar la plantilla:",
+    "error_processing_data": "Error al procesar los datos:",
+    "file_selected": "Archivo seleccionado"
 }
diff --git a/src/core/app_runner.py b/src/core/app_runner.py
new file mode 100644
index 0000000..590c29c
--- /dev/null
+++ b/src/core/app_runner.py
@@ -0,0 +1,45 @@
+# app_runner.py
+import sys
+import os
+
+# Definir el directorio raÃ­z del proyecto y el archivo de configuraciÃ³n
+project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
+config_path = os.path.join(project_root, 'config', 'config.json')
+
+# Agregar el directorio `src` a `sys.path`
+src_path = os.path.join(project_root, 'src')
+sys.path.insert(0, src_path)
+
+from utils.utils import cargar_configuracion, cargar_traducciones
+from visualization.geoPy import main as run_geo
+from data_processing.metPy import main as run_met
+
+print("src_path:", src_path)
+print("config_path:", config_path)
+
+# Cargar configuraciÃ³n y traducciones
+try:
+    config = cargar_configuracion(config_path)
+    language = config.get("language", "en")
+    traducciones = cargar_traducciones(language)
+except Exception as e:
+    print(f"Error cargando configuraciÃ³n o traducciones: {e}")
+    sys.exit(1)
+
+def main():
+    if len(sys.argv) < 2:
+        print(traducciones["provide_argument"])
+        return
+
+    arg = sys.argv[1].lower()
+    if arg == 'geo':
+        print(traducciones["running_geo"])
+        run_geo(config, traducciones)
+    elif arg == 'met':
+        print(traducciones["running_met"])
+        run_met(config, traducciones)
+    else:
+        print(traducciones["invalid_argument"])
+
+if __name__ == "__main__":
+    main()
diff --git a/src/core/core.py b/src/core/core.py
deleted file mode 100644
index 3af15df..0000000
--- a/src/core/core.py
+++ /dev/null
@@ -1,145 +0,0 @@
-import os
-from datetime import datetime
-from src.utils.utils import (
-    cls,
-    cargar_configuracion,
-    cargar_traducciones,
-    inicializar_directorios,
-    copiar_plantilla_si_no_existe,
-    obtener_fechas_disponibles_api,
-    obtener_datos_meteo
-)
-import win32com.client as win32
-
-def menu_principal(config, plantilla, data_dir, api_settings):
-    """FunciÃ³n principal del menÃº para procesar datos meteorolÃ³gicos."""
-    latitud, longitud = 37.3891, -5.9845
-    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud, api_settings)
-
-    if not fechas_disponibles:
-        print("No se encontraron fechas disponibles.")
-        input("Presione Enter para continuar...")
-        return
-
-    while True:
-        print("\n--- MenÃº Principal ---")
-        print("1. Procesar datos meteorolÃ³gicos")
-        print("2. Salir")
-        opcion = input("Seleccione una opciÃ³n: ")
-
-        if opcion == '1':
-            print("\nFechas disponibles:")
-            for i, fecha in enumerate(fechas_disponibles, start=1):
-                print(f"{i}. {fecha}")
-
-            while True:
-                try:
-                    seleccion_fecha = int(input("Seleccione una fecha (por nÃºmero): ")) - 1
-                    if 0 <= seleccion_fecha < len(fechas_disponibles):
-                        fecha = datetime.strptime(fechas_disponibles[seleccion_fecha], '%Y-%m-%d')
-                        break
-                    else:
-                        print("SelecciÃ³n fuera de rango.")
-                except ValueError:
-                    print("Entrada invÃ¡lida. Intente nuevamente.")
-
-            # Seleccionar comunidad autÃ³noma
-            comunidad = seleccionar_comunidad(config)
-            if comunidad is None:
-                print("No se seleccionÃ³ ninguna comunidad.")
-                continue
-
-            # Procesar datos con la fecha y comunidad seleccionada
-            procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings)
-
-            input("Procesamiento completado. Presione Enter para ver los resultados...")
-
-        elif opcion == '2':
-            print("Saliendo...")
-            break
-        else:
-            print("SelecciÃ³n invÃ¡lida.")
-            input("Presione Enter para continuar...")
-
-def seleccionar_comunidad(config):
-    """Permite seleccionar una comunidad autÃ³noma desde la configuraciÃ³n."""
-    comunidades = config.get("comunidades", [])
-    if not comunidades:
-        print("No se encontraron comunidades en la configuraciÃ³n.")
-        input("Presione Enter para continuar...")
-        return None
-
-    print("Seleccione una comunidad autÃ³noma:")
-    for i, comunidad in enumerate(comunidades, start=1):
-        print(f"{i}. {comunidad}")
-
-    while True:
-        try:
-            seleccion = int(input("Seleccione una opciÃ³n: ")) - 1
-            if 0 <= seleccion < len(comunidades):
-                return comunidades[seleccion]
-            else:
-                print("SelecciÃ³n fuera de rango.")
-        except ValueError:
-            print("Entrada invÃ¡lida.")
-
-def procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings):
-    """Procesa los datos meteorolÃ³gicos para la fecha y comunidad especificada."""
-    archivo_destino = copiar_plantilla_si_no_existe(fecha, plantilla, data_dir)
-
-    # Verificar si el archivo de destino existe antes de intentar abrirlo
-    if not archivo_destino or not os.path.exists(archivo_destino):
-        print(f"Error: El archivo {archivo_destino} no se pudo crear o no existe.")
-        return
-
-    excel = win32.Dispatch("Excel.Application")
-    excel.Visible = False  # Oculta Excel durante el procesamiento
-    wb = None
-
-    try:
-        print(f"Intentando abrir el archivo de destino: {archivo_destino}")
-        wb = excel.Workbooks.Open(archivo_destino)  # Abrir archivo de destino
-        ws = wb.Sheets(comunidad)
-        fecha_str = fecha.strftime('%Y-%m-%d')
-
-        # Llenar datos en el Excel
-        for row in range(2, ws.UsedRange.Rows.Count + 1):
-            coordenadas = ws.Cells(row, 3).Value  # Columna C
-            if coordenadas:
-                latitud, longitud = map(float, coordenadas.split(', '))
-                datos = obtener_datos_meteo(latitud, longitud, fecha, api_settings)
-
-                if datos:
-                    ws.Cells(row, 8).Value = datos['temperature_min']  # Columna H
-                    ws.Cells(row, 9).Value = datos['temperature_max']  # Columna I
-                    ws.Cells(row, 10).Value = datos['windspeed_max']  # Columna J
-                    ws.Cells(row, 11).Value = datos['windgusts_max']  # Columna K
-                    ws.Cells(row, 12).Value = datos['winddirection_dominant']  # Columna L
-                    ws.Cells(row, 13).Value = datos['precipitation_sum']  # Columna M
-                    ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Columna N
-                else:
-                    print(f"Datos no encontrados para la fecha: {fecha_str}")
-
-        wb.Save()
-        print(f"Datos meteorolÃ³gicos guardados en {archivo_destino}")
-
-    except Exception as e:
-        print(f"OcurriÃ³ un error al procesar el archivo de datos: {e}")
-
-    finally:
-        if wb:
-            wb.Close(False)
-        excel.Quit()
-
-# EjecuciÃ³n principal
-if __name__ == "__main__":
-    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
-    config = cargar_configuracion(config_path)
-    traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(os.path.dirname(__file__), '..', '..', 'locales'))
-    data_dir = config.get("data_directory", "data")
-    plantilla = config.get("template_path", "config/templates/MeteoData_Template.xlsm")
-    api_settings = config.get("api_settings", {})
-    
-    inicializar_directorios(data_dir)
-    cls()
-    menu_principal(config, plantilla, data_dir, api_settings)
diff --git a/src/data_processing/metPy.py b/src/data_processing/metPy.py
index cdbaa0b..c60c113 100644
--- a/src/data_processing/metPy.py
+++ b/src/data_processing/metPy.py
@@ -1,136 +1,212 @@
+# metPy.py
+
 import os
-import sys
+import pandas as pd
+import win32com.client as win32
+import requests
 from datetime import datetime
 from dotenv import load_dotenv
-import win32com.client as win32
-
-# Configurar la ruta absoluta del proyecto y aÃ±adir `src` al `sys.path`
-project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
-src_path = os.path.join(project_root, 'src')
-sys.path.insert(0, src_path)
-
-# Importar los mÃ³dulos desde `src`
-from utils.utils import (
-    cargar_configuracion,
-    cargar_traducciones,
-    inicializar_directorios,
-    copiar_plantilla_si_no_existe,
-    obtener_fechas_disponibles_api,
-    obtener_datos_meteo,
-    seleccionar_comunidad
-)
-
-load_dotenv()  # Carga las variables del .env
-
-def procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings):
-    """Procesa los datos meteorolÃ³gicos para la fecha y comunidad especificadas usando win32com."""
-    archivo_destino = copiar_plantilla_si_no_existe(fecha, plantilla, data_dir)
-
-    # Convertimos la ruta en absoluta para asegurar que Excel la interprete correctamente
-    archivo_destino = os.path.abspath(archivo_destino) if archivo_destino else None
-
-    # Verificar si el archivo de destino existe antes de intentar abrirlo
-    if not archivo_destino or not os.path.exists(archivo_destino):
-        print(f"Error: El archivo {archivo_destino} no se pudo crear o no existe.")
-        return
-
-    excel = win32.Dispatch("Excel.Application")
-    excel.Visible = False  # Oculta Excel durante el procesamiento
-    wb = None  # Asegura que wb estÃ© definida para evitar errores de cierre
-
-    try:
-        print(f"Intentando abrir el archivo de destino: {archivo_destino}")
-        wb = excel.Workbooks.Open(archivo_destino)  # Abrir archivo de destino con ruta absoluta
-        ws = wb.Sheets(comunidad)
+from utils.utils import cargar_configuracion, cargar_traducciones
+import time
+
+def main(config, traducciones):
+    # ConfiguraciÃ³n del proyecto
+    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
+    data_dir = os.path.abspath(config.get("data_directory", "data"))
+    plantilla = os.getenv("TEMPLATE_PATH", os.path.join(project_root, "config", "templates", "MeteoData_Template.xlsm"))
+    api_settings = config.get("api_settings", {})
+
+    def obtener_fechas_disponibles_api(latitud, longitud):
+        """Obtiene las fechas de pronÃ³stico disponibles desde la API de Open-Meteo."""
+        url = f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}"
+        for intento in range(5):  # MÃ¡ximo 5 reintentos
+            response = requests.get(url)
+            if response.status_code == 200:
+                return response.json().get('daily', {}).get('time', [])
+            elif response.status_code == 429:
+                print("Demasiadas solicitudes. Esperando para reintentar...")
+                time.sleep(5)
+            else:
+                print(f"Error en la solicitud. CÃ³digo de estado: {response.status_code}")
+                return []
+        print("Se alcanzÃ³ el nÃºmero mÃ¡ximo de reintentos.")
+        return []
+    
+    def obtener_datos_meteo(latitud, longitud, fecha):
+        """Obtiene datos meteorolÃ³gicos para una fecha y coordenadas especÃ­ficas desde la API."""
         fecha_str = fecha.strftime('%Y-%m-%d')
-
-        for row in range(2, ws.UsedRange.Rows.Count + 1):
-            coordenadas = ws.Cells(row, 3).Value  # Columna C
-            if coordenadas:
-                latitud, longitud = map(float, coordenadas.split(', '))
-                datos = obtener_datos_meteo(latitud, longitud, fecha, api_settings)
-
-                if datos:
-                    ws.Cells(row, 8).Value = datos['temperature_min']  # Columna H
-                    ws.Cells(row, 9).Value = datos['temperature_max']  # Columna I
-                    ws.Cells(row, 10).Value = datos['windspeed_max']  # Columna J
-                    ws.Cells(row, 11).Value = datos['windgusts_max']  # Columna K
-                    ws.Cells(row, 12).Value = datos['winddirection_dominant']  # Columna L
-                    ws.Cells(row, 13).Value = datos['precipitation_sum']  # Columna M
-                    ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Columna N
-                else:
-                    print(f"Datos no encontrados para la fecha: {fecha_str}")
-
-        wb.Save()
-        print(f"Datos meteorolÃ³gicos guardados en {archivo_destino}")
-
-    except Exception as e:
-        print(f"OcurriÃ³ un error al procesar el archivo de datos: {e}")
-
-    finally:
-        if wb:
-            wb.Close(False)
-        excel.Quit()
-
-def menu_principal(config, plantilla, api_settings):
-    """FunciÃ³n principal del menÃº para procesar datos meteorolÃ³gicos."""
-    latitud, longitud = 37.3891, -5.9845
-
-    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud, api_settings)
-    if not fechas_disponibles:
-        print(traducciones["no_dates_found"])
-        input("Presione Enter para continuar...")
-        return
-
-    while True:
-        print("\n--- " + traducciones["main_menu"] + " ---")
-        print("1. " + traducciones["process_data"])
-        print("2. " + traducciones["exit"])
-        opcion = input(traducciones["select_option"])
-
-        if opcion == '1':
-            print("\n" + traducciones["available_dates"])
-            for i, fecha in enumerate(fechas_disponibles, start=1):
-                print(f"{i}. {fecha}")
-
-            while True:
-                try:
-                    seleccion_fecha = int(input(traducciones["select_date_option"])) - 1
-                    if 0 <= seleccion_fecha < len(fechas_disponibles):
-                        fecha = datetime.strptime(fechas_disponibles[seleccion_fecha], '%Y-%m-%d')
-                        break
-                    else:
-                        print(traducciones["invalid_selection"])
-                except ValueError:
-                    print(traducciones["invalid_input"])
-
-            # AÃ±adir 'traducciones' en la llamada
-            comunidad = seleccionar_comunidad(config, traducciones)
-            if comunidad is None:
-                print("No se seleccionÃ³ ninguna comunidad.")
-                continue
-
-            procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings)
-
-            input("Procesamiento completado. Presione Enter para ver los resultados...")
-
-        elif opcion == '2':
-            print(traducciones["exiting"])
-            break
+        url = (f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}"
+               f"&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}")
+        
+        response = requests.get(url)
+        if response.status_code == 200:
+            datos = response.json()
+            if fecha_str in datos['daily']['time']:
+                index = datos['daily']['time'].index(fecha_str)
+                return {param: datos['daily'][param][index] for param in api_settings['daily_params']}
+            else:
+                print(f"No se encontraron datos para la fecha {fecha_str}")
         else:
-            print(traducciones["invalid_selection"])
-            input("Presione Enter para continuar...")
-
-# Cargar configuraciÃ³n y ejecutar menÃº principal
-config_path = os.path.join(project_root, 'config', 'config.json')
-config = cargar_configuracion(config_path)
-traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(project_root, 'locales'))
-data_dir = config.get("data_directory", "data")
-inicializar_directorios(data_dir)
-
-# Usa la ruta del TEMPLATE_PATH del archivo .env, o una ruta absoluta por defecto
-plantilla = os.getenv("TEMPLATE_PATH", os.path.join(project_root, "config", "templates", "MeteoData_Template.xlsm"))
-api_settings = config.get("api_settings", {})
-
-# Llamar a la funciÃ³n principal
-menu_principal(config, plantilla, api_settings)
+            print(f"Error al obtener datos para la fecha {fecha_str}: {response.status_code}")
+        return None    
+
+    def copiar_plantilla(fecha):
+        """Copia la plantilla si no existe un archivo de datos para la fecha dada."""
+        # Asegurarse de que la ruta de la plantilla es correcta
+        if not os.path.exists(plantilla):
+            print(f"Error: La plantilla no se encuentra en la ruta especificada: {plantilla}")
+            return None
+
+        archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha.strftime('%Y%m%d')}.xlsm")
+        if os.path.exists(archivo_destino):
+            print(f"{traducciones['file_exists']} {archivo_destino}")
+            return archivo_destino
+
+        try:
+            # Usar DispatchEx para iniciar una nueva instancia de Excel
+            excel = win32.DispatchEx("Excel.Application")
+            workbook = excel.Workbooks.Open(plantilla)
+            workbook.SaveAs(archivo_destino, FileFormat=52)
+            workbook.Close(False)
+            print(f"{traducciones['template_copied']} {archivo_destino}")
+            return archivo_destino
+        except Exception as e:
+            print(f"{traducciones['error_copy_template']}: {e}")
+            return None
+        finally:
+            try:
+                excel.Quit()  # AsegÃºrate de cerrar Excel correctamente
+            except Exception as e:
+                print(f"Error al cerrar Excel: {e}")
+
+    def listar_fechas_disponibles(comunidad, latitud, longitud):
+        """Lista las fechas disponibles desde la API y verifica si estÃ¡n completas o incompletas en los archivos locales."""
+        fechas_api = obtener_fechas_disponibles_api(latitud, longitud)
+        if not fechas_api:
+            print(traducciones["no_dates_found"])
+            return []
+
+        fechas_disponibles = []
+        for fecha_str in fechas_api:
+            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
+            archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha.strftime('%Y%m%d')}.xlsm")
+            
+            if os.path.exists(archivo_destino):
+                ultima_actualizacion = datetime.fromtimestamp(os.path.getmtime(archivo_destino)).strftime('%Y-%m-%d %H:%M:%S')
+                datos_completos = verificar_datos_completos(archivo_destino, comunidad)
+                estado = "Completa" if datos_completos else "Incompleta"
+            else:
+                ultima_actualizacion = "No disponible"
+                estado = "Incompleta"
+
+            fechas_disponibles.append((fecha, ultima_actualizacion, estado))
+
+        return sorted(fechas_disponibles, key=lambda x: x[0])
+
+    def verificar_datos_completos(archivo, comunidad):
+        """Verifica si la hoja de la comunidad tiene datos completos."""
+        excel = None
+        workbook = None
+        try:
+            excel = win32.DispatchEx("Excel.Application")
+            workbook = excel.Workbooks.Open(archivo)
+            ws = workbook.Sheets(comunidad)
+            datos_completos = all(ws.Cells(row, 8).Value for row in range(2, ws.UsedRange.Rows.Count + 1))
+            return datos_completos
+        except Exception as e:
+            print(f"Error al verificar datos: {e}")
+            return False
+        finally:
+            if workbook:
+                workbook.Close(False)
+            if excel:
+                try:
+                    excel.Quit()
+                except Exception as e:
+                    print("Error al cerrar Excel:", e)
+
+    def procesar_datos(fecha, comunidad):
+        archivo_destino = copiar_plantilla(fecha)
+        if not archivo_destino:
+            return
+
+        excel = win32.DispatchEx("Excel.Application")
+        try:
+            workbook = excel.Workbooks.Open(archivo_destino)
+            ws = workbook.Sheets(comunidad)
+            for row in range(2, ws.UsedRange.Rows.Count + 1):
+                coordenadas = ws.Cells(row, 3).Value
+                if coordenadas:
+                    latitud, longitud = map(float, coordenadas.split(', '))
+                    datos = obtener_datos_meteo(latitud, longitud, fecha)
+                    if datos:
+                        for i, param in enumerate(api_settings['daily_params'], start=8):
+                            ws.Cells(row, i).Value = datos[param]
+                        ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
+            workbook.Save()
+            print(f"Datos meteorolÃ³gicos guardados en {archivo_destino}")
+        except Exception as e:
+            print(f"Error al procesar el archivo de datos: {e}")
+        finally:
+            if workbook:
+                workbook.Close(False)
+            if excel:
+                try:
+                    excel.Quit()
+                except Exception as e:
+                    print("Error al cerrar Excel:", e)
+
+    def mostrar_comunidades(comunidades):
+        print("\n--- Comunidades AutÃ³nomas disponibles ---")
+        for i, comunidad in enumerate(comunidades, start=1):
+            print(f"{i}. {comunidad}")
+
+    def menu_principal():
+        comunidades = config.get("comunidades", [])
+        mostrar_comunidades(comunidades)
+        
+        while True:
+            try:
+                seleccion_comunidad = int(input(traducciones["select_community_option"])) - 1
+                if 0 <= seleccion_comunidad < len(comunidades):
+                    comunidad = comunidades[seleccion_comunidad]
+                    break
+                else:
+                    print(traducciones["selection_out_of_range"])
+            except ValueError:
+                print(traducciones["invalid_input"])
+
+        latitud, longitud = 37.3891, -5.9845  # Coordenadas de ejemplo
+        fechas_disponibles = listar_fechas_disponibles(comunidad, latitud, longitud)
+        if not fechas_disponibles:
+            print(traducciones["no_dates_found"])
+            return
+
+        print(traducciones["select_date_option"])
+        for i, (fecha, ultima_actualizacion, estado) in enumerate(fechas_disponibles, start=1):
+            print(f"{i}. {fecha.strftime('%Y-%m-%d')} - Ãšltima actualizaciÃ³n: {ultima_actualizacion} - Estado: {estado}")
+
+        while True:
+            try:
+                seleccion_fecha = int(input(traducciones["select_date_option"])) - 1
+                if 0 <= seleccion_fecha < len(fechas_disponibles):
+                    fecha = fechas_disponibles[seleccion_fecha][0]
+                    break
+                else:
+                    print(traducciones["selection_out_of_range"])
+            except ValueError:
+                print(traducciones["invalid_input"])
+
+        procesar_datos(fecha, comunidad)
+
+    # Ejecutar el menÃº principal
+    menu_principal()
+
+if __name__ == "__main__":
+    load_dotenv()  # Carga las variables del .env
+    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
+    config_path = os.path.join(project_root, 'config', 'config.json')
+    config = cargar_configuracion(config_path)
+    traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(project_root, 'locales'))
+    
+    main(config, traducciones)
diff --git a/src/utils/utils.py b/src/utils/utils.py
index 9895612..80836fe 100644
--- a/src/utils/utils.py
+++ b/src/utils/utils.py
@@ -1,23 +1,26 @@
+# utils.py
 import os
 import json
-import time
 import pandas as pd
 import geopandas as gpd
-import shutil
-import requests
 from dotenv import load_dotenv
-from datetime import datetime
-import win32com.client as win32
 
 # Cargar variables de entorno
 load_dotenv()
 
+def obtener_rutas():
+    """Devuelve las rutas principales del proyecto."""
+    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
+    config_path = os.path.join(project_root, 'config', 'config.json')
+    return project_root, config_path
+
 def cls():
     """Limpia la pantalla."""
     os.system('cls' if os.name == 'nt' else 'clear')
 
 def cargar_configuracion(config_path):
     """Carga la configuraciÃ³n desde el archivo JSON especificado."""
+    print("Ruta recibida para config_path en cargar_configuracion:", config_path)  # AÃ±adir para depuraciÃ³n
     try:
         with open(config_path, "r", encoding="utf-8") as file:
             return json.load(file)
@@ -28,170 +31,51 @@ def cargar_configuracion(config_path):
         print("Error: El archivo de configuraciÃ³n tiene un formato JSON no vÃ¡lido.")
         exit()
 
-def cargar_traducciones(idioma, locales_dir):
+def cargar_traducciones(idioma="es"):
     """Carga el archivo de traducciones en el idioma especificado."""
+    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
+    locales_dir = os.path.join(project_root, 'locales')
     idioma_path = os.path.join(locales_dir, f"{idioma}.json")
+
     try:
         with open(idioma_path, 'r', encoding='utf-8') as f:
             return json.load(f)
     except FileNotFoundError:
-        print(f"Archivo de idioma '{idioma}.json' no encontrado. Usando idioma predeterminado (espaÃ±ol).")
-        with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
-            return json.load(f)
+        print(f"Traducciones para '{idioma}' no encontradas en {idioma_path}. Usando espaÃ±ol por defecto.")
+        return {}  # Retorna un diccionario vacÃ­o o uno predeterminado para evitar mÃ¡s errores
 
 def inicializar_directorios(data_dir):
     """Inicializa el directorio de almacenamiento de datos."""
     os.makedirs(data_dir, exist_ok=True)
 
-def listar_archivos_disponibles(data_dir, traducciones):
-    """Lista archivos en el directorio especificado que cumplen con el formato de nombre."""
+def listar_archivos_disponibles(data_dir, traducciones, imprimir=True):
+    """Lista los archivos disponibles en el directorio de datos y permite seleccionar uno."""
     directorio_completo = os.path.abspath(data_dir)
-    print(f"Buscando archivos en: {directorio_completo}")
-    
     archivos = []
+
     for root, dirs, files in os.walk(directorio_completo):
         for file in files:
-            if file.startswith("MeteoData_") and file.endswith((".xlsx", ".xlsm")):
+            if file.startswith("MeteoData_") and (file.endswith(".xlsx") or file.endswith(".xlsm")):
                 archivos.append(os.path.join(root, file))
 
     if not archivos:
         print(traducciones["no_files_available"])
         return None
-    
-    print(traducciones["available_files"])
-    for i, archivo in enumerate(archivos, start=1):
-        print(f"{i}. {os.path.basename(archivo)}")
-    
-    while True:
-        try:
-            seleccion = int(input(traducciones["select_file"])) - 1
-            if 0 <= seleccion < len(archivos):
-                return archivos[seleccion]
-            else:
-                print(traducciones["selection_out_of_range"])
-        except ValueError:
-            print(traducciones["invalid_input"])
 
-def cargar_excel(archivo_seleccionado):
-    """Carga un archivo Excel y retorna sus hojas disponibles."""
-    try:
-        excel_file = pd.ExcelFile(archivo_seleccionado)
-        hojas_disponibles = excel_file.sheet_names
-        return excel_file, hojas_disponibles
-    except FileNotFoundError:
-        print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
-        return None, []
+    if imprimir:  # Solo imprime si 'imprimir' es True
+        print(traducciones["available_files"])
+        for i, archivo in enumerate(archivos, start=1):
+            print(f"{i}. {os.path.basename(archivo)}")
+    
+    return archivos
 
 def cargar_shapefile(shapefile_path, traducciones):
-    """Carga un archivo shapefile y retorna el objeto GeoDataFrame."""
+    """Carga un shapefile en un GeoDataFrame."""
     if not os.path.exists(shapefile_path):
-        print(f"Error: No se encontrÃ³ el archivo de shapes en '{shapefile_path}'.")
+        print(f"{traducciones['shapefile_not_found']} {shapefile_path}")
         exit()
     try:
         return gpd.read_file(shapefile_path)
     except Exception as e:
-        print(traducciones["error_loading_shapefile"])
-        print(f"Detalles del error: {e}")
+        print(traducciones["error_loading_shapefile"], e)
         exit()
-
-def copiar_plantilla_si_no_existe(fecha, plantilla, data_dir):
-    """Copia la plantilla a la ubicaciÃ³n de destino solo si el archivo no existe."""
-    fecha_str = fecha.strftime('%Y%m%d')
-    archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha_str}.xlsm")
-
-    # Si el archivo de destino ya existe, no lo sobrescribimos
-    if os.path.exists(archivo_destino):
-        print(f"Archivo ya existente: {archivo_destino}. No se crearÃ¡ una nueva copia.")
-        return archivo_destino
-
-    archivo_temp = os.path.join(os.getenv('TEMP'), f"MeteoData_{fecha_str}_temp.xlsm")
-    excel = win32.Dispatch("Excel.Application")
-    excel.Visible = False
-
-    try:
-        # Verificar si la plantilla existe
-        if not os.path.exists(plantilla):
-            print(f"Error: La plantilla {plantilla} no se encuentra.")
-            return None
-
-        workbook = excel.Workbooks.Open(plantilla)
-        workbook.SaveAs(archivo_temp, FileFormat=52)  # 52 es el formato para .xlsm
-        workbook.Close(False)
-
-        # Mover la copia temporal al destino final
-        os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)
-        shutil.move(archivo_temp, archivo_destino)
-        
-        print(f"Copia de la plantilla creada en: {archivo_destino}")
-        return archivo_destino
-    except Exception as e:
-        print(f"OcurriÃ³ un error al copiar la plantilla: {e}")
-        return None
-    finally:
-        excel.Quit()
-
-def obtener_fechas_disponibles_api(latitud, longitud, api_settings):
-    """Obtiene las fechas disponibles desde la API de Open-Meteo utilizando la configuraciÃ³n de API."""
-    url = f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}"
-    for intento in range(5):  # MÃ¡ximo 5 reintentos
-        response = requests.get(url)
-        if response.status_code == 200:
-            return response.json().get('daily', {}).get('time', [])
-        elif response.status_code == 429:
-            print("Demasiadas solicitudes. Esperando para reintentar...")
-            time.sleep(5)
-        else:
-            print(f"Error en la solicitud. CÃ³digo de estado: {response.status_code}")
-            input("Presione Enter para continuar...")
-            return []
-    print("Se alcanzÃ³ el nÃºmero mÃ¡ximo de reintentos.")
-    input("Presione Enter para continuar...")
-    return []
-
-def obtener_datos_meteo(latitud, longitud, fecha, api_settings):
-    """Obtiene los datos meteorolÃ³gicos de la API para la fecha y coordenadas especificadas."""
-    fecha_str = fecha.strftime('%Y-%m-%d')
-    url = (f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}"
-           f"&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}")
-    response = requests.get(url)
-    if response.status_code == 200:
-        datos = response.json()
-        if fecha_str in datos['daily']['time']:
-            index = datos['daily']['time'].index(fecha_str)
-            return {
-                'temperature_min': datos['daily']['temperature_2m_min'][index],
-                'temperature_max': datos['daily']['temperature_2m_max'][index],
-                'windspeed_max': datos['daily']['windspeed_10m_max'][index],
-                'windgusts_max': datos['daily']['windgusts_10m_max'][index],
-                'winddirection_dominant': datos['daily']['winddirection_10m_dominant'][index],
-                'precipitation_sum': datos['daily']['precipitation_sum'][index]
-            }
-        else:
-            print(f"Datos no disponibles para la fecha: {fecha_str}")
-            return None
-    else:
-        print(f"Error en la solicitud. CÃ³digo de estado: {response.status_code}")
-        input("Presione Enter para continuar...")
-        return None
-
-def seleccionar_comunidad(config, traducciones):
-    """Permite seleccionar una comunidad autÃ³noma a partir de la configuraciÃ³n."""
-    comunidades = config.get("comunidades", [])
-    if not comunidades:
-        print(traducciones["no_communities_found"])
-        input("Presione Enter para continuar...")
-        return None
-
-    print(traducciones["select_community"])
-    for i, comunidad in enumerate(comunidades, start=1):
-        print(f"{i}. {comunidad}")
-
-    while True:
-        try:
-            seleccion = int(input(traducciones["select_community_option"])) - 1
-            if 0 <= seleccion < len(comunidades):
-                return comunidades[seleccion]
-            else:
-                print(traducciones["invalid_selection"])
-        except ValueError:
-            print(traducciones["invalid_input"])
diff --git a/src/visualization/geoPy.py b/src/visualization/geoPy.py
index f52c566..ae6d8c5 100644
--- a/src/visualization/geoPy.py
+++ b/src/visualization/geoPy.py
@@ -1,283 +1,238 @@
 import os
-import json
 import pandas as pd
 import geopandas as gpd
 import matplotlib.pyplot as plt
 from matplotlib.colors import Normalize
 from matplotlib.widgets import Button
-from datetime import datetime
-
-def cls():
-    """Limpia la consola."""
-    os.system('cls' if os.name == 'nt' else 'clear')
-
-# Cargar configuraciÃ³n desde archivo JSON
-def cargar_configuracion():
-    """Carga la configuraciÃ³n desde el archivo config.json."""
-    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
+from utils.utils import cargar_configuracion, cargar_traducciones, cargar_shapefile, listar_archivos_disponibles
+
+def main(config=None, traducciones=None):
+    # Cargar configuraciÃ³n y traducciones si no se proporcionan como argumentos
+    if config is None:
+        config = cargar_configuracion()
+    if traducciones is None:
+        traducciones = cargar_traducciones(config.get("language", "es"))
+
+    # ConfiguraciÃ³n de variables
+    label_threshold = config.get("label_threshold", 400)
+    min_point_size = config.get("min_point_size", 5)
+    max_point_size = config.get("max_point_size", 500)
+    data_dir = os.path.abspath(config.get("data_directory", "data"))
+    shapefile_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'shp', 'gadm41_ESP_4.shp'))
+
+    # Unidad de medida
+    global unit_dict
+    unit_dict = {
+        "temperature_min": "Â°C",
+        "temperature_max": "Â°C",
+        "wind_gusts": "km/h",
+        "wind_speed": "km/h",
+        "precipitation_sum": "mm"
+    }
+
+    # Cargar shapefile
     try:
-        with open(config_path, "r", encoding="utf-8") as file:
-            return json.load(file)
-    except FileNotFoundError:
-        print("Error: El archivo config.json no se encuentra en la ruta especificada.")
-        exit()
-    except json.JSONDecodeError:
-        print("Error: El archivo config.json tiene un formato JSON no vÃ¡lido.")
-        exit()
-
-def cargar_traducciones(idioma="es"):
-    """Carga el archivo de traducciones en el idioma especificado."""
-    locales_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'locales')
-    idioma_path = os.path.join(locales_dir, f"{idioma}.json")
+        espana_shapefile = cargar_shapefile(shapefile_path, traducciones)
+    except Exception as e:
+        print(f"Error al cargar el shapefile: {e}")
+        return
+
+    # Listar archivos disponibles
+    archivo_seleccionado = listar_archivos_disponibles(data_dir, traducciones, imprimir=False)
+    if archivo_seleccionado is None or len(archivo_seleccionado) == 0:
+        print("No se encontraron archivos vÃ¡lidos.")
+        return
+
+    # SelecciÃ³n del archivo
+    if len(archivo_seleccionado) > 1:
+        print("Archivos disponibles:")
+        for i, archivo in enumerate(archivo_seleccionado, start=1):
+            print(f"{i}. {os.path.basename(archivo)}")
+        
+        while True:
+            try:
+                seleccion_archivo = int(input("Selecciona el nÃºmero del archivo a utilizar: ")) - 1
+                if 0 <= seleccion_archivo < len(archivo_seleccionado):
+                    archivo_seleccionado = archivo_seleccionado[seleccion_archivo]
+                    break
+                else:
+                    print("SelecciÃ³n fuera de rango.")
+            except ValueError:
+                print("Entrada invÃ¡lida.")
+    else:
+        archivo_seleccionado = archivo_seleccionado[0]
+
+    print(f"Archivo seleccionado: {archivo_seleccionado}")
+
     try:
-        with open(idioma_path, 'r', encoding='utf-8') as f:
-            return json.load(f)
+        excel_file = pd.ExcelFile(archivo_seleccionado)
+        hojas_disponibles = excel_file.sheet_names
     except FileNotFoundError:
-        print(f"Archivo de idioma '{idioma}.json' no encontrado. Usando idioma predeterminado (espaÃ±ol).")
-        with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
-            return json.load(f)
-
-# Inicializar parÃ¡metros desde la configuraciÃ³n
-config = cargar_configuracion()
-traducciones = cargar_traducciones(config.get("language", "es"))
-
-# Variables de configuraciÃ³n
-label_threshold = config.get("label_threshold", 400)
-min_point_size = config.get("min_point_size", 5)
-max_point_size = config.get("max_point_size", 500)
-data_dir = config.get("data_directory", "data")
-shapefile_path = config.get("shapefile_path", "config/shp/gadm41_ESP_4.shp")
-
-# Unidad de medida para cada tipo de dato
-unit_dict = {
-    "temperature_min": "Â°C",
-    "temperature_max": "Â°C",
-    "wind_gusts": "km/h",
-    "wind_speed": "km/h",
-    "precipitation_sum": "mm"
-}
-
-# Verificar si el archivo shapefile existe
-if not os.path.exists(shapefile_path):
-    print(f"Error: No se encontrÃ³ el archivo de shapes en '{shapefile_path}'.")
-    exit()
-
-# Cargar el shapefile de EspaÃ±a
-try:
-    espana_shapefile = gpd.read_file(shapefile_path)
-except Exception as e:
-    print(traducciones["error_loading_shapefile"])
-    print(f"Detalles del error: {e}")
-    exit()
-
-# FunciÃ³n para listar archivos disponibles en el directorio de datos
-def listar_archivos_disponibles():
-    directorio_completo = os.path.abspath(data_dir)
-    print(f"Buscando archivos en: {directorio_completo}")
-    
-    archivos = []
-    
-    for root, dirs, files in os.walk(directorio_completo):
-        for file in files:
-            if file.startswith("MeteoData_") and (file.endswith(".xlsx") or file.endswith(".xlsm")):
-                archivos.append(os.path.join(root, file))
-
-    if not archivos:
-        print(traducciones["no_files_available"])
-        return None
-    
-    print(traducciones["available_files"])
-    for i, archivo in enumerate(archivos, start=1):
-        print(f"{i}. {os.path.basename(archivo)}")
-    
+        print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
+        return
+    except Exception as e:
+        print(f"Error al abrir el archivo Excel: {e}")
+        return
+
+    # Verificar quÃ© comunidades tienen datos en las hojas
+    comunidades = {
+        "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'AndalucÃ­a'],
+        "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']
+    }
+
+    comunidades_con_datos = []
+    for hoja in hojas_disponibles:
+        df = pd.read_excel(archivo_seleccionado, sheet_name=hoja)
+        if not df.empty and df.iloc[:, 7:11].count().sum() > 0:
+            comunidades_con_datos.append(hoja)
+
+    comunidades = {k: v for k, v in comunidades.items() if k in comunidades_con_datos}
+
+    if not comunidades:
+        print("No hay comunidades con datos disponibles.")
+        return
+
+    print(traducciones["available_autonomous_communities"])
+    for i, comunidad in enumerate(comunidades.keys(), start=1):
+        print(f"{i}. {comunidad}")
+
+    # SelecciÃ³n de comunidad
     while True:
         try:
-            seleccion = int(input(traducciones["select_file"])) - 1
-            if 0 <= seleccion < len(archivos):
-                return archivos[seleccion]
+            seleccion_hoja = int(input(traducciones["select_community"])) - 1
+            if 0 <= seleccion_hoja < len(comunidades):
+                sheet_name = list(comunidades.keys())[seleccion_hoja]
+                break
             else:
                 print(traducciones["selection_out_of_range"])
         except ValueError:
             print(traducciones["invalid_input"])
 
-# Cargar el archivo Excel seleccionado y listar las hojas disponibles
-archivo_seleccionado = listar_archivos_disponibles()
-if archivo_seleccionado is None:
-    exit()
-
-try:
-    excel_file = pd.ExcelFile(archivo_seleccionado)
-    hojas_disponibles = excel_file.sheet_names
-except FileNotFoundError:
-    print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
-    exit()
-
-# Filtrar las comunidades autÃ³nomas que tienen datos disponibles
-comunidades_con_datos = []
-comunidades = { 
-    "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'AndalucÃ­a'],
-    "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']
-}
-
-for hoja in hojas_disponibles:
-    df = pd.read_excel(archivo_seleccionado, sheet_name=hoja)
-    
-    # Verificar que el DataFrame no estÃ© vacÃ­o y que contenga datos en las columnas correspondientes
-    # Usamos los Ã­ndices de columna 7 a 10 (equivalente a H, I, J, K en Excel)
-    if not df.empty and df.iloc[:, 7:11].count().sum() > 0:
-        comunidades_con_datos.append(hoja)
-
-# Filtrar las comunidades segÃºn los datos disponibles
-comunidades = {k: v for k, v in comunidades.items() if k in comunidades_con_datos}
-
-print(traducciones["available_autonomous_communities"])
-for i, comunidad in enumerate(comunidades.keys(), start=1):
-    print(f"{i}. {comunidad}")
-
-# Permitir que el usuario seleccione la hoja (comunidad autÃ³noma)
-while True:
+    df = pd.read_excel(archivo_seleccionado, sheet_name=sheet_name)
+
     try:
-        seleccion_hoja = int(input(traducciones["select_community"])) - 1
-        if 0 <= seleccion_hoja < len(comunidades):
-            sheet_name = list(comunidades.keys())[seleccion_hoja]
-            break
-        else:
-            print(traducciones["selection_out_of_range"])
-    except ValueError:
-        print(traducciones["invalid_input"])
-
-# Cargar los datos desde la hoja seleccionada
-df = pd.read_excel(archivo_seleccionado, sheet_name=sheet_name)
-
-# AsegÃºrate de que las columnas de coordenadas estÃ¡n en el formato correcto
-df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(', ', expand=True).astype(float)
-
-# Seleccionar la regiÃ³n en el mapa segÃºn la comunidad seleccionada
-region_map = comunidades.get(sheet_name.upper(), None)
-if region_map is None or region_map.empty:
-    print(f"Error: No se encontrÃ³ la regiÃ³n correspondiente para '{sheet_name}' en el shapefile.")
-    exit()
-
-# Crear la figura y grÃ¡ficos de datos meteorolÃ³gicos
-fig, ax1 = plt.subplots(figsize=(10, 8))
-fig.canvas.manager.set_window_title(f"Mapa de {sheet_name} - Datos MeteorolÃ³gicos")
-
-# Variable global para almacenar la selecciÃ³n actual
-selected_data = 'temperature_min'
-
-scatter_points = []
-name_points = [(row['Name'], row['Longitude'], row['Latitude'], label_threshold, None, None) for _, row in df.iterrows()]
-
-# FunciÃ³n de actualizaciÃ³n para el grÃ¡fico
-def update_scatter():
-    global min_point_size, max_point_size
-    ax1.clear()
-    region_map.boundary.plot(ax=ax1, linewidth=0.5, color='lightgray')
-
-    ax1.set_xlabel('Longitud')
-    ax1.set_ylabel('Latitud')
-    
-    if selected_data == 'temperature_min':
-        data = df['Min Temperature']
-        title = traducciones["temperature_min_title"]
-        cmap = 'Blues'
-    elif selected_data == 'temperature_max':
-        data = df['Max Temperature']
-        title = traducciones["temperature_max_title"]
-        cmap = 'Reds'
-    elif selected_data == 'wind_gusts':
-        data = df['Maximum wind gusts']
-        title = traducciones["wind_gusts_title"]
-        cmap = 'Purples'
-    elif selected_data == 'wind_speed':
-        data = df['Maximum wind speed']
-        title = traducciones["wind_speed_title"]
-        cmap = 'Greens'
-    elif selected_data == 'precipitation_sum':
-        data = df['Precipitation']
-        title = traducciones["precipitation_sum_title"]
-        cmap = 'Blues'
-
-    norm = Normalize(vmin=data.min(), vmax=data.max())
-    scatter_points.clear()
-    
-    for i, row in df.iterrows():
-        if pd.isnull(data[i]):
-            continue
-        
-        current_data = data[i]
-        color = plt.get_cmap(cmap)(norm(current_data))
-        
-        point_size = min_point_size + (max_point_size - min_point_size) * (current_data - data.min()) / (data.max() - data.min())
-
-        scatter = ax1.scatter(row['Longitude'], row['Latitude'], color=color, s=point_size, alpha=0.7)
-        scatter_points.append((scatter, point_size))
-        name_points[i] = (row['Name'], row['Longitude'], row['Latitude'], label_threshold, point_size, current_data)
-    
-    ax1.set_title(f'{sheet_name} - {title}')
-    update_labels()
-    fig.canvas.draw_idle()
-
-# FunciÃ³n para actualizar etiquetas de nombres
-def update_labels():
-    for label in ax1.texts:
-        label.remove()
-    
-    for locality, lon, lat, threshold, size, value in name_points:
-        if size and size >= threshold:
-            ax1.text(lon, lat, locality, fontsize=8, ha='center', va='bottom', alpha=0.8)
-
-fig.canvas.mpl_connect('draw_event', lambda event: update_labels())
-
-# Conectar el evento de movimiento del ratÃ³n
-def on_mouse_move(event):
-    global last_locality  # Hacer que la variable sea global
-    if event.inaxes == ax1:
-        for locality, lon, lat, threshold, size, value in name_points:
-            distance = ((event.xdata - lon) ** 2 + (event.ydata - lat) ** 2) ** 0.5
-            if distance < 0.2:
-                # Solo mostrar la informaciÃ³n si es un nuevo punto
-                if locality != last_locality:
-                    print(f'{locality}: {value} {unit_dict[selected_data]}')  # Muestra el valor en la consola
-                    last_locality = locality  # Actualiza el Ãºltimo punto mostrado
-                break
-        else:
-            # Reiniciar el Ãºltimo punto si no se estÃ¡ sobre ningÃºn punto
-            last_locality = None
+        df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(', ', expand=True).astype(float)
+    except Exception as e:
+        print(f"Error al procesar las coordenadas: {e}")
+        return
 
-# Conectar el evento de movimiento del ratÃ³n
-fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
+    region_map = comunidades.get(sheet_name.upper(), None)
+    if region_map is None or region_map.empty:
+        print(f"Error: No se encontrÃ³ la regiÃ³n correspondiente para '{sheet_name}' en el shapefile.")
+        return
+
+    # Crear la figura y grÃ¡ficos
+    fig, ax1 = plt.subplots(figsize=(10, 8))
+    fig.canvas.manager.set_window_title(f"Mapa de {sheet_name} - Datos MeteorolÃ³gicos")
 
-# FunciÃ³n para establecer los datos seleccionados
-def set_selected_data(data_type):
     global selected_data
-    selected_data = data_type
-    update_scatter()  # Actualiza el grÃ¡fico con los nuevos datos
+    selected_data = 'temperature_min'
+    global last_locality
+    last_locality = None
+
+    scatter_points = []
+    name_points = [(row['Name'], row['Longitude'], row['Latitude'], label_threshold, None, None) for _, row in df.iterrows()]
+
+    def update_scatter():
+        ax1.clear()
+        region_map.boundary.plot(ax=ax1, linewidth=0.5, color='lightgray')
+        ax1.set_xlabel('Longitud')
+        ax1.set_ylabel('Latitud')
+
+        data, title, cmap = get_plot_data(selected_data, df, traducciones)
+
+        if data.isnull().all():
+            print(f"No hay datos disponibles para {title}.")
+            ax1.set_title(f"No hay datos para {title}.")
+            fig.canvas.draw_idle()
+            return
+
+        norm = Normalize(vmin=data.min(), vmax=data.max())
+        scatter_points.clear()
+
+        for i, row in df.iterrows():
+            if pd.isnull(data[i]):
+                continue
+
+            current_data = data[i]
+            color = plt.get_cmap(cmap)(norm(current_data))
+            point_size = min_point_size + (max_point_size - min_point_size) * (current_data - data.min()) / (data.max() - data.min())
+
+            scatter = ax1.scatter(row['Longitude'], row['Latitude'], color=color, s=point_size, alpha=0.7)
+            scatter_points.append((scatter, point_size))
+            name_points[i] = (row['Name'], row['Longitude'], row['Latitude'], label_threshold, point_size, current_data)
+
+        ax1.set_title(f'{sheet_name} - {title}')
+        update_labels()
+        fig.canvas.draw_idle()
+
+    def get_plot_data(selected_data, df, traducciones):
+        if selected_data == 'temperature_min':
+            return df['Min Temperature'], traducciones["temperature_min_title"], 'Blues'
+        elif selected_data == 'temperature_max':
+            return df['Max Temperature'], traducciones["temperature_max_title"], 'Reds'
+        elif selected_data == 'wind_gusts':
+            return df['Maximum wind gusts'], traducciones["wind_gusts_title"], 'Purples'
+        elif selected_data == 'wind_speed':
+            return df['Maximum wind speed'], traducciones["wind_speed_title"], 'Greens'
+        elif selected_data == 'precipitation_sum':
+            return df['Precipitation'], traducciones["precipitation_sum_title"], 'Blues'
+
+    def update_labels():
+        for label in ax1.texts:
+            label.remove()
+
+        for locality, lon, lat, threshold, size, value in name_points:
+            if size and size >= threshold:
+                ax1.text(lon, lat, locality, fontsize=8, ha='center', va='bottom', alpha=0.8)
+
+    fig.canvas.mpl_connect('draw_event', lambda event: update_labels())
+
+    def on_mouse_move(event):
+        global last_locality
+        if event.inaxes == ax1:
+            for locality, lon, lat, threshold, size, value in name_points:
+                distance = ((event.xdata - lon) ** 2 + (event.ydata - lat) ** 2) ** 0.5
+                if distance < 0.2:
+                    if locality != last_locality:
+                        print(f'{locality}: {value} {unit_dict[selected_data]}')
+                        last_locality = locality
+                    break
+            else:
+                last_locality = None
+
+    fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
+
+    def set_selected_data(data_type):
+        print(f"BotÃ³n clicado: {data_type}")
+        global selected_data
+        selected_data = data_type
+        update_scatter()
 
-# Botones para seleccionar cada tipo de dato
-button_width = 0.12
-button_height = 0.05
+    create_buttons(fig, traducciones, set_selected_data)
 
-ax_button_min = plt.axes([0.1, 0.01, button_width, button_height])
-btn_min = Button(ax_button_min, traducciones["temp_min_button"])  # Usar traducciÃ³n
-btn_min.on_clicked(lambda event: set_selected_data('temperature_min'))
+    update_scatter()
+    plt.show(block=True)
 
-ax_button_max = plt.axes([0.24, 0.01, button_width, button_height])
-btn_max = Button(ax_button_max, traducciones["temp_max_button"])  # Usar traducciÃ³n
-btn_max.on_clicked(lambda event: set_selected_data('temperature_max'))
+# Botones de selecciÃ³n de datos
+global_buttons = []
 
-ax_button_gusts = plt.axes([0.38, 0.01, button_width, button_height])
-btn_gusts = Button(ax_button_gusts, traducciones["wind_gusts_button"])  # Usar traducciÃ³n
-btn_gusts.on_clicked(lambda event: set_selected_data('wind_gusts'))
+def create_buttons(fig, traducciones, set_selected_data):
+    button_width = 0.12
+    button_height = 0.05
 
-ax_button_speed = plt.axes([0.52, 0.01, button_width, button_height])
-btn_speed = Button(ax_button_speed, traducciones["wind_speed_button"])  # Usar traducciÃ³n
-btn_speed.on_clicked(lambda event: set_selected_data('wind_speed'))
+    def on_button_click(data_type):
+        print(f"Clicked button for: {data_type}")
+        set_selected_data(data_type)
 
-ax_button_precip = plt.axes([0.66, 0.01, button_width, button_height])
-btn_precip = Button(ax_button_precip, traducciones["precipitation_sum_button"])  # Usar traducciÃ³n
-btn_precip.on_clicked(lambda event: set_selected_data('precipitation_sum'))
+    data_types = ['temperature_min', 'temperature_max', 'wind_gusts', 'wind_speed', 'precipitation_sum']
+    positions = [0.1, 0.24, 0.38, 0.52, 0.66]
+    for data_type, pos in zip(data_types, positions):
+        ax_button = plt.axes([pos, 0.01, button_width, button_height])
+        # LÃ­nea modificada para aplicar traducciones
+        btn = Button(ax_button, traducciones.get(f"{data_type}_button", data_type))
+        btn.on_clicked(lambda event, dt=data_type: on_button_click(dt))
+        global_buttons.append(btn)
 
-# ConfiguraciÃ³n de lÃ­mites originales y dibujar el grÃ¡fico inicial
-update_scatter()
-plt.show()
+if __name__ == "__main__":
+    main()


Commit Message: Changelog
Changes:
diff --git a/bin/scripts/generate_changelog.py b/bin/scripts/generate_changelog.py
index bbf8d46..8f9fa28 100644
--- a/bin/scripts/generate_changelog.py
+++ b/bin/scripts/generate_changelog.py
@@ -1,36 +1,22 @@
 import subprocess
-import os
 from datetime import date
-from dotenv import load_dotenv
-import openai
-import time
-
-# Cargar la API Key de OpenAI
-load_dotenv()
-openai.api_key = os.getenv("OPENAI_API_KEY")
+import os
 
 print("Iniciando la generaciÃ³n del changelog...")  # Mensaje de inicio
 
 def get_git_tags():
-    # Obtener etiquetas de Git
     print("Obteniendo etiquetas de Git...")
-    result = subprocess.run(
-        ["git", "tag"],
-        capture_output=True, text=True
-    )
+    result = subprocess.run(["git", "tag"], capture_output=True, text=True)
     if result.returncode != 0:
         print("Error al obtener etiquetas de Git:", result.stderr)
         return []
     return result.stdout.splitlines()
 
 def get_git_log(min_tag=None):
-    # Obtener commits recientes
     print("Obteniendo logs de Git...")
     command = ["git", "log", "--pretty=format:%h - %s"]
-    
     if min_tag:
-        command.append(f"{min_tag}..HEAD")  # Usar la etiqueta para limitar los commits
-    
+        command.append(f"{min_tag}..HEAD")
     result = subprocess.run(command, capture_output=True, text=True)
     if result.returncode != 0:
         print("Error al obtener logs de Git:", result.stderr)
@@ -38,80 +24,44 @@ def get_git_log(min_tag=None):
     return result.stdout.splitlines()
 
 def get_git_diff(commit_hash):
-    # Obtener los cambios de un commit especÃ­fico usando git diff
-    print(f"Obteniendo diferencias para el commit {commit_hash}...")
-    result = subprocess.run(
-        ["git", "diff", f"{commit_hash}~1", commit_hash],
-        capture_output=True, text=True
-    )
+    print(f"Obteniendo diferencias completas para el commit {commit_hash}...")
+    result = subprocess.run(["git", "diff", f"{commit_hash}~1", commit_hash], capture_output=True, text=True)
     if result.returncode != 0:
         print("Error al obtener diferencias de Git:", result.stderr)
         return ""
-    return result.stdout
-
-def summarize_diff(diff_content):
-    # Resumir el diff, aquÃ­ simplemente limitamos a los primeros 500 caracteres
-    return diff_content[:500]
+    return result.stdout  # No limitamos el contenido, obtenemos el diff completo
 
-def generate_prompt_with_changes(limit=10, min_tag=None):
+def generate_changelog_content(min_tag):
     commits = get_git_log(min_tag)
     if not commits:
         print("No se encontraron commits recientes.")
         return "No se encontraron commits recientes."
 
-    # Limitar a los Ãºltimos 'limit' commits
-    commits = commits[:limit]
-    prompt = "Generate a changelog based on the following commits and changes:\n\n"
-    
+    changelog = "Changelog generado:\n\n"
     for commit in commits:
         commit_hash, commit_message = commit.split(" - ", 1)
-        diff_content = summarize_diff(get_git_diff(commit_hash))
-
-        prompt += f"Commit Message: {commit_message}\n"
-        prompt += f"Changes:\n{diff_content}\n\n"
+        diff_content = get_git_diff(commit_hash)
+        changelog += f"Commit Message: {commit_message}\n"
+        changelog += f"Changes:\n{diff_content}\n\n"
     
-    return prompt
-
-def improve_changelog(prompt):
-    # Usar GPT para generar el changelog basado en el prompt
-    while True:  # Intentar hasta que se complete correctamente
-        try:
-            print("Generando changelog utilizando la API de OpenAI...")
-            response = openai.ChatCompletion.create(
-                model="gpt-3.5-turbo",
-                messages=[
-                    {"role": "system", "content": "You are a helpful assistant that generates changelogs."},
-                    {"role": "user", "content": prompt}
-                ],
-                max_tokens=5000
-            )
-            return response['choices'][0]['message']['content'].strip()
-        except openai.error.RateLimitError:
-            print("Rate limit exceeded. Waiting for 120 seconds before retrying...")
-            time.sleep(120)  # Esperar 120 segundos antes de reintentar
-        except Exception as e:
-            print(f"OcurriÃ³ un error inesperado: {e}")
-            break  # Salir del bucle en caso de un error inesperado
+    return changelog
 
 def save_changelog(content):
-    # Guardar el changelog generado
     filename = f"changelog_{date.today()}.md"
     with open(filename, "w", encoding="utf-8") as file:
         file.write(content)
-    print(f"Changelog saved to {filename}")
+    print(f"Changelog guardado en {filename}")
 
 # Obtener la versiÃ³n mÃ­nima a partir de la cual generar el changelog
 tags = get_git_tags()
-print("Etiquetas disponibles:", tags)
-min_tag = input("Introduce la versiÃ³n mÃ­nima (etiqueta de Git) a partir de la cual generar el changelog: ")
-
-# Verificar si la API key estÃ¡ configurada
-if openai.api_key:
-    prompt = generate_prompt_with_changes(min_tag=min_tag)
-    print("Prompt generado:", prompt)  # Imprimir el prompt para depuraciÃ³n
-    changelog = improve_changelog(prompt)
-    save_changelog(changelog)
+if len(tags) > 1:
+    min_tag = tags[-2]  # PenÃºltima etiqueta
 else:
-    print("Warning: OPENAI_API_KEY is not set. Generating a basic changelog based on git commits only.")
-    changelog = generate_prompt_with_changes(min_tag=min_tag)
-    save_changelog(changelog)
+    min_tag = None
+print(f"PenÃºltimo tag encontrado: {min_tag}")
+
+# Generar el contenido del changelog sin la API de OpenAI
+changelog_content = generate_changelog_content(min_tag)
+print("Resultado del changelog:\n")
+print(changelog_content)  # Imprimir el changelog en la consola
+save_changelog(changelog_content)  # Guardar el changelog en un archivo


Commit Message: Release version 1.4.0 - Cambios en la arquitectura del proyecto
Changes:
diff --git a/.gitignore b/.gitignore
index 3c521fa..d1fd74e 100644
--- a/.gitignore
+++ b/.gitignore
@@ -2,4 +2,5 @@ other
 data
 .env
 venv/
-__pycache__
\ No newline at end of file
+__pycache__
+temp
\ No newline at end of file
diff --git a/bin/scripts/generate_changelog.py b/bin/scripts/generate_changelog.py
new file mode 100644
index 0000000..bbf8d46
--- /dev/null
+++ b/bin/scripts/generate_changelog.py
@@ -0,0 +1,117 @@
+import subprocess
+import os
+from datetime import date
+from dotenv import load_dotenv
+import openai
+import time
+
+# Cargar la API Key de OpenAI
+load_dotenv()
+openai.api_key = os.getenv("OPENAI_API_KEY")
+
+print("Iniciando la generaciÃ³n del changelog...")  # Mensaje de inicio
+
+def get_git_tags():
+    # Obtener etiquetas de Git
+    print("Obteniendo etiquetas de Git...")
+    result = subprocess.run(
+        ["git", "tag"],
+        capture_output=True, text=True
+    )
+    if result.returncode != 0:
+        print("Error al obtener etiquetas de Git:", result.stderr)
+        return []
+    return result.stdout.splitlines()
+
+def get_git_log(min_tag=None):
+    # Obtener commits recientes
+    print("Obteniendo logs de Git...")
+    command = ["git", "log", "--pretty=format:%h - %s"]
+    
+    if min_tag:
+        command.append(f"{min_tag}..HEAD")  # Usar la etiqueta para limitar los commits
+    
+    result = subprocess.run(command, capture_output=True, text=True)
+    if result.returncode != 0:
+        print("Error al obtener logs de Git:", result.stderr)
+        return []
+    return result.stdout.splitlines()
+
+def get_git_diff(commit_hash):
+    # Obtener los cambios de un commit especÃ­fico usando git diff
+    print(f"Obteniendo diferencias para el commit {commit_hash}...")
+    result = subprocess.run(
+        ["git", "diff", f"{commit_hash}~1", commit_hash],
+        capture_output=True, text=True
+    )
+    if result.returncode != 0:
+        print("Error al obtener diferencias de Git:", result.stderr)
+        return ""
+    return result.stdout
+
+def summarize_diff(diff_content):
+    # Resumir el diff, aquÃ­ simplemente limitamos a los primeros 500 caracteres
+    return diff_content[:500]
+
+def generate_prompt_with_changes(limit=10, min_tag=None):
+    commits = get_git_log(min_tag)
+    if not commits:
+        print("No se encontraron commits recientes.")
+        return "No se encontraron commits recientes."
+
+    # Limitar a los Ãºltimos 'limit' commits
+    commits = commits[:limit]
+    prompt = "Generate a changelog based on the following commits and changes:\n\n"
+    
+    for commit in commits:
+        commit_hash, commit_message = commit.split(" - ", 1)
+        diff_content = summarize_diff(get_git_diff(commit_hash))
+
+        prompt += f"Commit Message: {commit_message}\n"
+        prompt += f"Changes:\n{diff_content}\n\n"
+    
+    return prompt
+
+def improve_changelog(prompt):
+    # Usar GPT para generar el changelog basado en el prompt
+    while True:  # Intentar hasta que se complete correctamente
+        try:
+            print("Generando changelog utilizando la API de OpenAI...")
+            response = openai.ChatCompletion.create(
+                model="gpt-3.5-turbo",
+                messages=[
+                    {"role": "system", "content": "You are a helpful assistant that generates changelogs."},
+                    {"role": "user", "content": prompt}
+                ],
+                max_tokens=5000
+            )
+            return response['choices'][0]['message']['content'].strip()
+        except openai.error.RateLimitError:
+            print("Rate limit exceeded. Waiting for 120 seconds before retrying...")
+            time.sleep(120)  # Esperar 120 segundos antes de reintentar
+        except Exception as e:
+            print(f"OcurriÃ³ un error inesperado: {e}")
+            break  # Salir del bucle en caso de un error inesperado
+
+def save_changelog(content):
+    # Guardar el changelog generado
+    filename = f"changelog_{date.today()}.md"
+    with open(filename, "w", encoding="utf-8") as file:
+        file.write(content)
+    print(f"Changelog saved to {filename}")
+
+# Obtener la versiÃ³n mÃ­nima a partir de la cual generar el changelog
+tags = get_git_tags()
+print("Etiquetas disponibles:", tags)
+min_tag = input("Introduce la versiÃ³n mÃ­nima (etiqueta de Git) a partir de la cual generar el changelog: ")
+
+# Verificar si la API key estÃ¡ configurada
+if openai.api_key:
+    prompt = generate_prompt_with_changes(min_tag=min_tag)
+    print("Prompt generado:", prompt)  # Imprimir el prompt para depuraciÃ³n
+    changelog = improve_changelog(prompt)
+    save_changelog(changelog)
+else:
+    print("Warning: OPENAI_API_KEY is not set. Generating a basic changelog based on git commits only.")
+    changelog = generate_prompt_with_changes(min_tag=min_tag)
+    save_changelog(changelog)
diff --git a/config/config.json b/config/config.json
index 7434af1..b808e2a 100644
--- a/config/config.json
+++ b/config/config.json
@@ -4,13 +4,35 @@
     "min_point_size": 5,
     "label_threshold": 400,
     "default_selected_data": "temperature_mean",
-    "map_xlim": [-7.6, -1.5],
-    "map_ylim": [35.8, 39],
+    "map_xlim": [
+        -7.6,
+        -1.5
+    ],
+    "map_ylim": [
+        35.8,
+        39
+    ],
     "shapefile_path": "config/shp/gadm41_ESP_4.shp",
     "language": "en",
-    "data_directory": "data", 
+    "data_directory": "data",
+    "version": "1.1.4",
     "comunidades": [
         "ANDALUCIA",
-        "VALENCIA"
-    ]
-}
+        "VALENCIA",
+        "CATALUÃ‘A",
+        "MADRID",
+        "GALICIA"
+    ],
+    "api_settings": {
+        "base_url": "https://api.open-meteo.com/v1/forecast",
+        "daily_params": [
+            "temperature_2m_max",
+            "temperature_2m_min",
+            "windspeed_10m_max",
+            "windgusts_10m_max",
+            "winddirection_10m_dominant",
+            "precipitation_sum"
+        ],
+        "timezone": "Europe/Madrid"
+    }
+}
\ No newline at end of file
diff --git a/config/templates/MeteoData.xlsx b/config/templates/MeteoData_Template.xlsm
similarity index 50%
rename from config/templates/MeteoData.xlsx
rename to config/templates/MeteoData_Template.xlsm
index a13ba0f..84d10ec 100644
Binary files a/config/templates/MeteoData.xlsx and b/config/templates/MeteoData_Template.xlsm differ
diff --git a/doc/architecture.md b/doc/architecture.md
new file mode 100644
index 0000000..250bf1c
--- /dev/null
+++ b/doc/architecture.md
@@ -0,0 +1,120 @@
+
+# Architecture
+
+## Overview
+
+**MeteoWave** is a Python-based application designed to fetch, process, and visualize meteorological data, focusing on specific regions in Spain. The main objectives of the application are:
+- To fetch weather data from external sources.
+- To process and organize the data for visualization.
+- To display the data on interactive maps with configurable visualization parameters.
+
+This document provides an architectural overview of the project, including the main components, directory structure, and data flow across modules.
+
+## Project Structure
+
+The MeteoWave project follows a modular architecture, with each module dedicated to specific functionalities. Below is an overview of the directory structure and the responsibilities of each module.
+
+```plaintext
+MeteoWave/
+â”œâ”€â”€ bin/                     # Batch files for running scripts and setting up releases
+â”œâ”€â”€ config/                  # Configuration files, including settings and templates
+â”‚   â”œâ”€â”€ shp/                 # Shapefiles for geographic regions
+â”‚   â””â”€â”€ templates/           # Excel templates for data storage
+â”œâ”€â”€ data/                    # Directory for storing acquired data and results
+â”‚   â”œâ”€â”€ YYYY/MM/             # Subdirectories for data organized by year and month
+â”œâ”€â”€ doc/                     # Documentation files
+â”œâ”€â”€ locales/                 # Language files for localization (e.g., en.json, es.json)
+â”œâ”€â”€ src/                     # Main source code directory
+â”‚   â”œâ”€â”€ core/                # Core logic and main entry point
+â”‚   â”œâ”€â”€ data_acquisition/    # Modules for fetching data from APIs
+â”‚   â”œâ”€â”€ data_processing/     # Modules for processing and cleaning data
+â”‚   â”œâ”€â”€ utils/               # Utility functions used across modules
+â”‚   â””â”€â”€ visualization/       # Modules for data visualization
+â”œâ”€â”€ tests/                   # Testing directory with unit, integration, and E2E tests
+â”‚   â”œâ”€â”€ e2e_tests/           # End-to-End tests
+â”‚   â”œâ”€â”€ integration_tests/   # Integration tests
+â”‚   â””â”€â”€ unit_tests/          # Unit tests for individual functions and modules
+â””â”€â”€ .github/                 # CI/CD workflows for GitHub Actions
+```
+
+### Module Breakdown
+
+#### 1. `core/`
+This module contains the core logic and main entry point of **MeteoWave**. It coordinates the flow of data from acquisition through to visualization.
+
+- **Key Functions**: `menu_principal`, `procesar_datos`
+- **Main Responsibilities**:
+  - Orchestrating data acquisition, processing, and visualization steps.
+  - Handling user interactions, such as selecting regions and dates.
+
+#### 2. `data_acquisition/`
+This module is responsible for fetching weather data from external APIs (e.g., Open Meteo).
+
+- **Key Functions**: `obtener_fechas_disponibles_api`, `obtener_datos_meteo`
+- **Main Responsibilities**:
+  - Handling API requests for weather data based on location and date.
+  - Managing retries and error handling for network issues.
+
+#### 3. `data_processing/`
+This module processes raw weather data, cleaning, formatting, and organizing it for storage or visualization.
+
+- **Key Functions**: `copiar_plantilla_si_no_existe`, `cargar_excel`
+- **Main Responsibilities**:
+  - Data cleaning and transformation.
+  - Organizing data into a structured format compatible with visualization.
+
+#### 4. `visualization/`
+The visualization module generates interactive maps to display meteorological data. It utilizes geographic data from shapefiles to render maps.
+
+- **Key Functions**: `update_scatter`, `set_selected_data`
+- **Main Responsibilities**:
+  - Displaying weather data on maps with visual indicators (e.g., color and size based on metrics).
+  - Allowing user interactions, such as hovering to view data values.
+
+#### 5. `utils/`
+This module contains utility functions used across various parts of the project. These functions include file handling, configuration loading, and auxiliary processes.
+
+- **Key Functions**: `cargar_configuracion`, `cargar_traducciones`, `inicializar_directorios`
+- **Main Responsibilities**:
+  - Supporting data processing, file operations, and configuration management.
+  - Simplifying repeated tasks across modules.
+
+## Data Flow
+
+The data flow in **MeteoWave** follows a logical sequence, beginning with data acquisition, moving through processing, and finally reaching visualization.
+
+1. **Data Acquisition** (`data_acquisition/`):
+   - The application fetches data from the API based on specified parameters (e.g., location, date).
+   - `obtener_fechas_disponibles_api` and `obtener_datos_meteo` manage the request and retrieval of raw weather data.
+
+2. **Data Processing** (`data_processing/`):
+   - The raw data is cleaned and structured in `data_processing` before being stored or visualized.
+   - Excel templates are used to organize data for historical reference and reporting.
+
+3. **Data Storage** (`data/`):
+   - The processed data is saved in the `data/` directory, organized by date and region for easy access.
+   - Historical data is stored in Excel files for use in future analysis or visualization.
+
+4. **Visualization** (`visualization/`):
+   - The data is loaded into the `visualization` module to generate interactive maps.
+   - Users can interact with the map to view detailed data points, and the visualization is customized based on user-selected metrics and regions.
+
+## CI/CD Integration
+
+The **MeteoWave** project uses GitHub Actions for continuous integration (CI) and deployment processes. The `ci.yml` workflow file in `.github/workflows/` defines automated testing triggered on each commit or pull request.
+
+- **Steps in CI/CD Pipeline**:
+  1. **Setup**: Clone the repository, set up Python, and install dependencies.
+  2. **Testing**: Execute unit, integration, and E2E tests to ensure code reliability.
+  3. **Deployment** (if applicable): Deploy changes if all tests pass.
+
+## Future Improvements
+
+1. **Expand Data Sources**: Integrate additional weather APIs for broader data coverage and redundancy.
+2. **Error Handling Enhancements**: Improve error handling for API requests, especially for rate limits and timeouts.
+3. **Scalability**: Adapt the architecture to handle larger datasets and multiple regions simultaneously.
+4. **Advanced Visualization**: Add dynamic features, such as time-based animations and additional weather metrics for a richer user experience.
+
+## Conclusion
+
+The **MeteoWave** architecture is modular and scalable, enabling straightforward maintenance, testing, and future expansion. Each module is dedicated to a specific responsibility, promoting a clear data flow from acquisition through processing to visualization. CI/CD integration via GitHub Actions ensures code reliability and project quality, making **MeteoWave** a robust solution for meteorological data analysis and visualization.
diff --git a/doc/changelog.md b/doc/changelog.md
new file mode 100644
index 0000000..0424a47
--- /dev/null
+++ b/doc/changelog.md
@@ -0,0 +1,56 @@
+
+# Changelog
+
+All notable changes to this project will be documented in this file.
+
+The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
+and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
+
+## [1.1.4] - 2024-11-06
+### Added
+- Added support for configurable visualization parameters in `config.json`.
+- Implemented `ci.yml` GitHub Actions workflow for continuous integration.
+- New `bin` batch files for running `geoPy.py` and `metPy.py` scripts with localization options.
+
+### Changed
+- Refactored `core.py` and `metPy.py` to use modular functions from `utils.py`.
+- Moved `geoPy.py` and `metPy.py` to `src` directory for a clearer project structure.
+
+### Fixed
+- Corrected issues with Excel file handling in `metPy.py` to avoid file locks.
+
+## [1.1.3] - 2024-11-05
+### Added
+- Integrated `.env` configuration file support for sensitive information like `GITHUB_TOKEN`.
+- Added error handling for API rate limits and network issues in `data_acquisition` module.
+
+### Changed
+- Updated `architecture.md` to reflect new modules and functions.
+
+### Fixed
+- Fixed `data_processing` module to handle missing or outlier values in API data.
+
+## [1.1.2] - 2024-11-05
+### Added
+- Included initial CI/CD setup for GitHub Actions.
+- Introduced locale support for English and Spanish (`locales/en.json` and `locales/es.json`).
+
+### Changed
+- Refined project structure with modular directories for core, data processing, and visualization.
+- Updated `config.json` to include `comunidades` list and API settings.
+
+### Fixed
+- Resolved issues with data formatting in Excel templates.
+
+## [1.1.1] - 2024-11-05
+### Added
+- Implemented data visualization with dynamic map interaction in `visualization/geoPy.py`.
+
+### Changed
+- Reorganized `config` directory to include `templates` for Excel files.
+
+## [1.1.0] - 2024-11-01
+### Added
+- Initial release of **MeteoWave** with modules for data acquisition, processing, and visualization.
+- Basic batch files for executing Python scripts.
+- Added `config.json` for centralized project configuration.
diff --git a/doc/contributing.md b/doc/contributing.md
new file mode 100644
index 0000000..778a675
--- /dev/null
+++ b/doc/contributing.md
@@ -0,0 +1,101 @@
+
+# Contributing to MeteoWave
+
+Thank you for your interest in contributing to MeteoWave! This guide provides information on the workflow and best practices for collaborating on the project.
+
+## Table of Contents
+- [Code of Conduct](#code-of-conduct)
+- [How to Report Issues](#how-to-report-issues)
+- [Contribution Process](#contribution-process)
+- [Project Structure](#project-structure)
+- [Testing and CI/CD](#testing-and-cicd)
+- [Code Standards](#code-standards)
+
+## Code of Conduct
+
+We want MeteoWave to be an inclusive and collaborative project. We ask that you are respectful and professional in all interactions with the community. Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.
+
+## How to Report Issues
+
+If you find a bug or would like to propose a new feature:
+1. Check [Issues](https://github.com/username/MeteoWave/issues) to ensure that a similar issue has not already been reported.
+2. Open a new issue with a detailed description of the problem or suggestion.
+3. Include steps to reproduce the problem (if applicable) and relevant screenshots or error logs.
+
+## Contribution Process
+
+### 1. Fork the Repository
+
+Fork the repository to your GitHub account and clone it to your machine:
+
+```bash
+git clone https://github.com/your_username/MeteoWave.git
+cd MeteoWave
+```
+
+### 2. Create a Branch for Your Contribution
+
+Use the `develop` branch for development. Create a new branch from `develop` with a descriptive name, for example:
+
+```bash
+git checkout -b feature/new-feature develop
+```
+
+**Note:** All development should be done in the `develop` branch. The `main` branch is reserved for deployment and release purposes.
+
+### 3. Make Changes and Add Tests
+
+Make the necessary changes in the code and ensure that:
+- The code is documented and follows the [Code Standards](#code-standards).
+- You add or update tests in `tests/` and `integration_tests/` as appropriate.
+
+### 4. Run the Tests
+
+Run all tests locally before submitting your contribution:
+
+```bash
+python -m unittest discover -s tests
+python -m unittest discover -s integration_tests
+```
+
+### 5. Create a Pull Request (PR)
+
+1. Push your changes to your forked repository.
+2. Open a *Pull Request* to the `develop` branch in the main repository.
+3. In the PR, provide a clear description of the changes made and their purpose.
+
+The maintenance team will review the PR and may suggest changes before approval.
+
+## Project Structure
+
+- `bin/`: Batch scripts to facilitate running project scripts.
+- `config/`: Configuration files and data templates.
+- `data/`: Test data and generated data storage.
+- `locales/`: Translation files for project localization.
+- `src/`: Main source code.
+  - `core/`: Core project logic.
+  - `data_acquisition/`: Functions to retrieve data from the Open Meteo API.
+  - `data_processing/`: Data processing functions.
+  - `utils/`: Utility or helper functions.
+  - `visualization/`: Code for visualizations and graphics.
+- `tests/`: Unit, integration, and end-to-end tests.
+
+## Testing and CI/CD
+
+The project has a CI/CD workflow set up in GitHub Actions that:
+- Runs unit and integration tests automatically when pushing or opening a PR to `develop` or `main`.
+- Verifies that all dependencies and configurations are up-to-date.
+
+Please check the CI/CD logs in your PR to ensure that your changes pass all tests.
+
+## Code Standards
+
+To maintain clean and maintainable code:
+- **PEP 8**: Follow Python's style guide.
+- **Documentation**: Document all key functions and classes.
+- **Commit Messages**: Use descriptive commit messages, e.g., `fix: correct error in community selection`.
+- **Type Hinting**: Use type hints where possible to improve readability and maintainability.
+
+## Questions
+
+If you have any questions, feel free to open an issue or contact the maintenance team. Thank you for contributing to MeteoWave!
diff --git a/doc/installation.md b/doc/installation.md
new file mode 100644
index 0000000..2ab9561
--- /dev/null
+++ b/doc/installation.md
@@ -0,0 +1,147 @@
+
+# Installation Guide
+
+Welcome to **MeteoWave**! This guide will walk you through the installation and initial setup of the application, including configuring important files and setting up dependencies.
+
+## Requirements
+
+Before starting, make sure you have:
+
+- **Python** 3.9 or higher installed.
+- Access to **Git** for cloning the repository.
+- **Virtual environment** support (recommended for dependency isolation).
+
+## Step 1: Clone the Repository
+
+Clone the repository to your local machine:
+
+```bash
+git clone https://github.com/yourusername/MeteoWave.git
+cd MeteoWave
+```
+
+## Step 2: Set Up a Virtual Environment
+
+To keep dependencies isolated and prevent conflicts, set up a virtual environment:
+
+```bash
+python -m venv venv
+```
+
+Activate the virtual environment:
+
+- **On Windows**:
+  ```bash
+  venv\Scripts\activate
+  ```
+- **On macOS/Linux**:
+  ```bash
+  source venv/bin/activate
+  ```
+
+## Step 3: Install Dependencies
+
+Install the required dependencies specified in the `requirements.txt` file:
+
+```bash
+pip install -r requirements.txt
+```
+
+If you need to generate the `requirements.txt` file manually, you can do so by running:
+
+```bash
+pip freeze > requirements.txt
+```
+
+## Step 4: Configure the Application
+
+### 1. Configuration File: `config.json`
+
+The application uses a `config.json` file located in the `config` folder to define various parameters. Here is a template of the file with explanations of each field:
+
+```json
+{
+    "base_size": 10,
+    "max_point_size": 500,
+    "min_point_size": 5,
+    "label_threshold": 400,
+    "default_selected_data": "temperature_mean",
+    "map_xlim": [-7.6, -1.5],
+    "map_ylim": [35.8, 39],
+    "shapefile_path": "config/shp/gadm41_ESP_4.shp",
+    "language": "en",
+    "data_directory": "data",
+    "template_path": "config/templates/MeteoData.xlsx",
+    "version": "1.1.4",
+    "comunidades": [
+        "ANDALUCIA",
+        "VALENCIA",
+        "CATALUÃ‘A",
+        "MADRID",
+        "GALICIA"
+    ],
+    "api_settings": {
+        "base_url": "https://api.open-meteo.com/v1/forecast",
+        "daily_params": [
+            "temperature_2m_max",
+            "temperature_2m_min",
+            "windspeed_10m_max",
+            "windgusts_10m_max",
+            "winddirection_10m_dominant",
+            "precipitation_sum"
+        ],
+        "timezone": "Europe/Madrid"
+    }
+}
+```
+
+### 2. `.env` File
+
+If not already created, set up a `.env` file to store sensitive information (e.g., API tokens):
+
+```bash
+GITHUB_TOKEN=your_token_here
+```
+
+> **Note:** Make sure to add your `.env` file to `.gitignore` to prevent it from being uploaded to the repository.
+
+## Step 5: Initial Setup Script
+
+To streamline the setup, run the `setup.bat` script (on Windows) or the equivalent shell script on macOS/Linux to create the environment, activate it, and install dependencies automatically.
+
+```bash
+setup.bat
+```
+
+This script performs the following tasks:
+
+- Creates and activates the virtual environment.
+- Installs dependencies.
+- Checks for a `.env` file and prompts for manual updates if necessary.
+
+## Step 6: Run the Application
+
+After setup is complete, you can run the application:
+
+```bash
+python src/metPy.py
+```
+
+## Step 7: Testing the Application (Optional)
+
+Run unit tests to verify that the application is set up correctly. If you have configured CI/CD, these tests should run automatically on each commit.
+
+```bash
+python -m unittest discover -s tests -p "*.py"
+```
+
+---
+
+### Additional Notes
+
+- **Language Support**: Set `"language": "en"` in `config.json` for English, or `"es"` for Spanish.
+- **Git Branches**: Development should occur in the `develop` branch, while releases are merged into `main`.
+
+---
+
+This should cover the installation and initial configuration of **MeteoWave**. For any questions, consult the documentation or reach out to the development team.
diff --git a/doc/overview.md b/doc/overview.md
new file mode 100644
index 0000000..f4f7d39
--- /dev/null
+++ b/doc/overview.md
@@ -0,0 +1,22 @@
+
+# Overview
+
+**MeteoWave** is a Python application designed for retrieving, processing, and visualizing meteorological data for specific regions in Spain. This project provides tools to fetch weather data from APIs, process it into structured formats, and display it interactively on maps.
+
+## Key Features
+
+- **Data Acquisition**: Fetches weather data from the Open Meteo API for specified dates and locations.
+- **Data Processing**: Cleans and organizes the data for analysis and visualization.
+- **Visualization**: Generates interactive maps displaying weather metrics with color and size variations based on the data values.
+- **Localization**: Supports multiple languages, including English and Spanish.
+
+## Technologies Used
+
+- **Python**: Main programming language.
+- **GitHub Actions**: For CI/CD workflows.
+- **Matplotlib & Geopandas**: For visualizing geographical data.
+- **Win32com**: For interacting with Excel files.
+
+## Project Goals
+
+The primary goal of **MeteoWave** is to provide a reliable and user-friendly tool for analyzing meteorological data, making it accessible to users who may not have advanced technical skills.
diff --git a/doc/spec/core.md b/doc/spec/core.md
new file mode 100644
index 0000000..e69de29
diff --git a/doc/spec/data_acquisition.md b/doc/spec/data_acquisition.md
new file mode 100644
index 0000000..e69de29
diff --git a/doc/spec/data_processing.md b/doc/spec/data_processing.md
new file mode 100644
index 0000000..e69de29
diff --git a/doc/spec/utils.md b/doc/spec/utils.md
new file mode 100644
index 0000000..e69de29
diff --git a/doc/spec/visualization.md b/doc/spec/visualization.md
new file mode 100644
index 0000000..e69de29
diff --git a/doc/tests.md b/doc/tests.md
new file mode 100644
index 0000000..e69de29
diff --git a/doc/usage.md b/doc/usage.md
new file mode 100644
index 0000000..85f9feb
--- /dev/null
+++ b/doc/usage.md
@@ -0,0 +1,52 @@
+
+# Usage
+
+This guide provides instructions on how to use **MeteoWave** for retrieving, processing, and visualizing weather data.
+
+## Basic Workflow
+
+1. **Fetch Weather Data**: Run the application and choose the region and date for which you want weather data.
+2. **Process Data**: The application will process the raw data, converting it into a structured format for analysis.
+3. **Visualize Data**: Use the map interface to interact with the weather data, viewing metrics such as temperature, wind speed, and precipitation.
+
+## Running the Application
+
+After completing the installation, you can run the application using the following options:
+
+### Option 1: Run with Python Command
+
+```bash
+python src/metPy.py
+```
+
+### Option 2: Run with .bat Files
+
+To streamline execution, use the provided `.bat` files in the `bin` directory:
+
+- **`run_metPy.bat`**: Runs the `metPy.py` script for data processing.
+- **`run_geoPy.bat`**: Runs the `geoPy.py` script for data visualization.
+- **`run_tests.bat`**: Runs all tests.
+
+> **Note**: Double-clicking the `.bat` file will automatically activate the virtual environment and execute the corresponding Python script.
+
+## User Interface
+
+- **Map Interaction**: Hover over regions to see specific data points.
+- **Data Selection**: Use buttons to switch between metrics (e.g., temperature, wind speed).
+- **Language Setting**: Change language settings in `config.json` to switch between English and Spanish.
+
+## Additional Commands
+
+- **Run Tests**: To verify the setup and functionality of the application:
+
+  ```bash
+  python -m unittest discover -s tests -p "*.py"
+  ```
+
+Alternatively, you can run tests using the `.bat` file:
+
+```bash
+bin\run_tests.bat
+```
+
+This file will activate the environment and execute all tests, providing a streamlined testing process.
diff --git a/requirements.txt b/requirements.txt
index 6c7a8d5..e3e8962 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -23,3 +23,5 @@ shapely==2.0.6
 six==1.16.0
 tzdata==2024.2
 urllib3==2.2.3
+pywin32
+python-dotenv
\ No newline at end of file
diff --git a/setup.bat b/setup.bat
index d2a7e83..a0c2d96 100644
--- a/setup.bat
+++ b/setup.bat
@@ -2,23 +2,64 @@
 @chcp 65001 >nul
 SETLOCAL ENABLEDELAYEDEXPANSION
 
-REM Crear entorno virtual
-python -m venv venv
-echo Entorno virtual creado en la carpeta 'venv'.
-
-REM Activar entorno virtual
-call venv\Scripts\activate
-
-REM Instalar dependencias desde requirements.txt
-pip install -r requirements.txt
-echo Dependencias instaladas correctamente.
-
-REM Crear archivo .env si no existe
-IF NOT EXIST .env (
-    echo GITHUB_TOKEN=tu_token_aqui > .env
-    echo Archivo .env creado. Por favor, aÃ±ade tus credenciales en el archivo .env.
-) ELSE (
-    echo El archivo .env ya existe.
+REM Crear entorno virtual si no existe
+if not exist "venv" (
+    python -m venv venv
+    echo Entorno virtual creado en la carpeta 'venv'.
+) else (
+    echo Entorno virtual ya existe.
+)
+
+REM Activar el entorno virtual
+if exist venv\Scripts\activate (
+    call venv\Scripts\activate
+    echo Entorno virtual activado.
+) else (
+    echo Error: No se pudo activar el entorno virtual.
+    pause
+    exit /b
+)
+
+REM Usar ruta absoluta para python en el entorno virtual y forzar instalaciÃ³n de pip
+set "VENV_PYTHON=venv\Scripts\python.exe"
+if exist %VENV_PYTHON% (
+    echo Python encontrado en el entorno virtual. Instalando dependencias...
+    %VENV_PYTHON% -m ensurepip --upgrade
+    %VENV_PYTHON% -m pip install --upgrade pip
+    %VENV_PYTHON% -m pip install -r requirements.txt
+    echo Dependencias instaladas correctamente.
+) else (
+    echo Error: No se pudo encontrar python en el entorno virtual.
+    echo Verifica si el entorno virtual contiene python.exe en venv\Scripts.
+    echo Si el archivo no estÃ¡ presente, intenta recrear el entorno virtual.
+    pause
+    exit /b
+)
+
+REM Crear o actualizar archivo .env con GITHUB_TOKEN, TEMPLATE_PATH y OPENAI_API_KEY
+set "env_path=.env"
+set "template_path=%cd%\config\templates\MeteoData_Template.xlsm"
+
+REM AÃ±adir GITHUB_TOKEN, TEMPLATE_PATH y OPENAI_API_KEY si no estÃ¡n presentes en .env
+set "found_template_path=false"
+set "found_openai_api_key=false"
+
+REM Verificar existencia de TEMPLATE_PATH y OPENAI_API_KEY
+for /f "tokens=1* delims==" %%i in ('type "%env_path%"') do (
+    if /i "%%i"=="TEMPLATE_PATH" set "found_template_path=true"
+    if /i "%%i"=="OPENAI_API_KEY" set "found_openai_api_key=true"
+)
+
+REM AÃ±adir TEMPLATE_PATH si no se encontrÃ³
+if "%found_template_path%"=="false" (
+    echo TEMPLATE_PATH=%template_path% >> "%env_path%"
+    echo TEMPLATE_PATH agregado a .env
+)
+
+REM AÃ±adir OPENAI_API_KEY si no se encontrÃ³
+if "%found_openai_api_key%"=="false" (
+    echo OPENAI_API_KEY=your_openai_api_key_here >> "%env_path%"
+    echo OPENAI_API_KEY agregado a .env
 )
 
 echo ConfiguraciÃ³n inicial completada.
diff --git a/src/core/core.py b/src/core/core.py
new file mode 100644
index 0000000..3af15df
--- /dev/null
+++ b/src/core/core.py
@@ -0,0 +1,145 @@
+import os
+from datetime import datetime
+from src.utils.utils import (
+    cls,
+    cargar_configuracion,
+    cargar_traducciones,
+    inicializar_directorios,
+    copiar_plantilla_si_no_existe,
+    obtener_fechas_disponibles_api,
+    obtener_datos_meteo
+)
+import win32com.client as win32
+
+def menu_principal(config, plantilla, data_dir, api_settings):
+    """FunciÃ³n principal del menÃº para procesar datos meteorolÃ³gicos."""
+    latitud, longitud = 37.3891, -5.9845
+    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud, api_settings)
+
+    if not fechas_disponibles:
+        print("No se encontraron fechas disponibles.")
+        input("Presione Enter para continuar...")
+        return
+
+    while True:
+        print("\n--- MenÃº Principal ---")
+        print("1. Procesar datos meteorolÃ³gicos")
+        print("2. Salir")
+        opcion = input("Seleccione una opciÃ³n: ")
+
+        if opcion == '1':
+            print("\nFechas disponibles:")
+            for i, fecha in enumerate(fechas_disponibles, start=1):
+                print(f"{i}. {fecha}")
+
+            while True:
+                try:
+                    seleccion_fecha = int(input("Seleccione una fecha (por nÃºmero): ")) - 1
+                    if 0 <= seleccion_fecha < len(fechas_disponibles):
+                        fecha = datetime.strptime(fechas_disponibles[seleccion_fecha], '%Y-%m-%d')
+                        break
+                    else:
+                        print("SelecciÃ³n fuera de rango.")
+                except ValueError:
+                    print("Entrada invÃ¡lida. Intente nuevamente.")
+
+            # Seleccionar comunidad autÃ³noma
+            comunidad = seleccionar_comunidad(config)
+            if comunidad is None:
+                print("No se seleccionÃ³ ninguna comunidad.")
+                continue
+
+            # Procesar datos con la fecha y comunidad seleccionada
+            procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings)
+
+            input("Procesamiento completado. Presione Enter para ver los resultados...")
+
+        elif opcion == '2':
+            print("Saliendo...")
+            break
+        else:
+            print("SelecciÃ³n invÃ¡lida.")
+            input("Presione Enter para continuar...")
+
+def seleccionar_comunidad(config):
+    """Permite seleccionar una comunidad autÃ³noma desde la configuraciÃ³n."""
+    comunidades = config.get("comunidades", [])
+    if not comunidades:
+        print("No se encontraron comunidades en la configuraciÃ³n.")
+        input("Presione Enter para continuar...")
+        return None
+
+    print("Seleccione una comunidad autÃ³noma:")
+    for i, comunidad in enumerate(comunidades, start=1):
+        print(f"{i}. {comunidad}")
+
+    while True:
+        try:
+            seleccion = int(input("Seleccione una opciÃ³n: ")) - 1
+            if 0 <= seleccion < len(comunidades):
+                return comunidades[seleccion]
+            else:
+                print("SelecciÃ³n fuera de rango.")
+        except ValueError:
+            print("Entrada invÃ¡lida.")
+
+def procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings):
+    """Procesa los datos meteorolÃ³gicos para la fecha y comunidad especificada."""
+    archivo_destino = copiar_plantilla_si_no_existe(fecha, plantilla, data_dir)
+
+    # Verificar si el archivo de destino existe antes de intentar abrirlo
+    if not archivo_destino or not os.path.exists(archivo_destino):
+        print(f"Error: El archivo {archivo_destino} no se pudo crear o no existe.")
+        return
+
+    excel = win32.Dispatch("Excel.Application")
+    excel.Visible = False  # Oculta Excel durante el procesamiento
+    wb = None
+
+    try:
+        print(f"Intentando abrir el archivo de destino: {archivo_destino}")
+        wb = excel.Workbooks.Open(archivo_destino)  # Abrir archivo de destino
+        ws = wb.Sheets(comunidad)
+        fecha_str = fecha.strftime('%Y-%m-%d')
+
+        # Llenar datos en el Excel
+        for row in range(2, ws.UsedRange.Rows.Count + 1):
+            coordenadas = ws.Cells(row, 3).Value  # Columna C
+            if coordenadas:
+                latitud, longitud = map(float, coordenadas.split(', '))
+                datos = obtener_datos_meteo(latitud, longitud, fecha, api_settings)
+
+                if datos:
+                    ws.Cells(row, 8).Value = datos['temperature_min']  # Columna H
+                    ws.Cells(row, 9).Value = datos['temperature_max']  # Columna I
+                    ws.Cells(row, 10).Value = datos['windspeed_max']  # Columna J
+                    ws.Cells(row, 11).Value = datos['windgusts_max']  # Columna K
+                    ws.Cells(row, 12).Value = datos['winddirection_dominant']  # Columna L
+                    ws.Cells(row, 13).Value = datos['precipitation_sum']  # Columna M
+                    ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Columna N
+                else:
+                    print(f"Datos no encontrados para la fecha: {fecha_str}")
+
+        wb.Save()
+        print(f"Datos meteorolÃ³gicos guardados en {archivo_destino}")
+
+    except Exception as e:
+        print(f"OcurriÃ³ un error al procesar el archivo de datos: {e}")
+
+    finally:
+        if wb:
+            wb.Close(False)
+        excel.Quit()
+
+# EjecuciÃ³n principal
+if __name__ == "__main__":
+    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
+    config = cargar_configuracion(config_path)
+    traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(os.path.dirname(__file__), '..', '..', 'locales'))
+    data_dir = config.get("data_directory", "data")
+    plantilla = config.get("template_path", "config/templates/MeteoData_Template.xlsm")
+    api_settings = config.get("api_settings", {})
+    
+    inicializar_directorios(data_dir)
+    cls()
+    menu_principal(config, plantilla, data_dir, api_settings)
diff --git a/src/data_processing/metPy.py b/src/data_processing/metPy.py
index e9b4435..cdbaa0b 100644
--- a/src/data_processing/metPy.py
+++ b/src/data_processing/metPy.py
@@ -1,172 +1,88 @@
 import os
-import shutil
-import requests
-import pandas as pd
-from openpyxl import load_workbook
+import sys
 from datetime import datetime
-import time
-import json
-
-def cls():
-    """Limpia la pantalla."""
-    os.system('cls' if os.name == 'nt' else 'clear')
+from dotenv import load_dotenv
+import win32com.client as win32
+
+# Configurar la ruta absoluta del proyecto y aÃ±adir `src` al `sys.path`
+project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
+src_path = os.path.join(project_root, 'src')
+sys.path.insert(0, src_path)
+
+# Importar los mÃ³dulos desde `src`
+from utils.utils import (
+    cargar_configuracion,
+    cargar_traducciones,
+    inicializar_directorios,
+    copiar_plantilla_si_no_existe,
+    obtener_fechas_disponibles_api,
+    obtener_datos_meteo,
+    seleccionar_comunidad
+)
+
+load_dotenv()  # Carga las variables del .env
+
+def procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings):
+    """Procesa los datos meteorolÃ³gicos para la fecha y comunidad especificadas usando win32com."""
+    archivo_destino = copiar_plantilla_si_no_existe(fecha, plantilla, data_dir)
+
+    # Convertimos la ruta en absoluta para asegurar que Excel la interprete correctamente
+    archivo_destino = os.path.abspath(archivo_destino) if archivo_destino else None
+
+    # Verificar si el archivo de destino existe antes de intentar abrirlo
+    if not archivo_destino or not os.path.exists(archivo_destino):
+        print(f"Error: El archivo {archivo_destino} no se pudo crear o no existe.")
+        return
 
-def cargar_configuracion():
-    """Carga la configuraciÃ³n desde el archivo config.json."""
-    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
-    try:
-        with open(config_path, "r", encoding="utf-8") as file:
-            return json.load(file)
-    except FileNotFoundError:
-        print("Error: El archivo config.json no se encuentra en la ruta especificada.")
-        input("Presione Enter para continuar...")
-        exit(1)
-    except json.JSONDecodeError:
-        print("Error: El archivo config.json tiene un formato JSON no vÃ¡lido.")
-        input("Presione Enter para continuar...")
-        exit(1)
+    excel = win32.Dispatch("Excel.Application")
+    excel.Visible = False  # Oculta Excel durante el procesamiento
+    wb = None  # Asegura que wb estÃ© definida para evitar errores de cierre
 
-def cargar_traducciones(idioma="es"):
-    """Carga el archivo de traducciones en el idioma especificado."""
-    locales_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'locales')
-    idioma_path = os.path.join(locales_dir, f"{idioma}.json")
     try:
-        with open(idioma_path, 'r', encoding='utf-8') as f:
-            return json.load(f)
-    except FileNotFoundError:
-        print("Archivo de idioma no encontrado. Usando idioma predeterminado (espaÃ±ol).")
-        input("Presione Enter para continuar...")
-        with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
-            return json.load(f)
-
-def inicializar_directorios(data_dir):
-    """Inicializa el directorio de almacenamiento de datos."""
-    os.makedirs(data_dir, exist_ok=True)
-
-def obtener_fechas_disponibles_api(latitud, longitud):
-    """Obtiene las fechas disponibles desde la API de Open-Meteo."""
-    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&daily=temperature_2m_max&timezone=Europe/Madrid"
-    for intento in range(5):  # MÃ¡ximo 5 reintentos
-        response = requests.get(url)
-        if response.status_code == 200:
-            return response.json().get('daily', {}).get('time', [])
-        elif response.status_code == 429:
-            print(traducciones["too_many_requests"])
-            time.sleep(5)
-        else:
-            print(traducciones["request_error"].format(code=response.status_code))
-            input("Presione Enter para continuar...")
-            return []
-    print(traducciones["max_retries_reached"])
-    input("Presione Enter para continuar...")
-    return []
-
-def verificar_archivo_existente(fecha, comunidad, data_dir):
-    """Verifica si existe un archivo de datos para la fecha y comunidad especificadas."""
-    fecha_str = fecha.replace("-", "")
-    archivo = os.path.join(data_dir, f"{fecha[:4]}/{fecha[5:7]}/MeteoData_{fecha_str}.xlsx")
-    if os.path.exists(archivo):
-        ultima_actualizacion = datetime.fromtimestamp(os.path.getmtime(archivo)).strftime('%Y-%m-%d %H:%M:%S')
-        datos_rellenos = verificar_datos_rellenos(archivo, comunidad)
-        return True, ultima_actualizacion, datos_rellenos
-    return False, None, False
-
-def verificar_datos_rellenos(archivo, comunidad):
-    """Verifica si hay datos rellenados en la hoja correspondiente a la comunidad autÃ³noma."""
-    wb = load_workbook(archivo)
-    if comunidad not in wb.sheetnames:
-        return False
-    ws = wb[comunidad]
-    return any(ws[f'H{row}'].value is not None for row in range(2, ws.max_row + 1))
-
-def obtener_datos_meteo(latitud, longitud, fecha):
-    """Obtiene los datos meteorolÃ³gicos de la API para la fecha y coordenadas especificadas."""
-    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,precipitation_sum&timezone=Europe/Madrid"
-    response = requests.get(url)
-    if response.status_code == 200:
-        return response.json()
-    else:
-        print(traducciones["request_error"].format(code=response.status_code))
-        input("Presione Enter para continuar...")
-        return None
-
-def copiar_plantilla(fecha, plantilla, data_dir):
-    """Copia la plantilla de archivo Excel para la fecha especificada."""
-    fecha_str = fecha.strftime('%Y%m%d')
-    anio_dir = os.path.join(data_dir, fecha.strftime('%Y'))
-    mes_dir = os.path.join(anio_dir, fecha.strftime('%m'))
-    os.makedirs(mes_dir, exist_ok=True)
-    archivo_destino = os.path.join(mes_dir, f"MeteoData_{fecha_str}.xlsx")
-    shutil.copyfile(plantilla, archivo_destino)
-    return archivo_destino
-
-def seleccionar_comunidad(config):
-    """Selecciona una comunidad autÃ³noma de la configuraciÃ³n."""
-    comunidades = config.get("comunidades", [])
-    if not comunidades:
-        print(traducciones["no_communities_found"])
-        input("Presione Enter para continuar...")
-        return None
-
-    print(traducciones["select_community"])
-    for i, comunidad in enumerate(comunidades, start=1):
-        print(f"{i}. {comunidad}")
+        print(f"Intentando abrir el archivo de destino: {archivo_destino}")
+        wb = excel.Workbooks.Open(archivo_destino)  # Abrir archivo de destino con ruta absoluta
+        ws = wb.Sheets(comunidad)
+        fecha_str = fecha.strftime('%Y-%m-%d')
 
-    while True:
-        try:
-            seleccion = int(input(traducciones["select_community_option"])) - 1
-            if 0 <= seleccion < len(comunidades):
-                return comunidades[seleccion]
-            else:
-                print(traducciones["invalid_selection"])
-        except ValueError:
-            print(traducciones["invalid_input"])
-
-def procesar_datos(fecha, comunidad, data_dir, plantilla):
-    """Procesa los datos meteorolÃ³gicos para la fecha y comunidad especificadas."""
-    archivo_destino = copiar_plantilla(fecha, plantilla, data_dir)
-    wb = load_workbook(archivo_destino)
-    ws = wb[comunidad]
-    fecha_str = fecha.strftime('%Y-%m-%d')
-
-    for row in range(2, ws.max_row + 1):
-        try:
-            coordenadas = ws[f'C{row}'].value
+        for row in range(2, ws.UsedRange.Rows.Count + 1):
+            coordenadas = ws.Cells(row, 3).Value  # Columna C
             if coordenadas:
                 latitud, longitud = map(float, coordenadas.split(', '))
-                datos = obtener_datos_meteo(latitud, longitud, fecha)
-
-                if datos and fecha_str in datos['daily']['time']:
-                    index = datos['daily']['time'].index(fecha_str)
-                    ws[f'H{row}'] = datos['daily']['temperature_2m_min'][index]
-                    ws[f'I{row}'] = datos['daily']['temperature_2m_max'][index]
-                    ws[f'J{row}'] = datos['daily']['windspeed_10m_max'][index]
-                    ws[f'K{row}'] = datos['daily']['windgusts_10m_max'][index]
-                    ws[f'L{row}'] = datos['daily']['winddirection_10m_dominant'][index]
-                    ws[f'M{row}'] = datos['daily']['precipitation_sum'][index]
-                    ws[f'N{row}'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
+                datos = obtener_datos_meteo(latitud, longitud, fecha, api_settings)
+
+                if datos:
+                    ws.Cells(row, 8).Value = datos['temperature_min']  # Columna H
+                    ws.Cells(row, 9).Value = datos['temperature_max']  # Columna I
+                    ws.Cells(row, 10).Value = datos['windspeed_max']  # Columna J
+                    ws.Cells(row, 11).Value = datos['windgusts_max']  # Columna K
+                    ws.Cells(row, 12).Value = datos['winddirection_dominant']  # Columna L
+                    ws.Cells(row, 13).Value = datos['precipitation_sum']  # Columna M
+                    ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Columna N
                 else:
-                    print(traducciones["date_not_found"].format(date=fecha_str))
-        except Exception as e:
-            print(traducciones["processing_error"].format(row=row, error=str(e)))
+                    print(f"Datos no encontrados para la fecha: {fecha_str}")
+
+        wb.Save()
+        print(f"Datos meteorolÃ³gicos guardados en {archivo_destino}")
+
+    except Exception as e:
+        print(f"OcurriÃ³ un error al procesar el archivo de datos: {e}")
 
-    wb.save(archivo_destino)
-    print(traducciones["data_saved"].format(archivo=archivo_destino))
-    input("Presione Enter para continuar...")  # Pausa despuÃ©s de procesar datos
+    finally:
+        if wb:
+            wb.Close(False)
+        excel.Quit()
 
-def menu_principal(config, plantilla):
+def menu_principal(config, plantilla, api_settings):
     """FunciÃ³n principal del menÃº para procesar datos meteorolÃ³gicos."""
     latitud, longitud = 37.3891, -5.9845
-    comunidad = seleccionar_comunidad(config)
 
-    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud)
+    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud, api_settings)
     if not fechas_disponibles:
         print(traducciones["no_dates_found"])
         input("Presione Enter para continuar...")
         return
 
     while True:
-        cls()  # Limpia la pantalla
         print("\n--- " + traducciones["main_menu"] + " ---")
         print("1. " + traducciones["process_data"])
         print("2. " + traducciones["exit"])
@@ -175,11 +91,7 @@ def menu_principal(config, plantilla):
         if opcion == '1':
             print("\n" + traducciones["available_dates"])
             for i, fecha in enumerate(fechas_disponibles, start=1):
-                existe, ultima_actualizacion, datos_rellenos = verificar_archivo_existente(fecha, comunidad, data_dir)
-                estado = (f"({traducciones['exists']} - {traducciones['last_update']}: {ultima_actualizacion}, "
-                          f"{traducciones['data_filled']}: {datos_rellenos})" if existe
-                          else f"({traducciones['does_not_exist']})")
-                print(f"{i}. {fecha} {estado}")
+                print(f"{i}. {fecha}")
 
             while True:
                 try:
@@ -192,25 +104,33 @@ def menu_principal(config, plantilla):
                 except ValueError:
                     print(traducciones["invalid_input"])
 
-            procesar_datos(fecha, comunidad, data_dir, plantilla)
+            # AÃ±adir 'traducciones' en la llamada
+            comunidad = seleccionar_comunidad(config, traducciones)
+            if comunidad is None:
+                print("No se seleccionÃ³ ninguna comunidad.")
+                continue
+
+            procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings)
+
+            input("Procesamiento completado. Presione Enter para ver los resultados...")
 
         elif opcion == '2':
             print(traducciones["exiting"])
             break
         else:
             print(traducciones["invalid_selection"])
-            input("Presione Enter para continuar...")  # Pausa si la selecciÃ³n no es vÃ¡lida
-
-# Cargar la configuraciÃ³n y traducciones
-config = cargar_configuracion()
-traducciones = cargar_traducciones(config.get("language", "es"))
+            input("Presione Enter para continuar...")
 
-# Directorio de almacenamiento de datos
-data_dir = config.get("data_dir", "data")
+# Cargar configuraciÃ³n y ejecutar menÃº principal
+config_path = os.path.join(project_root, 'config', 'config.json')
+config = cargar_configuracion(config_path)
+traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(project_root, 'locales'))
+data_dir = config.get("data_directory", "data")
 inicializar_directorios(data_dir)
 
-# ParÃ¡metros avanzados desde el archivo de configuraciÃ³n
-plantilla = config.get("template_path", "config/templates/MeteoData.xlsx")
+# Usa la ruta del TEMPLATE_PATH del archivo .env, o una ruta absoluta por defecto
+plantilla = os.getenv("TEMPLATE_PATH", os.path.join(project_root, "config", "templates", "MeteoData_Template.xlsm"))
+api_settings = config.get("api_settings", {})
 
-# Ejecutar el menÃº principal
-menu_principal(config, plantilla)
+# Llamar a la funciÃ³n principal
+menu_principal(config, plantilla, api_settings)
diff --git a/src/utils/utils.py b/src/utils/utils.py
new file mode 100644
index 0000000..9895612
--- /dev/null
+++ b/src/utils/utils.py
@@ -0,0 +1,197 @@
+import os
+import json
+import time
+import pandas as pd
+import geopandas as gpd
+import shutil
+import requests
+from dotenv import load_dotenv
+from datetime import datetime
+import win32com.client as win32
+
+# Cargar variables de entorno
+load_dotenv()
+
+def cls():
+    """Limpia la pantalla."""
+    os.system('cls' if os.name == 'nt' else 'clear')
+
+def cargar_configuracion(config_path):
+    """Carga la configuraciÃ³n desde el archivo JSON especificado."""
+    try:
+        with open(config_path, "r", encoding="utf-8") as file:
+            return json.load(file)
+    except FileNotFoundError:
+        print("Error: El archivo de configuraciÃ³n no se encuentra en la ruta especificada.")
+        exit()
+    except json.JSONDecodeError:
+        print("Error: El archivo de configuraciÃ³n tiene un formato JSON no vÃ¡lido.")
+        exit()
+
+def cargar_traducciones(idioma, locales_dir):
+    """Carga el archivo de traducciones en el idioma especificado."""
+    idioma_path = os.path.join(locales_dir, f"{idioma}.json")
+    try:
+        with open(idioma_path, 'r', encoding='utf-8') as f:
+            return json.load(f)
+    except FileNotFoundError:
+        print(f"Archivo de idioma '{idioma}.json' no encontrado. Usando idioma predeterminado (espaÃ±ol).")
+        with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
+            return json.load(f)
+
+def inicializar_directorios(data_dir):
+    """Inicializa el directorio de almacenamiento de datos."""
+    os.makedirs(data_dir, exist_ok=True)
+
+def listar_archivos_disponibles(data_dir, traducciones):
+    """Lista archivos en el directorio especificado que cumplen con el formato de nombre."""
+    directorio_completo = os.path.abspath(data_dir)
+    print(f"Buscando archivos en: {directorio_completo}")
+    
+    archivos = []
+    for root, dirs, files in os.walk(directorio_completo):
+        for file in files:
+            if file.startswith("MeteoData_") and file.endswith((".xlsx", ".xlsm")):
+                archivos.append(os.path.join(root, file))
+
+    if not archivos:
+        print(traducciones["no_files_available"])
+        return None
+    
+    print(traducciones["available_files"])
+    for i, archivo in enumerate(archivos, start=1):
+        print(f"{i}. {os.path.basename(archivo)}")
+    
+    while True:
+        try:
+            seleccion = int(input(traducciones["select_file"])) - 1
+            if 0 <= seleccion < len(archivos):
+                return archivos[seleccion]
+            else:
+                print(traducciones["selection_out_of_range"])
+        except ValueError:
+            print(traducciones["invalid_input"])
+
+def cargar_excel(archivo_seleccionado):
+    """Carga un archivo Excel y retorna sus hojas disponibles."""
+    try:
+        excel_file = pd.ExcelFile(archivo_seleccionado)
+        hojas_disponibles = excel_file.sheet_names
+        return excel_file, hojas_disponibles
+    except FileNotFoundError:
+        print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
+        return None, []
+
+def cargar_shapefile(shapefile_path, traducciones):
+    """Carga un archivo shapefile y retorna el objeto GeoDataFrame."""
+    if not os.path.exists(shapefile_path):
+        print(f"Error: No se encontrÃ³ el archivo de shapes en '{shapefile_path}'.")
+        exit()
+    try:
+        return gpd.read_file(shapefile_path)
+    except Exception as e:
+        print(traducciones["error_loading_shapefile"])
+        print(f"Detalles del error: {e}")
+        exit()
+
+def copiar_plantilla_si_no_existe(fecha, plantilla, data_dir):
+    """Copia la plantilla a la ubicaciÃ³n de destino solo si el archivo no existe."""
+    fecha_str = fecha.strftime('%Y%m%d')
+    archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha_str}.xlsm")
+
+    # Si el archivo de destino ya existe, no lo sobrescribimos
+    if os.path.exists(archivo_destino):
+        print(f"Archivo ya existente: {archivo_destino}. No se crearÃ¡ una nueva copia.")
+        return archivo_destino
+
+    archivo_temp = os.path.join(os.getenv('TEMP'), f"MeteoData_{fecha_str}_temp.xlsm")
+    excel = win32.Dispatch("Excel.Application")
+    excel.Visible = False
+
+    try:
+        # Verificar si la plantilla existe
+        if not os.path.exists(plantilla):
+            print(f"Error: La plantilla {plantilla} no se encuentra.")
+            return None
+
+        workbook = excel.Workbooks.Open(plantilla)
+        workbook.SaveAs(archivo_temp, FileFormat=52)  # 52 es el formato para .xlsm
+        workbook.Close(False)
+
+        # Mover la copia temporal al destino final
+        os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)
+        shutil.move(archivo_temp, archivo_destino)
+        
+        print(f"Copia de la plantilla creada en: {archivo_destino}")
+        return archivo_destino
+    except Exception as e:
+        print(f"OcurriÃ³ un error al copiar la plantilla: {e}")
+        return None
+    finally:
+        excel.Quit()
+
+def obtener_fechas_disponibles_api(latitud, longitud, api_settings):
+    """Obtiene las fechas disponibles desde la API de Open-Meteo utilizando la configuraciÃ³n de API."""
+    url = f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}"
+    for intento in range(5):  # MÃ¡ximo 5 reintentos
+        response = requests.get(url)
+        if response.status_code == 200:
+            return response.json().get('daily', {}).get('time', [])
+        elif response.status_code == 429:
+            print("Demasiadas solicitudes. Esperando para reintentar...")
+            time.sleep(5)
+        else:
+            print(f"Error en la solicitud. CÃ³digo de estado: {response.status_code}")
+            input("Presione Enter para continuar...")
+            return []
+    print("Se alcanzÃ³ el nÃºmero mÃ¡ximo de reintentos.")
+    input("Presione Enter para continuar...")
+    return []
+
+def obtener_datos_meteo(latitud, longitud, fecha, api_settings):
+    """Obtiene los datos meteorolÃ³gicos de la API para la fecha y coordenadas especificadas."""
+    fecha_str = fecha.strftime('%Y-%m-%d')
+    url = (f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}"
+           f"&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}")
+    response = requests.get(url)
+    if response.status_code == 200:
+        datos = response.json()
+        if fecha_str in datos['daily']['time']:
+            index = datos['daily']['time'].index(fecha_str)
+            return {
+                'temperature_min': datos['daily']['temperature_2m_min'][index],
+                'temperature_max': datos['daily']['temperature_2m_max'][index],
+                'windspeed_max': datos['daily']['windspeed_10m_max'][index],
+                'windgusts_max': datos['daily']['windgusts_10m_max'][index],
+                'winddirection_dominant': datos['daily']['winddirection_10m_dominant'][index],
+                'precipitation_sum': datos['daily']['precipitation_sum'][index]
+            }
+        else:
+            print(f"Datos no disponibles para la fecha: {fecha_str}")
+            return None
+    else:
+        print(f"Error en la solicitud. CÃ³digo de estado: {response.status_code}")
+        input("Presione Enter para continuar...")
+        return None
+
+def seleccionar_comunidad(config, traducciones):
+    """Permite seleccionar una comunidad autÃ³noma a partir de la configuraciÃ³n."""
+    comunidades = config.get("comunidades", [])
+    if not comunidades:
+        print(traducciones["no_communities_found"])
+        input("Presione Enter para continuar...")
+        return None
+
+    print(traducciones["select_community"])
+    for i, comunidad in enumerate(comunidades, start=1):
+        print(f"{i}. {comunidad}")
+
+    while True:
+        try:
+            seleccion = int(input(traducciones["select_community_option"])) - 1
+            if 0 <= seleccion < len(comunidades):
+                return comunidades[seleccion]
+            else:
+                print(traducciones["invalid_selection"])
+        except ValueError:
+            print(traducciones["invalid_input"])
diff --git a/src/visualization/geoPy.py b/src/visualization/geoPy.py
index 4cd51d9..f52c566 100644
--- a/src/visualization/geoPy.py
+++ b/src/visualization/geoPy.py
@@ -6,7 +6,6 @@ import matplotlib.pyplot as plt
 from matplotlib.colors import Normalize
 from matplotlib.widgets import Button
 from datetime import datetime
-import sys
 
 def cls():
     """Limpia la consola."""
@@ -38,19 +37,26 @@ def cargar_traducciones(idioma="es"):
         with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
             return json.load(f)
 
-# Variable global para rastrear el Ãºltimo punto sobre el que se pasÃ³ el ratÃ³n
-last_locality = None
-
 # Inicializar parÃ¡metros desde la configuraciÃ³n
 config = cargar_configuracion()
 traducciones = cargar_traducciones(config.get("language", "es"))
 
+# Variables de configuraciÃ³n
 label_threshold = config.get("label_threshold", 400)
 min_point_size = config.get("min_point_size", 5)
 max_point_size = config.get("max_point_size", 500)
-data_dir = config.get("data_directory", "Data")
+data_dir = config.get("data_directory", "data")
 shapefile_path = config.get("shapefile_path", "config/shp/gadm41_ESP_4.shp")
 
+# Unidad de medida para cada tipo de dato
+unit_dict = {
+    "temperature_min": "Â°C",
+    "temperature_max": "Â°C",
+    "wind_gusts": "km/h",
+    "wind_speed": "km/h",
+    "precipitation_sum": "mm"
+}
+
 # Verificar si el archivo shapefile existe
 if not os.path.exists(shapefile_path):
     print(f"Error: No se encontrÃ³ el archivo de shapes en '{shapefile_path}'.")
@@ -59,24 +65,11 @@ if not os.path.exists(shapefile_path):
 # Cargar el shapefile de EspaÃ±a
 try:
     espana_shapefile = gpd.read_file(shapefile_path)
-    comunidades = {
-        "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'AndalucÃ­a'],
-        "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']
-    }
 except Exception as e:
     print(traducciones["error_loading_shapefile"])
     print(f"Detalles del error: {e}")
     exit()
 
-# Definir la unidad de medida para cada tipo de dato
-unit_dict = {
-    "temperature_min": "Â°C",
-    "temperature_max": "Â°C",
-    "wind_gusts": "km/h",
-    "wind_speed": "km/h",
-    "precipitation_sum": "mm"
-}
-
 # FunciÃ³n para listar archivos disponibles en el directorio de datos
 def listar_archivos_disponibles():
     directorio_completo = os.path.abspath(data_dir)
@@ -86,7 +79,7 @@ def listar_archivos_disponibles():
     
     for root, dirs, files in os.walk(directorio_completo):
         for file in files:
-            if file.startswith("MeteoData_") and file.endswith(".xlsx"):
+            if file.startswith("MeteoData_") and (file.endswith(".xlsx") or file.endswith(".xlsm")):
                 archivos.append(os.path.join(root, file))
 
     if not archivos:
@@ -119,16 +112,34 @@ except FileNotFoundError:
     print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
     exit()
 
+# Filtrar las comunidades autÃ³nomas que tienen datos disponibles
+comunidades_con_datos = []
+comunidades = { 
+    "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'AndalucÃ­a'],
+    "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']
+}
+
+for hoja in hojas_disponibles:
+    df = pd.read_excel(archivo_seleccionado, sheet_name=hoja)
+    
+    # Verificar que el DataFrame no estÃ© vacÃ­o y que contenga datos en las columnas correspondientes
+    # Usamos los Ã­ndices de columna 7 a 10 (equivalente a H, I, J, K en Excel)
+    if not df.empty and df.iloc[:, 7:11].count().sum() > 0:
+        comunidades_con_datos.append(hoja)
+
+# Filtrar las comunidades segÃºn los datos disponibles
+comunidades = {k: v for k, v in comunidades.items() if k in comunidades_con_datos}
+
 print(traducciones["available_autonomous_communities"])
-for i, hoja in enumerate(hojas_disponibles, start=1):
-    print(f"{i}. {hoja}")
+for i, comunidad in enumerate(comunidades.keys(), start=1):
+    print(f"{i}. {comunidad}")
 
 # Permitir que el usuario seleccione la hoja (comunidad autÃ³noma)
 while True:
     try:
         seleccion_hoja = int(input(traducciones["select_community"])) - 1
-        if 0 <= seleccion_hoja < len(hojas_disponibles):
-            sheet_name = hojas_disponibles[seleccion_hoja]
+        if 0 <= seleccion_hoja < len(comunidades):
+            sheet_name = list(comunidades.keys())[seleccion_hoja]
             break
         else:
             print(traducciones["selection_out_of_range"])
@@ -147,7 +158,7 @@ if region_map is None or region_map.empty:
     print(f"Error: No se encontrÃ³ la regiÃ³n correspondiente para '{sheet_name}' en el shapefile.")
     exit()
 
-# Crear una figura para el grÃ¡fico
+# Crear la figura y grÃ¡ficos de datos meteorolÃ³gicos
 fig, ax1 = plt.subplots(figsize=(10, 8))
 fig.canvas.manager.set_window_title(f"Mapa de {sheet_name} - Datos MeteorolÃ³gicos")
 
diff --git a/tests/integration_tests/test_data_acquisition.py b/tests/integration_tests/test_data_acquisition.py
new file mode 100644
index 0000000..e1bd59f
--- /dev/null
+++ b/tests/integration_tests/test_data_acquisition.py
@@ -0,0 +1,22 @@
+import unittest
+from src.data_processing.metPy import obtener_datos_meteo
+
+class TestDataAcquisition(unittest.TestCase):
+
+    def test_obtener_datos_meteo(self):
+        # Configura datos de prueba
+        latitud = 37.3891
+        longitud = -5.9845
+        fecha = "2024-11-05"  # Ejemplo de fecha
+
+        # Llama a la funciÃ³n de adquisiciÃ³n de datos
+        datos = obtener_datos_meteo(latitud, longitud, fecha)
+
+        # Verifica que los datos no son None y contienen la informaciÃ³n esperada
+        self.assertIsNotNone(datos)
+        self.assertIn('daily', datos)
+        self.assertIn('temperature_2m_min', datos['daily'])
+        self.assertIn('temperature_2m_max', datos['daily'])
+
+if __name__ == '__main__':
+    unittest.main()
diff --git a/tests/integration_tests/test_full_processing.py b/tests/integration_tests/test_full_processing.py
new file mode 100644
index 0000000..74528da
--- /dev/null
+++ b/tests/integration_tests/test_full_processing.py
@@ -0,0 +1,24 @@
+import unittest
+from src.data_processing.metPy import procesar_datos, cargar_configuracion, copiar_plantilla
+from datetime import datetime
+
+class TestFullProcessing(unittest.TestCase):
+
+    def setUp(self):
+        # ConfiguraciÃ³n inicial de prueba
+        self.fecha = datetime.now()
+        self.config = cargar_configuracion()
+        self.data_dir = "data"
+        self.plantilla = self.config.get("template_path", "config/templates/MeteoData.xlsx")
+        self.comunidad = "ANDALUCIA"
+
+    def test_procesar_datos(self):
+        # Proceso completo de adquirir, procesar y guardar datos
+        archivo_destino = copiar_plantilla(self.fecha, self.plantilla, self.data_dir)
+        procesar_datos(self.fecha, self.comunidad, self.data_dir, archivo_destino)
+
+        # AquÃ­ podrÃ­as aÃ±adir verificaciones para asegurar que el archivo Excel se creÃ³ correctamente
+        # y que contiene los datos esperados
+
+if __name__ == '__main__':
+    unittest.main()
diff --git a/tests/test_geoPy.py b/tests/units_tests/test_geoPy.py
similarity index 100%
rename from tests/test_geoPy.py
rename to tests/units_tests/test_geoPy.py
diff --git a/tests/test_metPy.py b/tests/units_tests/test_metPy.py
similarity index 100%
rename from tests/test_metPy.py
rename to tests/units_tests/test_metPy.py


