import os
import csv
from pymongo import MongoClient
from dotenv import load_dotenv
import win32com.client as win32
import json
import datetime
import sys
import time
from bson import ObjectId

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Cargar configuración desde config.json
def cargar_configuracion(ruta_config):
    with open(ruta_config) as config_file:
        return json.load(config_file)

# Configuración de MongoDB
MONGO_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION")

# Conectar a MongoDB y obtener la colección
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Cargar configuración del proyecto
config = cargar_configuracion(os.path.join(os.getenv("PROJECT_PATH"), "config", "config.json"))
DATA_DIRECTORY = config.get("data_directory")  # Obtener el data_directory del config.json
PROJECT_PATH = os.getenv("PROJECT_PATH")  # Obtener la ruta del proyecto
COMUNIDADES = config.get("comunidades")  # Obtener la lista de comunidades

def fecha_consulta():
    fecha_string = sys.argv[1]  # Suponiendo que la fecha está en el primer argumento
    fecha_consulta = datetime.datetime.strptime(fecha_string, '%d/%m/%Y')  # Ajustar al formato correcto
    return fecha_consulta

def obtener_datos(filtro=None):
    """Obtiene datos de la colección de MongoDB según el filtro especificado."""
    try:
        datos = collection.find(filtro or {})
        return list(datos)  # Convertir a lista para poder reutilizar
    except Exception as e:
        print("Error al obtener datos de MongoDB:", e)
        return []

def insertar_datos(datos):
    """Inserta datos en la colección de MongoDB."""
    try:
        if isinstance(datos, list):
            db[COLLECTION_NAME].insert_many(datos)
        else:
            db[COLLECTION_NAME].insert_one(datos)
        print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error al insertar datos en MongoDB: {e}")

def exportar_datos_a_csv():

    """Exporta datos de MongoDB a un archivo CSV con codificación UTF-8."""
    # Filtrar datos para la fecha especificada
    filtro = {"fecha": fecha_consulta().strftime('%Y-%m-%d')}  # Agregar filtro por fecha
    datos = obtener_datos(filtro)

    # Resto de tu lógica para exportar a CSV
    ruta_csv = os.path.join(os.getenv("TEMP_PATH"), "datos_exportados.csv")  # Ruta del archivo CSV en la carpeta temp

    with open(ruta_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir encabezados
        writer.writerow(["localidad_id", "fecha", "temperature_2m_max", "precipitation_sum", "temperature_2m_min", "windspeed_10m_max", "windgusts_10m_max"])

        for dato in datos:
            writer.writerow([
                dato.get("localidad_id"),
                dato.get("fecha"),
                dato.get("metrics", {}).get("temperature_2m_max", ""),
                dato.get("metrics", {}).get("precipitation_sum", ""),
                dato.get("metrics", {}).get("temperature_2m_min", ""),
                dato.get("metrics", {}).get("windspeed_10m_max", ""),
                dato.get("metrics", {}).get("windgusts_10m_max", "")
            ])
            #print(f"Escribiendo dato: {dato.get('localidad_id')}, {dato.get('fecha')}")

    print(f"Datos exportados a {ruta_csv}")

def exportar_datos_a_excel():
    """Importa datos desde el archivo CSV a las hojas de Excel correspondientes a cada comunidad autónoma."""
    # Conectar a Excel
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = True  # Mostrar Excel durante la ejecución

    # Construir la ruta del archivo CSV
    ruta_csv = os.path.join(os.getenv("TEMP_PATH"), "datos_exportados.csv")  # Ruta del archivo CSV en la carpeta temp

    # Leer datos del CSV
    datos = []
    with open(ruta_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Leer el CSV como diccionario
        for row in reader:
            datos.append(row)

    # Inicializar wb
    wb = None

    # Intentar abrir el libro de Excel
    try:
        año = str(fecha_consulta().year)  # Obtener el año de la fecha
        mes = str(fecha_consulta().month).zfill(2)  # Asegurar que el mes esté en formato 2 dígitos
        plantilla_path = os.path.join(PROJECT_PATH, DATA_DIRECTORY, año, mes, f"MeteoData_{fecha_consulta().strftime('%Y%m%d')}.xlsm")
        wb = excel.Workbooks.Open(plantilla_path)  # Abrir el archivo de plantilla correcto
        print("Libro de Excel abierto correctamente.")
    except Exception as e:
        print(f"Error al abrir el libro de Excel: {e}")
        return  # Salir de la función si hay un error
    # Iterar sobre las comunidades y exportar datos
    for comunidad in COMUNIDADES:
        try:
            # Verificar si la hoja de la comunidad existe
            ws_comunidad = wb.Sheets(comunidad)  # Esto lanzará un error si no existe

            print(f"Accediendo a la hoja: {comunidad}")

            # Limpiar datos de la hoja (sobreescribir a partir de la fila 2)
            ws_comunidad.Range("H2:K1048576").ClearContents()  # Limpiar solo desde H en adelante

            # Filtrar los datos para la comunidad actual
            ids_comunidad = [localidad.get('_id') for localidad in db.Localidades.find({"comunidad_autonoma": comunidad})]
            datos_comunidad = [dato for dato in datos if ObjectId(dato.get("localidad_id")) in ids_comunidad]
            next_row = 1

            for dato in datos_comunidad:
                # Usar el oid en lugar del id
                fecha = dato.get("fecha", "")
                metrics = {
                    "temperature_2m_max": dato.get("temperature_2m_max", ""),
                    "precipitation_sum": dato.get("precipitation_sum", ""),
                    "temperature_2m_min": dato.get("temperature_2m_min", ""),
                    "windspeed_10m_max": dato.get("windspeed_10m_max", ""),
                    "windgusts_10m_max": dato.get("windgusts_10m_max", ""),
                }

                # Determinar la fila en la hoja para insertar los datos
                next_row = next_row + 1
                # Insertar los datos en las columnas correspondientes
                ws_comunidad.Cells(next_row, 14).Value = fecha  # Columna N
                ws_comunidad.Cells(next_row, 9).Value = metrics.get("temperature_2m_max", "")  # Columna I
                ws_comunidad.Cells(next_row, 13).Value = metrics.get("precipitation_sum", "")  # Columna M
                ws_comunidad.Cells(next_row, 8).Value = metrics.get("temperature_2m_min", "")  # Columna H
                ws_comunidad.Cells(next_row, 10).Value = metrics.get("windspeed_10m_max", "")  # Columna J
                ws_comunidad.Cells(next_row, 11).Value = metrics.get("windgusts_10m_max", "")  # Columna K

        except Exception as e:
            print(f"Error al acceder a la hoja {comunidad}: {e}")

    # Guardar el libro y cerrarlo
    if wb is not None:
        wb.Save()

    # Permitir al usuario trabajar en el libro después de la ejecución
    print("Los datos han sido exportados a las hojas de Excel. Puedes revisar los cambios.")

if __name__ == "__main__":
    exportar_datos_a_csv()  # Llama a la función para exportar datos a CSV
    exportar_datos_a_excel()  # Llama a la función para exportar datos a Excel
