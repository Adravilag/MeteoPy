import os
import json
import time
import pandas as pd
import geopandas as gpd
import shutil
import requests
from dotenv import load_dotenv
from datetime import datetime
import win32com.client as win32

# Cargar variables de entorno
load_dotenv()

def cls():
    """Limpia la pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_configuracion(config_path):
    """Carga la configuración desde el archivo JSON especificado."""
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: El archivo de configuración no se encuentra en la ruta especificada.")
        exit()
    except json.JSONDecodeError:
        print("Error: El archivo de configuración tiene un formato JSON no válido.")
        exit()

def cargar_traducciones(idioma, locales_dir):
    """Carga el archivo de traducciones en el idioma especificado."""
    idioma_path = os.path.join(locales_dir, f"{idioma}.json")
    try:
        with open(idioma_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Archivo de idioma '{idioma}.json' no encontrado. Usando idioma predeterminado (español).")
        with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
            return json.load(f)

def inicializar_directorios(data_dir):
    """Inicializa el directorio de almacenamiento de datos."""
    os.makedirs(data_dir, exist_ok=True)

def listar_archivos_disponibles(data_dir, traducciones):
    """Lista archivos en el directorio especificado que cumplen con el formato de nombre."""
    directorio_completo = os.path.abspath(data_dir)
    print(f"Buscando archivos en: {directorio_completo}")
    
    archivos = []
    for root, dirs, files in os.walk(directorio_completo):
        for file in files:
            if file.startswith("MeteoData_") and file.endswith((".xlsx", ".xlsm")):
                archivos.append(os.path.join(root, file))

    if not archivos:
        print(traducciones["no_files_available"])
        return None
    
    print(traducciones["available_files"])
    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    while True:
        try:
            seleccion = int(input(traducciones["select_file"])) - 1
            if 0 <= seleccion < len(archivos):
                return archivos[seleccion]
            else:
                print(traducciones["selection_out_of_range"])
        except ValueError:
            print(traducciones["invalid_input"])

def cargar_excel(archivo_seleccionado):
    """Carga un archivo Excel y retorna sus hojas disponibles."""
    try:
        excel_file = pd.ExcelFile(archivo_seleccionado)
        hojas_disponibles = excel_file.sheet_names
        return excel_file, hojas_disponibles
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
        return None, []

def cargar_shapefile(shapefile_path, traducciones):
    """Carga un archivo shapefile y retorna el objeto GeoDataFrame."""
    if not os.path.exists(shapefile_path):
        print(f"Error: No se encontró el archivo de shapes en '{shapefile_path}'.")
        exit()
    try:
        return gpd.read_file(shapefile_path)
    except Exception as e:
        print(traducciones["error_loading_shapefile"])
        print(f"Detalles del error: {e}")
        exit()

def copiar_plantilla_si_no_existe(fecha, plantilla, data_dir):
    """Copia la plantilla a la ubicación de destino solo si el archivo no existe."""
    fecha_str = fecha.strftime('%Y%m%d')
    archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha_str}.xlsm")

    # Si el archivo de destino ya existe, no lo sobrescribimos
    if os.path.exists(archivo_destino):
        print(f"Archivo ya existente: {archivo_destino}. No se creará una nueva copia.")
        return archivo_destino

    archivo_temp = os.path.join(os.getenv('TEMP'), f"MeteoData_{fecha_str}_temp.xlsm")
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False

    try:
        # Verificar si la plantilla existe
        if not os.path.exists(plantilla):
            print(f"Error: La plantilla {plantilla} no se encuentra.")
            return None

        workbook = excel.Workbooks.Open(plantilla)
        workbook.SaveAs(archivo_temp, FileFormat=52)  # 52 es el formato para .xlsm
        workbook.Close(False)

        # Mover la copia temporal al destino final
        os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)
        shutil.move(archivo_temp, archivo_destino)
        
        print(f"Copia de la plantilla creada en: {archivo_destino}")
        return archivo_destino
    except Exception as e:
        print(f"Ocurrió un error al copiar la plantilla: {e}")
        return None
    finally:
        excel.Quit()

def obtener_fechas_disponibles_api(latitud, longitud, api_settings):
    """Obtiene las fechas disponibles desde la API de Open-Meteo utilizando la configuración de API."""
    url = f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}"
    for intento in range(5):  # Máximo 5 reintentos
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('daily', {}).get('time', [])
        elif response.status_code == 429:
            print("Demasiadas solicitudes. Esperando para reintentar...")
            time.sleep(5)
        else:
            print(f"Error en la solicitud. Código de estado: {response.status_code}")
            input("Presione Enter para continuar...")
            return []
    print("Se alcanzó el número máximo de reintentos.")
    input("Presione Enter para continuar...")
    return []

def obtener_datos_meteo(latitud, longitud, fecha, api_settings):
    """Obtiene los datos meteorológicos de la API para la fecha y coordenadas especificadas."""
    fecha_str = fecha.strftime('%Y-%m-%d')
    url = (f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}"
           f"&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}")
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        if fecha_str in datos['daily']['time']:
            index = datos['daily']['time'].index(fecha_str)
            return {
                'temperature_min': datos['daily']['temperature_2m_min'][index],
                'temperature_max': datos['daily']['temperature_2m_max'][index],
                'windspeed_max': datos['daily']['windspeed_10m_max'][index],
                'windgusts_max': datos['daily']['windgusts_10m_max'][index],
                'winddirection_dominant': datos['daily']['winddirection_10m_dominant'][index],
                'precipitation_sum': datos['daily']['precipitation_sum'][index]
            }
        else:
            print(f"Datos no disponibles para la fecha: {fecha_str}")
            return None
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        input("Presione Enter para continuar...")
        return None

def seleccionar_comunidad(config, traducciones):
    """Permite seleccionar una comunidad autónoma a partir de la configuración."""
    comunidades = config.get("comunidades", [])
    if not comunidades:
        print(traducciones["no_communities_found"])
        input("Presione Enter para continuar...")
        return None

    print(traducciones["select_community"])
    for i, comunidad in enumerate(comunidades, start=1):
        print(f"{i}. {comunidad}")

    while True:
        try:
            seleccion = int(input(traducciones["select_community_option"])) - 1
            if 0 <= seleccion < len(comunidades):
                return comunidades[seleccion]
            else:
                print(traducciones["invalid_selection"])
        except ValueError:
            print(traducciones["invalid_input"])
