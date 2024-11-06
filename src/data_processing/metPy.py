# metPy.py

import os
import pandas as pd
import win32com.client as win32
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils.utils import cargar_configuracion, cargar_traducciones
import time

def main(config, traducciones):
    # Configuración del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.abspath(config.get("data_directory", "data"))
    plantilla = os.getenv("TEMPLATE_PATH", os.path.join(project_root, "config", "templates", "MeteoData_Template.xlsm"))
    api_settings = config.get("api_settings", {})

    def obtener_fechas_disponibles_api(latitud, longitud):
        """Obtiene las fechas de pronóstico disponibles desde la API de Open-Meteo."""
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
                return []
        print("Se alcanzó el número máximo de reintentos.")
        return []
    
    def obtener_datos_meteo(latitud, longitud, fecha):
        """Obtiene datos meteorológicos para una fecha y coordenadas específicas desde la API."""
        fecha_str = fecha.strftime('%Y-%m-%d')
        url = (f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}"
               f"&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}")
        
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            if fecha_str in datos['daily']['time']:
                index = datos['daily']['time'].index(fecha_str)
                return {param: datos['daily'][param][index] for param in api_settings['daily_params']}
            else:
                print(f"No se encontraron datos para la fecha {fecha_str}")
        else:
            print(f"Error al obtener datos para la fecha {fecha_str}: {response.status_code}")
        return None    

    def copiar_plantilla(fecha):
        """Copia la plantilla si no existe un archivo de datos para la fecha dada."""
        # Asegurarse de que la ruta de la plantilla es correcta
        if not os.path.exists(plantilla):
            print(f"Error: La plantilla no se encuentra en la ruta especificada: {plantilla}")
            return None

        archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha.strftime('%Y%m%d')}.xlsm")
        if os.path.exists(archivo_destino):
            print(f"{traducciones['file_exists']} {archivo_destino}")
            return archivo_destino

        try:
            # Usar DispatchEx para iniciar una nueva instancia de Excel
            excel = win32.DispatchEx("Excel.Application")
            workbook = excel.Workbooks.Open(plantilla)
            workbook.SaveAs(archivo_destino, FileFormat=52)
            workbook.Close(False)
            print(f"{traducciones['template_copied']} {archivo_destino}")
            return archivo_destino
        except Exception as e:
            print(f"{traducciones['error_copy_template']}: {e}")
            return None
        finally:
            try:
                excel.Quit()  # Asegúrate de cerrar Excel correctamente
            except Exception as e:
                print(f"Error al cerrar Excel: {e}")

    def listar_fechas_disponibles(comunidad, latitud, longitud):
        """Lista las fechas disponibles desde la API y verifica si están completas o incompletas en los archivos locales."""
        fechas_api = obtener_fechas_disponibles_api(latitud, longitud)
        if not fechas_api:
            print(traducciones["no_dates_found"])
            return []

        fechas_disponibles = []
        for fecha_str in fechas_api:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha.strftime('%Y%m%d')}.xlsm")
            
            if os.path.exists(archivo_destino):
                ultima_actualizacion = datetime.fromtimestamp(os.path.getmtime(archivo_destino)).strftime('%Y-%m-%d %H:%M:%S')
                datos_completos = verificar_datos_completos(archivo_destino, comunidad)
                estado = "Completa" if datos_completos else "Incompleta"
            else:
                ultima_actualizacion = "No disponible"
                estado = "Incompleta"

            fechas_disponibles.append((fecha, ultima_actualizacion, estado))

        return sorted(fechas_disponibles, key=lambda x: x[0])

    def verificar_datos_completos(archivo, comunidad):
        """Verifica si la hoja de la comunidad tiene datos completos."""
        excel = None
        workbook = None
        try:
            excel = win32.DispatchEx("Excel.Application")
            workbook = excel.Workbooks.Open(archivo)
            ws = workbook.Sheets(comunidad)
            datos_completos = all(ws.Cells(row, 8).Value for row in range(2, ws.UsedRange.Rows.Count + 1))
            return datos_completos
        except Exception as e:
            print(f"Error al verificar datos: {e}")
            return False
        finally:
            if workbook:
                workbook.Close(False)
            if excel:
                try:
                    excel.Quit()
                except Exception as e:
                    print("Error al cerrar Excel:", e)

    def procesar_datos(fecha, comunidad):
        archivo_destino = copiar_plantilla(fecha)
        if not archivo_destino:
            return

        excel = win32.DispatchEx("Excel.Application")
        try:
            workbook = excel.Workbooks.Open(archivo_destino)
            ws = workbook.Sheets(comunidad)
            for row in range(2, ws.UsedRange.Rows.Count + 1):
                coordenadas = ws.Cells(row, 3).Value
                if coordenadas:
                    latitud, longitud = map(float, coordenadas.split(', '))
                    datos = obtener_datos_meteo(latitud, longitud, fecha)
                    if datos:
                        for i, param in enumerate(api_settings['daily_params'], start=8):
                            ws.Cells(row, i).Value = datos[param]
                        ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            workbook.Save()
            print(f"Datos meteorológicos guardados en {archivo_destino}")
        except Exception as e:
            print(f"Error al procesar el archivo de datos: {e}")
        finally:
            if workbook:
                workbook.Close(False)
            if excel:
                try:
                    excel.Quit()
                except Exception as e:
                    print("Error al cerrar Excel:", e)

    def mostrar_comunidades(comunidades):
        print("\n--- Comunidades Autónomas disponibles ---")
        for i, comunidad in enumerate(comunidades, start=1):
            print(f"{i}. {comunidad}")

    def menu_principal():
        comunidades = config.get("comunidades", [])
        mostrar_comunidades(comunidades)
        
        while True:
            try:
                seleccion_comunidad = int(input(traducciones["select_community_option"])) - 1
                if 0 <= seleccion_comunidad < len(comunidades):
                    comunidad = comunidades[seleccion_comunidad]
                    break
                else:
                    print(traducciones["selection_out_of_range"])
            except ValueError:
                print(traducciones["invalid_input"])

        latitud, longitud = 37.3891, -5.9845  # Coordenadas de ejemplo
        fechas_disponibles = listar_fechas_disponibles(comunidad, latitud, longitud)
        if not fechas_disponibles:
            print(traducciones["no_dates_found"])
            return

        print(traducciones["select_date_option"])
        for i, (fecha, ultima_actualizacion, estado) in enumerate(fechas_disponibles, start=1):
            print(f"{i}. {fecha.strftime('%Y-%m-%d')} - Última actualización: {ultima_actualizacion} - Estado: {estado}")

        while True:
            try:
                seleccion_fecha = int(input(traducciones["select_date_option"])) - 1
                if 0 <= seleccion_fecha < len(fechas_disponibles):
                    fecha = fechas_disponibles[seleccion_fecha][0]
                    break
                else:
                    print(traducciones["selection_out_of_range"])
            except ValueError:
                print(traducciones["invalid_input"])

        procesar_datos(fecha, comunidad)

    # Ejecutar el menú principal
    menu_principal()

if __name__ == "__main__":
    load_dotenv()  # Carga las variables del .env
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_path = os.path.join(project_root, 'config', 'config.json')
    config = cargar_configuracion(config_path)
    traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(project_root, 'locales'))
    
    main(config, traducciones)
