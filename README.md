
# MeteoWave

**MeteoWave** es una aplicación de Python diseñada para visualizar datos meteorológicos en un mapa interactivo utilizando archivos SHP. Permite visualizar la temperatura media en áreas geográficas como Andalucía y otras regiones de España, basándose en datos obtenidos de la API de Open Meteo.

## Características

- **Visualización interactiva** de temperaturas en mapas geográficos, con tamaños y colores de puntos que varían según la temperatura.
- **Historial de datos meteorológicos**: Guarda datos en función de la fecha, creando un registro histórico en archivos Excel.
- **Detalles interactivos**: Muestra valores específicos al pasar el ratón sobre diferentes áreas del mapa.
- **Configuración avanzada**: Un archivo `config.json` permite personalizar aspectos de visualización y parámetros de la API.
- **Mapas detallados**: Muestra nombres de localidades cuando se hace zoom o cuando el tamaño del área alcanza un cierto umbral.

## Estructura del Proyecto

- **bin/**: Contiene scripts `.bat` para automatizar tareas, como ejecutar pruebas o activar el entorno virtual.
- **config/**: Contiene el archivo `config.json` para configuración general, plantillas de Excel y archivos SHP.
- **data/**: Almacena datos generados (organizados por año y mes) para crear un histórico.
- **locales/**: Archivos de traducción en formato JSON para soporte multilingüe (`es.json`, `en.json`).
- **src/**: Contiene el código fuente de la aplicación, organizado en subdirectorios `data_processing` y `visualization`.
- **tests/**: Contiene las pruebas unitarias para asegurar la correcta funcionalidad del proyecto.
- **venv/**: Entorno virtual para administrar dependencias de Python.

## Instalación

### 1. Clonar el Repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/usuario/MeteoWave.git
cd MeteoWave
```

### 2. Configurar el Entorno de Desarrollo en Windows

Ejecuta el siguiente script para crear y configurar el entorno virtual, instalar dependencias y generar el archivo `.env`:

```bash
bin\setup.bat
```

Este script realizará los siguientes pasos automáticamente:
1. Creará un entorno virtual en la carpeta `venv`.
2. Instalará las dependencias necesarias desde `requirements.txt`.
3. Generará un archivo `.env` con un campo para el token de la API (`GITHUB_TOKEN`).

### 3. Configuración Manual (Opcional)

Si prefieres una configuración manual, sigue estos pasos:

1. Crea y activa el entorno virtual:
   ```bash
   python -m venv venv
   ```
   - En **Windows**: `venv\Scripts\activate`
   - En **macOS/Linux**: `source venv/bin/activate`

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz del proyecto y añade tu token de la API:
   ```env
   GITHUB_TOKEN=tu_token_aqui
   ```

## Configuración de `config.json`

La aplicación **MeteoWave** utiliza un archivo `config.json` para definir parámetros clave de visualización y configuración de la API. Asegúrate de revisar o modificar este archivo según tus necesidades.

Ejemplo de `config.json`:

```json
{
    "language": "es",
    "base_size": 10,
    "max_point_size": 500,
    "min_point_size": 5,
    "label_threshold": 400,
    "default_selected_data": "temperature_mean",
    "map_xlim": [-7.6, -1.5],
    "map_ylim": [35.8, 39],
    "shapefile_path": "config/shp/gadm41_ESP_4.shp"
}
```

### Parámetros Importantes

- **language**: Idioma para los mensajes en la aplicación (`es` para español, `en` para inglés).
- **base_size**: Tamaño base de los puntos en el mapa.
- **max_point_size** y **min_point_size**: Tamaños máximo y mínimo de los puntos en función de la temperatura.
- **label_threshold**: Controla cuándo aparecen etiquetas en el mapa.
- **map_xlim** y **map_ylim**: Coordenadas límite para la visualización en el mapa.
- **shapefile_path**: Ruta del archivo SHP que define la región en el mapa.

### Archivos `.bat` para Ejecución

**MeteoWave** incluye archivos `.bat` en el directorio `bin` para facilitar la ejecución y pruebas de los scripts principales:

- **run_metPy.bat**: Ejecuta el script `metPy.py` en `src`, que se encarga de cargar y visualizar datos meteorológicos.
- **run_geoPy.bat**: Ejecuta el script `geoPy.py` en `src`, para manejar funcionalidades adicionales de visualización geográfica.
- **run_tests.bat**: Ejecuta todas las pruebas unitarias en el directorio `tests` de manera secuencial.

### Ejecución de la Aplicación

Para ejecutar el script principal desde la línea de comandos:

```bash
python src/metPy.py
```

O bien, usa el archivo `.bat` correspondiente:

```batch
bin\run_metPy.bat
```

Este comando:

1. Carga los datos meteorológicos de Open Meteo.
2. Lee las coordenadas desde un archivo de Excel.
3. Muestra los datos en un mapa interactivo utilizando archivos SHP.

## Ejecución de Pruebas

Para ejecutar todas las pruebas unitarias en el directorio `tests`, usa:

```batch
bin\run_tests.bat
```

Cada prueba se ejecutará individualmente, mostrando los resultados antes de limpiar la pantalla. Puedes pausar entre cada prueba para revisar los resultados.

## Uso de la Aplicación

1. Ejecuta `metPy.py` usando `python src/metPy.py` o `run_metPy.bat`.
2. Selecciona una fecha y región. La aplicación descargará los datos meteorológicos y los mostrará en el mapa interactivo.
3. Los datos se guardarán en un archivo Excel (`MeteoData_YYYYMMDD.xlsx`) en el directorio `data`, permitiendo la creación de un histórico.

## Funcionalidades de Traducción

**MeteoWave** es compatible con varios idiomas, definidos en `locales/en.json` y `locales/es.json`. Puedes cambiar el idioma en el archivo `config.json` mediante el parámetro `language`. 

Ejemplo:
```json
"language": "en"
```

Esto hará que todos los mensajes de la aplicación se muestren en inglés.

## Contribuciones y Créditos

**MeteoWave** fue desarrollado con la colaboración de **ChatGPT** de OpenAI, permitiendo completar el proyecto en un tiempo récord. La estructura y diseño del proyecto están orientados a una fácil expansión y mejora continua.

### Motivación

El proyecto **MeteoWave** busca aplicar conocimientos de manejo de datos geoespaciales y visualización en Python, con el objetivo de crear una herramienta práctica y visual para la monitorización de datos meteorológicos.



## CI/CD e Integración Continua

La aplicación **MeteoWave** está configurada para utilizar un flujo de integración continua (CI/CD) a través de GitHub Actions. Esto asegura que cada cambio en el código desencadene un proceso de pruebas automáticas, verificando que los módulos y funciones principales se comporten de acuerdo a lo esperado.

### Configuración de GitHub Actions

Cada vez que se realiza un `push` o se abre un `pull request` en la rama principal, GitHub Actions ejecuta automáticamente el flujo de CI/CD configurado. Esto incluye:
- Instalación de dependencias.
- Configuración del entorno de pruebas.
- Ejecución de pruebas unitarias para validar la funcionalidad de los módulos principales.

### Script de Configuración Inicial

El proyecto incluye un script `setup.bat` que permite automatizar la configuración inicial del entorno. Este script realiza las siguientes tareas:
- Crea y activa un entorno virtual en `venv`.
- Instala las dependencias listadas en `requirements.txt`.
- Crea un archivo `.env` con variables de entorno necesarias para la API y otros servicios externos.

### Ejecución de Pruebas y Automatización

Para ejecutar las pruebas de manera local, se proporciona un script `run_tests.bat`. Este script recorre los archivos de prueba en el directorio `tests/` y ejecuta cada prueba individualmente, pausando entre pruebas para permitir la revisión de los resultados.

Ejemplo de uso en la línea de comandos:

```bash
# En la raíz del proyecto
./run_tests.bat
```

La configuración de GitHub Actions y estos scripts aseguran una integración continua efectiva, ayudando a mantener la estabilidad del código y reducir errores.

