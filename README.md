
# MeteoPy

**MeteoPy** es una aplicación de Python que utiliza archivos SHP para visualizar la temperatura media mediante áreas coloreadas en Andalucía y otras regiones de España. Los datos meteorológicos se obtienen de la API de Open Meteo, y la aplicación permite generar históricos y visualizar datos en un mapa interactivo.

## Características

- **Visualización interactiva** de temperatura por regiones, con tamaños y colores que varían según la temperatura.
- **Datos meteorológicos históricos**: permite guardar los datos de acuerdo con la fecha, generando un historial.
- **Información detallada**: muestra los valores y magnitudes al pasar el ratón sobre áreas del mapa.
- **Parámetros configurables**: incluye un archivo `config.json` para personalizar aspectos de visualización y límites de mapas.
- **Mapas detallados de localidades**: los nombres de localidades aparecen al hacer zoom o cuando el área alcanza un tamaño específico.

## Instalación

### 1. Clonar el Repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/usuario/MeteoPy.git
cd MeteoPy
```

### 2. Crear y Activar un Entorno Virtual (Opcional)

Para aislar las dependencias del proyecto, es recomendable usar un entorno virtual:

```bash
python -m venv venv
```

Activa el entorno virtual:

- **En Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **En macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 3. Instalar Dependencias

Instala todas las dependencias requeridas listadas en el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Si `requirements.txt` no está creado aún, puedes instalar manualmente las bibliotecas y luego generarlo:

```bash
pip install pandas geopandas matplotlib requests openpyxl
pip freeze > requirements.txt
```

## Configuración

La aplicación **MeteoPy** utiliza un archivo `config.json` para definir parámetros clave, incluyendo las coordenadas de visualización, el tamaño de puntos y límites de la región en el mapa. Asegúrate de revisar o modificar este archivo según tus necesidades.

### Archivos de Configuración

- **Ruta del archivo de configuración**: `config/config.json`
- **Plantilla de Excel**: `config/MeteoData.xlsx` (para organizar los datos meteorológicos)
- **Archivos SHP**: los archivos de shape (.shp) están en `config/shp/`, lo que permite definir las áreas geográficas.

### Parámetros en `config.json`

El archivo `config.json` contiene los siguientes parámetros:

```json
{
    "base_size":  10,
    "max_point_size":  500,
    "min_point_size":  5,
    "label_threshold":  400,
    "default_selected_data":  "temperature_mean",
    "map_xlim":  [
                     -7.6,
                     -1.5
                 ],
    "map_ylim":  [
                     35.8,
                     39
                 ],
    "shapefile_path":  "config/shp/gadm41_ESP_4.shp"
}
```

#### Descripción de los Parámetros

- **version**: Número de versión de la aplicación.
- **base_size**: Tamaño base de los puntos en el mapa.
- **max_point_size** y **min_point_size**: Tamaño máximo y mínimo de los puntos en función de la temperatura.
- **label_threshold**: Controla cuándo aparecen etiquetas en el mapa.
- **default_selected_data**: Región seleccionada al iniciar (por defecto: Andalucía).
- **map_xlim** y **map_ylim**: Coordenadas límite para la visualización en el mapa.
- **shapefile_path**: Ruta del archivo SHP que define la región en el mapa.

### Cómo Personalizar las Configuraciones

1. Abre el archivo `config/config.json` en un editor de texto.
2. Cambia los valores de los parámetros según tus necesidades. Por ejemplo, puedes cambiar `default_selected_data` para centrarte en otra región o ajustar `max_point_size` para cambiar el tamaño máximo de los puntos en el mapa.
3. Guarda los cambios y ejecuta la aplicación nuevamente para aplicar la configuración actualizada.

## Ejecución de la Aplicación

### Ejecución desde la Línea de Comandos

Para ejecutar la aplicación, asegúrate de estar en la carpeta raíz del proyecto y usa el siguiente comando:

```bash
python src/metPy.py
```

Este script:

- Carga los datos meteorológicos de Open Meteo.
- Lee las coordenadas desde un archivo de Excel.
- Muestra los datos en un mapa interactivo utilizando archivos SHP.

### Uso de Archivos `.bat` para Ejecutar Scripts

Si prefieres usar archivos `.bat` para facilitar la ejecución, crea los siguientes archivos en la raíz del proyecto:

- **run_metPy.bat**:

  ```batch
  @echo off
  python src/metPy.py
  pause
  ```

- **run_geoPy.bat**:

  ```batch
  @echo off
  python src/geoPy.py
  pause
  ```

Al hacer doble clic en estos archivos `.bat`, puedes ejecutar los scripts sin necesidad de escribir el comando en la terminal.

## Ejemplo de Uso

1. Ejecuta `metPy.py` usando `python src/metPy.py` o `run_metPy.bat`.
2. Selecciona una fecha y región, y la aplicación descargará los datos meteorológicos.
3. La visualización interactiva muestra los valores de temperatura en el mapa. Las áreas cambian de tamaño y color según la temperatura en cada ubicación.
4. Guarda los datos generados en el archivo de Excel `MeteoData_YYYYMMDD.xlsx` en el directorio `data`, permitiendo generar un histórico.

## Comentario del Desarrollador

El propósito de **MeteoPy** es permitir la recopilación de datos meteorológicos y su visualización en un mapa interactivo. Este proyecto es una oportunidad para aplicar conocimientos en APIs REST, manejo de datos geoespaciales y visualización en Python. Las características principales del mapa incluyen la variación del tamaño y color de las áreas según la temperatura, y la aparición de nombres de localidades al hacer zoom."# MeteoPy" 
"# MeteoPy" 
