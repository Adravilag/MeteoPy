# app_runner.py
import sys
import os

# Definir el directorio raíz del proyecto y el archivo de configuración
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
config_path = os.path.join(project_root, 'config', 'config.json')

# Agregar el directorio `src` a `sys.path`
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.utils import cargar_configuracion, cargar_traducciones
from visualization.geoPy import main as run_geo
from data_processing.metPy import main as run_met

print("src_path:", src_path)
print("config_path:", config_path)

# Cargar configuración y traducciones
try:
    config = cargar_configuracion(config_path)
    language = config.get("language", "en")
    traducciones = cargar_traducciones(language)
except Exception as e:
    print(f"Error cargando configuración o traducciones: {e}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print(traducciones["provide_argument"])
        return

    arg = sys.argv[1].lower()
    if arg == 'geo':
        print(traducciones["running_geo"])
        run_geo(config, traducciones)
    elif arg == 'met':
        print(traducciones["running_met"])
        run_met(config, traducciones)
    else:
        print(traducciones["invalid_argument"])

if __name__ == "__main__":
    main()
