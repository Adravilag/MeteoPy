import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.widgets import Button
from utils.utils import cargar_configuracion, cargar_traducciones, cargar_shapefile, listar_archivos_disponibles

def main(config=None, traducciones=None):
    # Cargar configuración y traducciones si no se proporcionan como argumentos
    if config is None:
        config = cargar_configuracion()
    if traducciones is None:
        traducciones = cargar_traducciones(config.get("language", "es"))

    # Configuración de variables
    label_threshold = config.get("label_threshold", 400)
    min_point_size = config.get("min_point_size", 5)
    max_point_size = config.get("max_point_size", 500)
    data_dir = os.path.abspath(config.get("data_directory", "data"))
    shapefile_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'shp', 'gadm41_ESP_4.shp'))

    # Unidad de medida
    global unit_dict
    unit_dict = {
        "temperature_min": "°C",
        "temperature_max": "°C",
        "wind_gusts": "km/h",
        "wind_speed": "km/h",
        "precipitation_sum": "mm"
    }

    # Cargar shapefile
    try:
        espana_shapefile = cargar_shapefile(shapefile_path, traducciones)
    except Exception as e:
        print(f"Error al cargar el shapefile: {e}")
        return

    # Listar archivos disponibles
    archivo_seleccionado = listar_archivos_disponibles(data_dir, traducciones, imprimir=False)
    if archivo_seleccionado is None or len(archivo_seleccionado) == 0:
        print("No se encontraron archivos válidos.")
        return

    # Selección del archivo
    if len(archivo_seleccionado) > 1:
        print("Archivos disponibles:")
        for i, archivo in enumerate(archivo_seleccionado, start=1):
            print(f"{i}. {os.path.basename(archivo)}")
        
        while True:
            try:
                seleccion_archivo = int(input("Selecciona el número del archivo a utilizar: ")) - 1
                if 0 <= seleccion_archivo < len(archivo_seleccionado):
                    archivo_seleccionado = archivo_seleccionado[seleccion_archivo]
                    break
                else:
                    print("Selección fuera de rango.")
            except ValueError:
                print("Entrada inválida.")
    else:
        archivo_seleccionado = archivo_seleccionado[0]

    print(f"Archivo seleccionado: {archivo_seleccionado}")

    try:
        excel_file = pd.ExcelFile(archivo_seleccionado)
        hojas_disponibles = excel_file.sheet_names
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_seleccionado} no se pudo encontrar.")
        return
    except Exception as e:
        print(f"Error al abrir el archivo Excel: {e}")
        return

    # Verificar qué comunidades tienen datos en las hojas
    comunidades = {
        "ANDALUCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Andalucía'],
        "VALENCIA": espana_shapefile[espana_shapefile['NAME_1'] == 'Comunidad Valenciana']
    }

    comunidades_con_datos = []
    for hoja in hojas_disponibles:
        df = pd.read_excel(archivo_seleccionado, sheet_name=hoja)
        if not df.empty and df.iloc[:, 7:11].count().sum() > 0:
            comunidades_con_datos.append(hoja)

    comunidades = {k: v for k, v in comunidades.items() if k in comunidades_con_datos}

    if not comunidades:
        print("No hay comunidades con datos disponibles.")
        return

    print(traducciones["available_autonomous_communities"])
    for i, comunidad in enumerate(comunidades.keys(), start=1):
        print(f"{i}. {comunidad}")

    # Selección de comunidad
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

    df = pd.read_excel(archivo_seleccionado, sheet_name=sheet_name)

    try:
        df[['Latitude', 'Longitude']] = df['Coordinates'].str.split(', ', expand=True).astype(float)
    except Exception as e:
        print(f"Error al procesar las coordenadas: {e}")
        return

    region_map = comunidades.get(sheet_name.upper(), None)
    if region_map is None or region_map.empty:
        print(f"Error: No se encontró la región correspondiente para '{sheet_name}' en el shapefile.")
        return

    # Crear la figura y gráficos
    fig, ax1 = plt.subplots(figsize=(10, 8))
    fig.canvas.manager.set_window_title(f"Mapa de {sheet_name} - Datos Meteorológicos")

    global selected_data
    selected_data = 'temperature_min'
    global last_locality
    last_locality = None

    scatter_points = []
    name_points = [(row['Name'], row['Longitude'], row['Latitude'], label_threshold, None, None) for _, row in df.iterrows()]

    def update_scatter():
        ax1.clear()
        region_map.boundary.plot(ax=ax1, linewidth=0.5, color='lightgray')
        ax1.set_xlabel('Longitud')
        ax1.set_ylabel('Latitud')

        data, title, cmap = get_plot_data(selected_data, df, traducciones)

        if data.isnull().all():
            print(f"No hay datos disponibles para {title}.")
            ax1.set_title(f"No hay datos para {title}.")
            fig.canvas.draw_idle()
            return

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

    def get_plot_data(selected_data, df, traducciones):
        if selected_data == 'temperature_min':
            return df['Min Temperature'], traducciones["temperature_min_title"], 'Blues'
        elif selected_data == 'temperature_max':
            return df['Max Temperature'], traducciones["temperature_max_title"], 'Reds'
        elif selected_data == 'wind_gusts':
            return df['Maximum wind gusts'], traducciones["wind_gusts_title"], 'Purples'
        elif selected_data == 'wind_speed':
            return df['Maximum wind speed'], traducciones["wind_speed_title"], 'Greens'
        elif selected_data == 'precipitation_sum':
            return df['Precipitation'], traducciones["precipitation_sum_title"], 'Blues'

    def update_labels():
        for label in ax1.texts:
            label.remove()

        for locality, lon, lat, threshold, size, value in name_points:
            if size and size >= threshold:
                ax1.text(lon, lat, locality, fontsize=8, ha='center', va='bottom', alpha=0.8)

    fig.canvas.mpl_connect('draw_event', lambda event: update_labels())

    def on_mouse_move(event):
        global last_locality
        if event.inaxes == ax1:
            for locality, lon, lat, threshold, size, value in name_points:
                distance = ((event.xdata - lon) ** 2 + (event.ydata - lat) ** 2) ** 0.5
                if distance < 0.2:
                    if locality != last_locality:
                        print(f'{locality}: {value} {unit_dict[selected_data]}')
                        last_locality = locality
                    break
            else:
                last_locality = None

    fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

    def set_selected_data(data_type):
        print(f"Botón clicado: {data_type}")
        global selected_data
        selected_data = data_type
        update_scatter()

    create_buttons(fig, traducciones, set_selected_data)

    update_scatter()
    plt.show(block=True)

# Botones de selección de datos
global_buttons = []

def create_buttons(fig, traducciones, set_selected_data):
    button_width = 0.12
    button_height = 0.05

    def on_button_click(data_type):
        print(f"Clicked button for: {data_type}")
        set_selected_data(data_type)

    data_types = ['temperature_min', 'temperature_max', 'wind_gusts', 'wind_speed', 'precipitation_sum']
    positions = [0.1, 0.24, 0.38, 0.52, 0.66]
    for data_type, pos in zip(data_types, positions):
        ax_button = plt.axes([pos, 0.01, button_width, button_height])
        # Línea modificada para aplicar traducciones
        btn = Button(ax_button, traducciones.get(f"{data_type}_button", data_type))
        btn.on_clicked(lambda event, dt=data_type: on_button_click(dt))
        global_buttons.append(btn)

if __name__ == "__main__":
    main()
