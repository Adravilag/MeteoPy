import os
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.widgets import Button
from datetime import datetime
import time

# Cargar configuración desde archivo JSON
def cargar_configuracion():
    try:
        with open("config/config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Error: El archivo config.json no se encuentra en la ruta especificada.")
        exit()
    except json.JSONDecodeError:
        print("Error: El archivo config.json tiene un formato JSON no válido.")
        exit()

# Inicializar parámetros desde la configuración
config = cargar_configuracion()

# Definir el directorio de datos y otros parámetros
data_dir = config.get("data_directory", "Data")
shapefile_path = config.get("shapefile_path", "/config/shp/gadm41_ESP_4.shp")
base_size = config.get("base_size", 10)
max_point_size = config.get("max_point_size", 500)
min_point_size = config.get("min_point_size", 5)
label_threshold = config.get("label_threshold", 400)
original_xlim = tuple(config.get("map_xlim", [-7.6, -1.5]))
original_ylim = tuple(config.get("map_ylim", [35.8, 39]))

# Verificar si el archivo shapefile existe, usando ruta absoluta si es necesario
if not os.path.exists(shapefile_path):
    abs_shapefile_path = os.path.abspath(shapefile_path)
    if os.path.exists(abs_shapefile_path):
        shapefile_path = abs_shapefile_path
    else:
        print(f"Error: No se encontró el archivo de shapes en '{shapefile_path}' ni en '{abs_shapefile_path}'.")
        exit()

# Cargar el shapefile de España y filtrar Andalucía y Comunidad Valenciana
try:
    espana_shapefile = gpd.read_file(shapefile_path)
    comunidades = {
        "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Andalucía'],
        "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']  # Ajuste aquí para asegurar coincidencia exacta
    }
except Exception as e:
    print(f"Error al cargar el archivo de shapes: {e}")
    exit()

# Definir la unidad de medida para cada tipo de dato
unit_dict = {
    "temperature_min": "°C",
    "temperature_max": "°C",
    "wind_gusts": "km/h",
    "wind_speed": "km/h",
    "precipitation_sum": "mm"
}

# Listar archivos disponibles en el directorio de datos y permitir selección
def listar_archivos_disponibles():
    archivos = [f for f in os.listdir(data_dir) if f.startswith("MeteoData_") and f.endswith(".xlsx")]
    if not archivos:
        print("No hay archivos disponibles en el directorio 'Data'.")
        return None
    
    print("Archivos disponibles:")
    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {archivo}")
    
    while True:
        try:
            seleccion = int(input("Selecciona el número del archivo a utilizar: ")) - 1
            if 0 <= seleccion < len(archivos):
                return archivos[seleccion]
            else:
                print("Selección fuera de rango. Intenta nuevamente.")
        except ValueError:
            print("Entrada no válida. Introduce un número.")

# Seleccionar el archivo de datos
archivo_seleccionado = listar_archivos_disponibles()
if archivo_seleccionado is None:
    exit()  # Terminar si no hay archivos disponibles

# Extraer la fecha del nombre del archivo
try:
    fecha_archivo = archivo_seleccionado.split('_')[1].split('.')[0]
    fecha_formateada = f"{fecha_archivo[:4]}-{fecha_archivo[4:6]}-{fecha_archivo[6:]}"
except IndexError:
    print("Error: El archivo seleccionado no tiene la fecha en el formato esperado.")
    exit()

# Cargar el archivo Excel seleccionado y listar las hojas disponibles
archivo_path = os.path.join(data_dir, archivo_seleccionado)
excel_file = pd.ExcelFile(archivo_path)
hojas_disponibles = excel_file.sheet_names

print("\nComunidades Autónomas disponibles:")
for i, hoja in enumerate(hojas_disponibles, start=1):
    print(f"{i}. {hoja}")

# Permitir que el usuario seleccione la hoja (comunidad autónoma)
while True:
    try:
        seleccion_hoja = int(input("Selecciona la comunidad autónoma (por número): ")) - 1
        if 0 <= seleccion_hoja < len(hojas_disponibles):
            sheet_name = hojas_disponibles[seleccion_hoja]
            break
        else:
            print("Selección fuera de rango. Intenta nuevamente.")
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número.")

# Cargar los datos desde la hoja seleccionada
df = pd.read_excel(archivo_path, sheet_name=sheet_name)

# Asegúrate de que las columnas de coordenadas están en el formato correcto
df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(', ', expand=True).astype(float)

# Seleccionar la región en el mapa según la comunidad seleccionada
region_map = comunidades.get(sheet_name.upper(), None)  # Convertir a mayúsculas para coincidencia
if region_map is None or region_map.empty:
    print(f"Error: No se encontró la región correspondiente para '{sheet_name}' en el shapefile.")
    exit()  # Terminar si no se encuentra la región

# Crear una figura
fig, ax1 = plt.subplots(figsize=(10, 8))
fig.canvas.manager.set_window_title(f"Mapa de {sheet_name} - Datos Meteorológicos")

# Crear una variable global para almacenar la selección actual
selected_data = 'temperature_min'  # Opción predeterminada: temperatura mínima

scatter_points = []
name_points = [(row['Name'], row['Longitude'], row['Latitude'], label_threshold, None, None) for _, row in df.iterrows()]

# Configuración de los límites iniciales para la Comunidad Valenciana
valencia_xlim = (-2, 3)  # Ajuste de longitud para que Valencia se vea mejor
valencia_ylim = (37.5, 41)  # Ajuste de latitud para que Valencia se vea mejor

# Función de actualización con coordenadas iniciales ajustadas para Valencia
def update_scatter():
    ax1.clear()
    region_map.boundary.plot(ax=ax1, linewidth=0.5, color='lightgray')

    # Ajustar la vista inicial a los límites de Valencia si se selecciona Valencia
    if sheet_name.upper() == "VALENCIA":
        ax1.set_xlim(valencia_xlim)
        ax1.set_ylim(valencia_ylim)
    else:
        ax1.set_xlim(original_xlim)
        ax1.set_ylim(original_ylim)

    ax1.set_xlabel('Longitud')
    ax1.set_ylabel('Latitud')
    
    # Configuración para el tipo de datos seleccionado
    if selected_data == 'temperature_min':
        data = df['Min Temperature']
        title = 'Temperatura Mínima (°C)'
        cmap = 'Blues'
    elif selected_data == 'temperature_max':
        data = df['Max Temperature']
        title = 'Temperatura Máxima (°C)'
        cmap = 'Reds'
    elif selected_data == 'wind_gusts':
        data = df['Maximum wind gusts']
        title = 'Rachas de Viento (km/h)'
        cmap = 'Purples'
    elif selected_data == 'wind_speed':
        data = df['Maximum wind speed']
        title = 'Velocidad del Viento (km/h)'
        cmap = 'Greens'
    elif selected_data == 'precipitation_sum':
        data = df['Precipitation']
        title = 'Precipitación Acumulada (mm)'
        cmap = 'Blues'

    norm = Normalize(vmin=data.min(), vmax=data.max())
    scatter_points.clear()
    
    for i, row in df.iterrows():
        if pd.isnull(data[i]):
            continue
        
        current_data = data[i]
        color = plt.get_cmap(cmap)(norm(current_data))
        
        point_size = min_point_size + (max_point_size - min_point_size) * (current_data - data.min()) / (data.max() - data.min())

        scatter = ax1.scatter(row['Longitude'], row['Latitude'], color=color, s=point_size, alpha=0.7)
        scatter_points.append((scatter, point_size))
        name_points[i] = (row['Name'], row['Longitude'], row['Latitude'], label_threshold, point_size, current_data)
    
    ax1.set_title(f'{sheet_name} - {title} - {fecha_formateada}')
    update_labels()
    fig.canvas.draw_idle()

# Función para actualizar etiquetas de nombres usando el umbral y zoom
def update_labels():
    zoom_level = abs(ax1.get_xlim()[1] - ax1.get_xlim()[0])
    
    for label in ax1.texts:
        label.remove()
    
    for locality, lon, lat, threshold, size, value in name_points:
        if size and size >= threshold:
            if zoom_level < 2:
                ax1.text(lon, lat, f"{locality}", 
                         fontsize=8, ha='center', va='bottom', alpha=0.8)
            else:
                ax1.text(lon, lat, locality, fontsize=8, ha='center', va='bottom', alpha=0.8)

fig.canvas.mpl_connect('draw_event', lambda event: update_labels())

subtitle_text = ax1.text(0.5, -0.1, '', fontsize=10, ha='center', va='center', color='black', 
                          bbox=dict(boxstyle='round,pad=0.5', edgecolor='none', facecolor='white'), transform=ax1.transAxes)

# Variable global para rastrear el último tiempo de actualización
last_update_time = time.time()

# Función para mostrar los valores al pasar el ratón
def on_mouse_move(event):
    global last_update_time
    current_time = time.time()
    
    # Verificar si ha pasado 3 segundos desde la última actualización
    if current_time - last_update_time < 3:
        return  # No hacer nada si el tiempo no ha pasado

    last_update_time = current_time  # Actualizar el último tiempo de actualización
    
    if event.inaxes == ax1:
        found = False  # Variable para rastrear si encontramos un punto cercano
        for locality, lon, lat, threshold, size, value in name_points:
            # Calcular la distancia euclidiana
            if event.xdata is not None and event.ydata is not None:
                distance = ((event.xdata - lon) ** 2 + (event.ydata - lat) ** 2) ** 0.5
                if distance < 0.2:  # Umbral de proximidad aumentado para depuración
                    # Mostrar el valor y la unidad en el subtítulo
                    subtitle_text.set_text(f'{locality}: {value} {unit_dict[selected_data]}')
                    subtitle_text.set_visible(True)
                    found = True  # Indicador de que se ha encontrado un punto
                    fig.canvas.draw_idle()
                    break  # Salir del bucle una vez que se encuentra un punto cercano

        # Si no se encontró ningún punto cercano, ocultar el subtítulo
        if not found:
            subtitle_text.set_visible(False)
            fig.canvas.draw_idle()

# Conectar el evento de movimiento del ratón
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Funciones de los botones
def set_selected_data(data_type):
    global selected_data
    selected_data = data_type
    update_scatter()

# Crear botones para seleccionar cada tipo de dato, ajustando el tamaño
button_width = 0.12
button_height = 0.05

ax_button_min = plt.axes([0.1, 0.01, button_width, button_height])
btn_min = Button(ax_button_min, 'Temp Min')
btn_min.on_clicked(lambda event: set_selected_data('temperature_min'))

ax_button_max = plt.axes([0.24, 0.01, button_width, button_height])
btn_max = Button(ax_button_max, 'Temp Max')
btn_max.on_clicked(lambda event: set_selected_data('temperature_max'))

ax_button_gusts = plt.axes([0.38, 0.01, button_width, button_height])
btn_gusts = Button(ax_button_gusts, 'Rachas Viento')
btn_gusts.on_clicked(lambda event: set_selected_data('wind_gusts'))

ax_button_speed = plt.axes([0.52, 0.01, button_width, button_height])
btn_speed = Button(ax_button_speed, 'Velocidad Viento')
btn_speed.on_clicked(lambda event: set_selected_data('wind_speed'))

ax_button_precip = plt.axes([0.66, 0.01, button_width, button_height])
btn_precip = Button(ax_button_precip, 'Precipitación')
btn_precip.on_clicked(lambda event: set_selected_data('precipitation_sum'))

# Configuración de límites originales y dibujar el gráfico inicial
update_scatter()
plt.show()
