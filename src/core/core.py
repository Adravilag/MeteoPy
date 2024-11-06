import os
from datetime import datetime
from src.utils.utils import (
    cls,
    cargar_configuracion,
    cargar_traducciones,
    inicializar_directorios,
    copiar_plantilla_si_no_existe,
    obtener_fechas_disponibles_api,
    obtener_datos_meteo
)
import win32com.client as win32

def menu_principal(config, plantilla, data_dir, api_settings):
    """Función principal del menú para procesar datos meteorológicos."""
    latitud, longitud = 37.3891, -5.9845
    fechas_disponibles = obtener_fechas_disponibles_api(latitud, longitud, api_settings)

    if not fechas_disponibles:
        print("No se encontraron fechas disponibles.")
        input("Presione Enter para continuar...")
        return

    while True:
        print("\n--- Menú Principal ---")
        print("1. Procesar datos meteorológicos")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("\nFechas disponibles:")
            for i, fecha in enumerate(fechas_disponibles, start=1):
                print(f"{i}. {fecha}")

            while True:
                try:
                    seleccion_fecha = int(input("Seleccione una fecha (por número): ")) - 1
                    if 0 <= seleccion_fecha < len(fechas_disponibles):
                        fecha = datetime.strptime(fechas_disponibles[seleccion_fecha], '%Y-%m-%d')
                        break
                    else:
                        print("Selección fuera de rango.")
                except ValueError:
                    print("Entrada inválida. Intente nuevamente.")

            # Seleccionar comunidad autónoma
            comunidad = seleccionar_comunidad(config)
            if comunidad is None:
                print("No se seleccionó ninguna comunidad.")
                continue

            # Procesar datos con la fecha y comunidad seleccionada
            procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings)

            input("Procesamiento completado. Presione Enter para ver los resultados...")

        elif opcion == '2':
            print("Saliendo...")
            break
        else:
            print("Selección inválida.")
            input("Presione Enter para continuar...")

def seleccionar_comunidad(config):
    """Permite seleccionar una comunidad autónoma desde la configuración."""
    comunidades = config.get("comunidades", [])
    if not comunidades:
        print("No se encontraron comunidades en la configuración.")
        input("Presione Enter para continuar...")
        return None

    print("Seleccione una comunidad autónoma:")
    for i, comunidad in enumerate(comunidades, start=1):
        print(f"{i}. {comunidad}")

    while True:
        try:
            seleccion = int(input("Seleccione una opción: ")) - 1
            if 0 <= seleccion < len(comunidades):
                return comunidades[seleccion]
            else:
                print("Selección fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

def procesar_datos(fecha, comunidad, plantilla, data_dir, api_settings):
    """Procesa los datos meteorológicos para la fecha y comunidad especificada."""
    archivo_destino = copiar_plantilla_si_no_existe(fecha, plantilla, data_dir)

    # Verificar si el archivo de destino existe antes de intentar abrirlo
    if not archivo_destino or not os.path.exists(archivo_destino):
        print(f"Error: El archivo {archivo_destino} no se pudo crear o no existe.")
        return

    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False  # Oculta Excel durante el procesamiento
    wb = None

    try:
        print(f"Intentando abrir el archivo de destino: {archivo_destino}")
        wb = excel.Workbooks.Open(archivo_destino)  # Abrir archivo de destino
        ws = wb.Sheets(comunidad)
        fecha_str = fecha.strftime('%Y-%m-%d')

        # Llenar datos en el Excel
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

# Ejecución principal
if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
    config = cargar_configuracion(config_path)
    traducciones = cargar_traducciones(config.get("language", "es"), os.path.join(os.path.dirname(__file__), '..', '..', 'locales'))
    data_dir = config.get("data_directory", "data")
    plantilla = config.get("template_path", "config/templates/MeteoData_Template.xlsm")
    api_settings = config.get("api_settings", {})
    
    inicializar_directorios(data_dir)
    cls()
    menu_principal(config, plantilla, data_dir, api_settings)
