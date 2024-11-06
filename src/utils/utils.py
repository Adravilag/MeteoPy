# utils.py
import os
import json
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def obtener_rutas():
    """Devuelve las rutas principales del proyecto."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_path = os.path.join(project_root, 'config', 'config.json')
    return project_root, config_path

def cls():
    """Limpia la pantalla."""
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_configuracion(config_path):
    """Carga la configuración desde el archivo JSON especificado."""
    print("Ruta recibida para config_path en cargar_configuracion:", config_path)  # Añadir para depuración
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: El archivo de configuración no se encuentra en la ruta especificada.")
        exit()
    except json.JSONDecodeError:
        print("Error: El archivo de configuración tiene un formato JSON no válido.")
        exit()

def cargar_traducciones(idioma="es"):
    """Carga el archivo de traducciones en el idioma especificado."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    locales_dir = os.path.join(project_root, 'locales')
    idioma_path = os.path.join(locales_dir, f"{idioma}.json")

    try:
        with open(idioma_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Traducciones para '{idioma}' no encontradas en {idioma_path}. Usando español por defecto.")
        return {}  # Retorna un diccionario vacío o uno predeterminado para evitar más errores

def inicializar_directorios(data_dir):
    """Inicializa el directorio de almacenamiento de datos."""
    os.makedirs(data_dir, exist_ok=True)

def listar_archivos_disponibles(data_dir, traducciones, imprimir=True):
    """Lista los archivos disponibles en el directorio de datos y permite seleccionar uno."""
    directorio_completo = os.path.abspath(data_dir)
    archivos = []

    for root, dirs, files in os.walk(directorio_completo):
        for file in files:
            if file.startswith("MeteoData_") and (file.endswith(".xlsx") or file.endswith(".xlsm")):
                archivos.append(os.path.join(root, file))

    if not archivos:
        print(traducciones["no_files_available"])
        return None

    if imprimir:  # Solo imprime si 'imprimir' es True
        print(traducciones["available_files"])
        for i, archivo in enumerate(archivos, start=1):
            print(f"{i}. {os.path.basename(archivo)}")
    
    return archivos

def cargar_shapefile(shapefile_path, traducciones):
    """Carga un shapefile en un GeoDataFrame."""
    if not os.path.exists(shapefile_path):
        print(f"{traducciones['shapefile_not_found']} {shapefile_path}")
        exit()
    try:
        return gpd.read_file(shapefile_path)
    except Exception as e:
        print(traducciones["error_loading_shapefile"], e)
        exit()
