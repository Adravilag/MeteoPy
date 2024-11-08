import os
import pandas as pd
import win32com.client as win32
import requests
from datetime import datetime
from dotenv import load_dotenv
from utils.utils import cargar_configuracion, cargar_traducciones
import time
from database.db_connector import insertar_datos, db
from bson import ObjectId

def main(config, traducciones):
    # Configuración del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.abspath(config.get("data_directory", "data"))
    plantilla = os.getenv("TEMPLATE_PATH", os.path.join(project_root, "config", "templates", "MeteoData_Template.xlsm"))
    api_settings = config.get("api_settings", {})

    def obtener_fechas_disponibles_api(latitud, longitud):
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
        fecha_str = fecha.strftime('%Y-%m-%d')
        url = (f"{api_settings['base_url']}?latitude={latitud}&longitude={longitud}&daily={','.join(api_settings['daily_params'])}&timezone={api_settings['timezone']}")
        
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            if fecha_str in datos['daily']['time']:
                index = datos['daily']['time'].index(fecha_str)
                result = {param: datos['daily'][param][index] for param in api_settings['daily_params']}
                # print(f"Datos obtenidos para {fecha_str}: {result}")  # Línea de depuración
                return result
            else:
                print(f"No se encontraron datos para la fecha {fecha_str}")
        else:
            print(f"Error al obtener datos para la fecha {fecha_str}: {response.status_code}")
        return None    

    def copiar_plantilla(fecha):
        if not os.path.exists(plantilla):
            print(f"Error: La plantilla no se encuentra en la ruta especificada: {plantilla}")
            return None

        archivo_destino = os.path.join(data_dir, fecha.strftime('%Y'), fecha.strftime('%m'), f"MeteoData_{fecha.strftime('%Y%m%d')}.xlsm")
        if os.path.exists(archivo_destino):
            print(f"{traducciones['file_exists']} {archivo_destino}")
            return archivo_destino

        try:
            excel = win32.DispatchEx("Excel.Application")
            workbook = excel.Workbooks.Open(plantilla)
            workbook.SaveAs(archivo_destino, FileFormat=52)
            workbook.Close(False)
            print(f"{traducciones['template_copied']} {archivo_destino}")

            # Establecer la fecha en la celda F2 de la hoja "Macros"
            workbook = excel.Workbooks.Open(archivo_destino)
            ws_macros = workbook.Sheets("Macros")
            # Establecer la fecha en la celda F2 de la hoja "Macros"
            ws_macros.Range("F2").Value = fecha.strftime('%d/%m/%Y')  # Esto convierte a string
            ws_macros.Range("F2").NumberFormat = "dd/mm/yy"  # Establecer el formato de la celda
            workbook.Save()
            workbook.Close(False)

            return archivo_destino
        except Exception as e:
            print(f"{traducciones['error_copy_template']}: {e}")
            return None
        finally:
            try:
                excel.Quit()
            except Exception as e:
                print(f"Error al cerrar Excel: {e}")

    def listar_fechas_disponibles(comunidad, latitud, longitud):
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

    def obtener_localidad_id(nombre_localidad, comunidad_autonoma, provincia, oid):
        """Obtiene el ObjectId de la localidad desde la colección Localidades o la crea si no existe."""
        resultado = db.Localidades.find_one({"nombre": nombre_localidad})
        if resultado:
            # print(f"localidad_id encontrado para {nombre_localidad}: {resultado['_id']}")  # Línea de depuración
            return resultado["_id"]
        else:
            # Si no se encuentra la localidad, la agregamos con la comunidad autónoma, la provincia y el oid
            nuevo_documento = {
                "nombre": nombre_localidad,
                "comunidad_autonoma": comunidad_autonoma,
                "provincia": provincia,
                "oid": oid
            }
            db.Localidades.insert_one(nuevo_documento)
            nuevo_id = nuevo_documento["_id"]  # Obtenemos el ID del nuevo documento
            # print(f"Localidad {nombre_localidad} creada con id: {nuevo_id}")  # Línea de depuración
            return nuevo_id

    def procesar_datos(fecha, comunidad):
        archivo_destino = copiar_plantilla(fecha)
        if not archivo_destino:
            return

        excel = win32.DispatchEx("Excel.Application")
        try:
            workbook = excel.Workbooks.Open(archivo_destino)
            ws = workbook.Sheets(comunidad)
            datos_mongodb = []  # Lista para almacenar los datos que se subirán a MongoDB

            for row in range(2, ws.UsedRange.Rows.Count + 1):
                localidad = ws.Cells(row, 2).Value  # Nombre de la localidad en la columna B
                coordenadas = ws.Cells(row, 3).Value
                oid = ws.Cells(row, 1).Value  # Obtener el OID de la columna A
                provincia = ws.Cells(row, 5).Value  # Suponiendo que la provincia está en la columna E
                
                if localidad and coordenadas:
                    latitud, longitud = map(float, coordenadas.split(', '))
                    localidad_id = obtener_localidad_id(localidad, comunidad, provincia, oid)  # Pasar la comunidad autónoma, la provincia y el oid al crear la localidad
                    if localidad_id:
                        datos = obtener_datos_meteo(latitud, longitud, fecha)
                        if datos:
                            # print(f"Datos meteorológicos para {localidad}: {datos}")  # Línea de depuración
                            for i, param in enumerate(api_settings['daily_params'], start=8):
                                ws.Cells(row, i).Value = datos[param]
                            ws.Cells(row, 14).Value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            
                            # Preparar los datos para MongoDB
                            datos_mongodb.append({
                                "localidad_id": localidad_id,  # Almacena la referencia a la localidad
                                "fecha": fecha.strftime('%Y-%m-%d'),
                                "metrics": datos
                            })

            workbook.Save()
            print(f"Datos meteorológicos guardados en {archivo_destino}")

            # Subir los datos a MongoDB
            if datos_mongodb:
                print("Datos a subir a MongoDB:", datos_mongodb)  # Línea de depuración
                insertar_datos(datos_mongodb)
                print("Datos subidos a MongoDB exitosamente.")
            else:
                print("No hay datos para subir a MongoDB.")

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
