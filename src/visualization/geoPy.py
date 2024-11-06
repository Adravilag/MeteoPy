import os
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.widgets import Button
from datetime import datetime

def cls():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Cargar configuración desde archivo JSON
def cargar_configuracion():
    """Carga la configuración desde el archivo config.json."""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.json')
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: El archivo config.json no se encuentra en la ruta especificada.")
        exit()
    except json.JSONDecodeError:
        print("Error: El archivo config.json tiene un formato JSON no válido.")
        exit()

def cargar_traducciones(idioma="es"):
    """Carga el archivo de traducciones en el idioma especificado."""
    locales_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'locales')
    idioma_path = os.path.join(locales_dir, f"{idioma}.json")
    try:
        with open(idioma_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Archivo de idioma '{idioma}.json' no encontrado. Usando idioma predeterminado (español).")
        with open(os.path.join(locales_dir, 'es.json'), 'r', encoding='utf-8') as f:
            return json.load(f)

# Inicializar parámetros desde la configuración
config = cargar_configuracion()
traducciones = cargar_traducciones(config.get("language", "es"))

# Variables de configuración
label_threshold = config.get("label_threshold", 400)
min_point_size = config.get("min_point_size", 5)
max_point_size = config.get("max_point_size", 500)
data_dir = config.get("data_directory", "data")
shapefile_path = config.get("shapefile_path", "config/shp/gadm41_ESP_4.shp")

# Unidad de medida para cada tipo de dato
unit_dict = {
    "temperature_min": "°C",
    "temperature_max": "°C",
    "wind_gusts": "km/h",
    "wind_speed": "km/h",
    "precipitation_sum": "mm"
}

# Verificar si el archivo shapefile existe
if not os.path.exists(shapefile_path):
    print(f"Error: No se encontró el archivo de shapes en '{shapefile_path}'.")
    exit()

# Cargar el shapefile de España
try:
    espana_shapefile = gpd.read_file(shapefile_path)
except Exception as e:
    print(traducciones["error_loading_shapefile"])
    print(f"Detalles del error: {e}")
    exit()

# Función para listar archivos disponibles en el directorio de datos
def listar_archivos_disponibles():
    directorio_completo = os.path.abspath(data_dir)
    print(f"Buscando archivos en: {directorio_completo}")
    
    archivos = []
    
    for root, dirs, files in os.walk(directorio_completo):
        for file in files:
            if file.startswith("MeteoData_") and (file.endswith(".xlsx") or file.endswith(".xlsm")):
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

# Cargar el archivo Excel seleccionado y listar las hojas disponibles
archivo_seleccionado = listar_archivos_disponibles()
if archivo_seleccionado is None:
    exit()

try:
    excel_file = pd.ExcelFile(archivo_seleccionado)
    hojas_disponibles = excel_file.sheet_names
except FileNotFoundError:
    print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
    exit()

# Filtrar las comunidades autónomas que tienen datos disponibles
comunidades_con_datos = []
comunidades = { 
    "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Andalucía'],
    "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']
}

for hoja in hojas_disponibles:
    df = pd.read_excel(archivo_seleccionado, sheet_name=hoja)
    
    # Verificar que el DataFrame no esté vacío y que contenga datos en las columnas correspondientes
    # Usamos los índices de columna 7 a 10 (equivalente a H, I, J, K en Excel)
    if not df.empty and df.iloc[:, 7:11].count().sum() > 0:
        comunidades_con_datos.append(hoja)

# Filtrar las comunidades según los datos disponibles
comunidades = {k: v for k, v in comunidades.items() if k in comunidades_con_datos}

print(traducciones["available_autonomous_communities"])
for i, comunidad in enumerate(comunidades.keys(), start=1):
    print(f"{i}. {comunidad}")

# Permitir que el usuario seleccione la hoja (comunidad autónoma)
while True:
    try:
        seleccion_hoja = int(input(traducciones["select_community"])) - 1
        if 0 <= seleccion_hoja < len(comunidades):
            sheet_name = list(comunidades.keys())[seleccion_hoja]
            break
        else:
            print(traducciones["selection_out_of_range"])
    except ValueError:
        print(traducciones["invalid_input"])

# Cargar los datos desde la hoja seleccionada
df = pd.read_excel(archivo_seleccionado, sheet_name=sheet_name)

# Asegúrate de que las columnas de coordenadas están en el formato correcto
df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(', ', expand=True).astype(float)

# Seleccionar la región en el mapa según la comunidad seleccionada
region_map = comunidades.get(sheet_name.upper(), None)
if region_map is None or region_map.empty:
    print(f"Error: No se encontró la región correspondiente para '{sheet_name}' en el shapefile.")
    exit()

# Crear la figura y gráficos de datos meteorológicos
fig, ax1 = plt.subplots(figsize=(10, 8))
fig.canvas.manager.set_window_title(f"Mapa de {sheet_name} - Datos Meteorológicos")

# Variable global para almacenar la selección actual
selected_data = 'temperature_min'

scatter_points = []
name_points = [(row['Name'], row['Longitude'], row['Latitude'], label_threshold, None, None) for _, row in df.iterrows()]

# Función de actualización para el gráfico
def update_scatter():
    global min_point_size, max_point_size
    ax1.clear()
    region_map.boundary.plot(ax=ax1, linewidth=0.5, color='lightgray')

    ax1.set_xlabel('Longitud')
    ax1.set_ylabel('Latitud')
    
    if selected_data == 'temperature_min':
        data = df['Min Temperature']
        title = traducciones["temperature_min_title"]
        cmap = 'Blues'
    elif selected_data == 'temperature_max':
        data = df['Max Temperature']
        title = traducciones["temperature_max_title"]
        cmap = 'Reds'
    elif selected_data == 'wind_gusts':
        data = df['Maximum wind gusts']
        title = traducciones["wind_gusts_title"]
        cmap = 'Purples'
    elif selected_data == 'wind_speed':
        data = df['Maximum wind speed']
        title = traducciones["wind_speed_title"]
        cmap = 'Greens'
    elif selected_data == 'precipitation_sum':
        data = df['Precipitation']
        title = traducciones["precipitation_sum_title"]
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
    
    ax1.set_title(f'{sheet_name} - {title}')
    update_labels()
    fig.canvas.draw_idle()

# Función para actualizar etiquetas de nombres
def update_labels():
    for label in ax1.texts:
        label.remove()
    
    for locality, lon, lat, threshold, size, value in name_points:
        if size and size >= threshold:
            ax1.text(lon, lat, locality, fontsize=8, ha='center', va='bottom', alpha=0.8)

fig.canvas.mpl_connect('draw_event', lambda event: update_labels())

# Conectar el evento de movimiento del ratón
def on_mouse_move(event):
    global last_locality  # Hacer que la variable sea global
    if event.inaxes == ax1:
        for locality, lon, lat, threshold, size, value in name_points:
            distance = ((event.xdata - lon) ** 2 + (event.ydata - lat) ** 2) ** 0.5
            if distance < 0.2:
                # Solo mostrar la información si es un nuevo punto
                if locality != last_locality:
                    print(f'{locality}: {value} {unit_dict[selected_data]}')  # Muestra el valor en la consola
                    last_locality = locality  # Actualiza el último punto mostrado
                break
        else:
            # Reiniciar el último punto si no se está sobre ningún punto
            last_locality = None

# Conectar el evento de movimiento del ratón
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

# Función para establecer los datos seleccionados
def set_selected_data(data_type):
    global selected_data
    selected_data = data_type
    update_scatter()  # Actualiza el gráfico con los nuevos datos

# Botones para seleccionar cada tipo de dato
button_width = 0.12
button_height = 0.05

ax_button_min = plt.axes([0.1, 0.01, button_width, button_height])
btn_min = Button(ax_button_min, traducciones["temp_min_button"])  # Usar traducción
btn_min.on_clicked(lambda event: set_selected_data('temperature_min'))

ax_button_max = plt.axes([0.24, 0.01, button_width, button_height])
btn_max = Button(ax_button_max, traducciones["temp_max_button"])  # Usar traducción
btn_max.on_clicked(lambda event: set_selected_data('temperature_max'))

ax_button_gusts = plt.axes([0.38, 0.01, button_width, button_height])
btn_gusts = Button(ax_button_gusts, traducciones["wind_gusts_button"])  # Usar traducción
btn_gusts.on_clicked(lambda event: set_selected_data('wind_gusts'))

ax_button_speed = plt.axes([0.52, 0.01, button_width, button_height])
btn_speed = Button(ax_button_speed, traducciones["wind_speed_button"])  # Usar traducción
btn_speed.on_clicked(lambda event: set_selected_data('wind_speed'))

ax_button_precip = plt.axes([0.66, 0.01, button_width, button_height])
btn_precip = Button(ax_button_precip, traducciones["precipitation_sum_button"])  # Usar traducción
btn_precip.on_clicked(lambda event: set_selected_data('precipitation_sum'))

# Configuración de límites originales y dibujar el gráfico inicial
update_scatter()
plt.show()
