import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import win32com.client as win32

# Configurar la ruta absoluta del proyecto y añadir `src` al `sys.path`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# Importar los módulos desde `src`
from utils.utils import (
    cargar_configuracion,
    cargar_traducciones,
    inicializar_directorios,
    copiar_plantilla_si_no_existe,
    obtener_fechas_disponibles_api,
    obtener_datos_meteo,
    seleccionar_comunidad
)

load_dotenv()  # Carga las variables del .env

def procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings):
    """Procesa los datos meteorológicos para la fecha y comunidad especificadas usando win32com."""
    archivo_destino = copiar_plantilla_si_no_existe(fecha, plantilla, data_dir)

    # Convertimos la ruta en absoluta para asegurar que Excel la interprete correctamente
    archivo_destino = os.path.abspath(archivo_destino) if archivo_destino else None

    # Verificar si el archivo de destino existe antes de intentar abrirlo
    if not archivo_destino or not os.path.exists(archivo_destino):
        print(f"Error: El archivo {archivo_destino} no se pudo crear o no existe.")
        return

    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False  # Oculta Excel durante el procesamiento
    wb = None  # Asegura que wb esté definida para evitar errores de cierre

    try:
        print(f"Intentando abrir el archivo de destino: {archivo_destino}")
        wb = excel.Workbooks.Open(archivo_destino)  # Abrir archivo de destino con ruta absoluta
        ws = wb.Sheets(comunidad)
        fecha_str = fecha.strftime('%Y-%m-%d')

        for row in range(2, ws.UsedRange.Rows.Count + 1):
            coordenadas = ws.Cells(row, 3).Value  # Columna C
            if coordenadas:
                latitud, longitud = map(float, coordenadas.split(', '))
                datos = obtener_datos_meteo(latitud, longitud, fecha, api_settings)

                if datos:
                    ws.Cells(row, 8).Value = datos['temperature_min']  # Columna H
                    ws.Cells(row, 9).Value = datos['temperature_max']  # Columna I
                    ws.Cells(row, 10).Value = datos['windspeed_max']  # Columna J
                    ws.Cells(row, 11).Value = datos['windgusts_max']  # Columna K
                    ws.Cells(row, 12).Value = datos['winddirection_dominant']  # Columna L
                    ws.Cells(row, 13).Value = datos['precipitation_sum']  # Columna M
                    ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Columna N
                else:
                    print(f"Datos no encontrados para la fecha: {fecha_str}")

        wb.Save()
        print(f"Datos meteorológicos guardados en {archivo_destino}")

    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo de datos: {e}")

    finally:
        if wb:
            wb.Close(False)
        excel.Quit()

def menu_principal(config, plantilla, api_settings):
    """Función principal del menú para procesar datos meteorológicos."""
    latitud, longitud = 37.3891, -5.9845

    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud, api_settings)
    if not fechas_disponibles:
        print(traducciones["no_dates_found"])
        input("Presione Enter para continuar...")
        return

    while True:
        print("\n--- " + traducciones["main_menu"] + " ---")
        print("1. " + traducciones["process_data"])
        print("2. " + traducciones["exit"])
        opcion = input(traducciones["select_option"])

        if opcion == '1':
            print("\n" + traducciones["available_dates"])
            for i, fecha in enumerate(fechas_disponibles, start=1):
                print(f"{i}. {fecha}")

            while True:
                try:
                    seleccion_fecha = int(input(traducciones["select_date_option"])) - 1
                    if 0 <= seleccion_fecha < len(fechas_disponibles):
                        fecha = datetime.strptime(fechas_disponibles[seleccion_fecha], '%Y-%m-%d')
                        break
                    else:
                        print(traducciones["invalid_selection"])
                except ValueError:
                    print(traducciones["invalid_input"])

            # Añadir 'traducciones' en la llamada
            comunidad = seleccionar_comunidad(config, traducciones)
            if comunidad is None:
                print("No se seleccionó ninguna comunidad.")
                continue

            procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings)

            input("Procesamiento completado. Presione Enter para ver los resultados...")

        elif opcion == '2':
            print(traducciones["exiting"])
            break
        else:
            print(traducciones["invalid_selection"])
            input("Presione Enter para continuar...")

# Cargar configuración y ejecutar menú principal
config_path = os.path.join(project_root, 'config', 'config.json')
config = cargar_configuracion(config_path)
traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(project_root, 'locales'))
data_dir = config.get("data_directory", "data")
inicializar_directorios(data_dir)

# Usa la ruta del TEMPLATE_PATH del archivo .env, o una ruta absoluta por defecto
plantilla = os.getenv("TEMPLATE_PATH", os.path.join(project_root, "config", "templates", "MeteoData_Template.xlsm"))
api_settings = config.get("api_settings", {})

# Llamar a la función principal
menu_principal(config, plantilla, api_settings)
