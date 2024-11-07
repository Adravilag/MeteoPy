import os
import subprocess
import sys
import argparse

def crear_entorno_virtual(nombre_entorno):
    if not os.path.exists(nombre_entorno):
        print(f"Creando el entorno virtual '{nombre_entorno}'...")
        subprocess.check_call([sys.executable, '-m', 'venv', nombre_entorno])
    else:
        print(f"El entorno virtual '{nombre_entorno}' ya existe.")

def activar_entorno_virtual(nombre_entorno):
    activate_script = os.path.join(nombre_entorno, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(nombre_entorno, 'bin', 'activate')
    if os.path.exists(activate_script):
        print(f"Activando el entorno virtual...")
        os.system(f'{activate_script}' if os.name != 'nt' else f'call {activate_script}')
        print(f"El entorno virtual '{nombre_entorno}' está activado.")
    else:
        print("Error: No se pudo activar el entorno virtual.")

def instalar_dependencias(nombre_entorno):
    pip_path = os.path.join(nombre_entorno, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(nombre_entorno, 'bin', 'pip')
    if os.path.exists(pip_path):
        print("Instalando dependencias...")
        if os.path.exists('requirements.txt'):
            subprocess.check_call([pip_path, 'install', '-r', 'requirements.txt'])
            print("Dependencias instaladas correctamente.")
        else:
            print("No se encontró el archivo requirements.txt.")
    else:
        print("Error: No se pudo encontrar pip en el entorno virtual.")

def censurar_token(key_value):
    if '=' in key_value:
        key, token = key_value.split('=', 1)  # Divide solo en el primer '='
    else:
        key, token = key_value, ''
    if token:
        return f"{key}={token[:4]}****{token[-4:]}"  # Censura solo una parte del token
    return key_value

def limpiar_duplicados_env(ruta_env):
    lineas_unicas = {}
    if os.path.exists(ruta_env):
        with open(ruta_env, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if '=' in linea and not linea.startswith('='):
                    clave, valor = linea.split('=', 1)
                    if clave not in lineas_unicas:
                        lineas_unicas[clave] = f"{clave}={valor}"

    with open(ruta_env, 'w') as archivo:
        for linea in lineas_unicas.values():
            archivo.write(linea + '\n')

def actualizar_env():
    env_path = '.env'
    limpiar_duplicados_env(env_path)
    found_vars = {}

    # Leer el archivo .env existente
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                key = line.split('=')[0].strip()
                found_vars[key] = line.strip()  # Guardar la línea completa

    # Solicitar al usuario nuevos valores para MongoDB
    mongodb_username = input("Introduce el nombre de usuario de MongoDB: ")
    mongodb_password = input("Introduce la contraseña de MongoDB: ")
    mongodb_appname = input("Introduce el nombre de la aplicación (appName): ")
    mongodb_database = input("Introduce el nombre de la base de datos: ")

    # Crear la URI de MongoDB
    mongodb_uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@cluster0.4v8ri.mongodb.net/{mongodb_database}?retryWrites=true&w=majority&appName={mongodb_appname}"

    # Actualizar las variables encontradas o añadir nuevas
    current_github_token = found_vars.get('GITHUB_TOKEN', None)
    if current_github_token:
        github_token = input(f"Introduce el GITHUB_TOKEN (actual: {censurar_token(current_github_token)}, dejar en blanco para mantener): ") or current_github_token
    else:
        github_token = input("Introduce el GITHUB_TOKEN: ")

    found_vars['GITHUB_TOKEN'] = github_token
    found_vars['TEMPLATE_PATH'] = input(f"Introduce la TEMPLATE_PATH (actual: {found_vars.get('TEMPLATE_PATH', 'No establecido')}, dejar en blanco para mantener): ") or found_vars.get('TEMPLATE_PATH', os.path.join(os.getcwd(), 'config', 'templates', 'MeteoData_Template.xlsm'))
    found_vars['MONGODB_URI'] = mongodb_uri
    found_vars['MONGODB_DATABASE'] = mongodb_database
    found_vars['MONGODB_COLLECTION'] = input(f"Introduce el MONGODB_COLLECTION (actual: {found_vars.get('MONGODB_COLLECTION', 'No establecido')}, dejar en blanco para mantener): ") or found_vars.get('MONGODB_COLLECTION', '')

    # Escribir el archivo .env actualizado
    with open(env_path, 'w') as f:
        for key, value in found_vars.items():
            if value:
                f.write(f"{key}={value}\n")

    print(f"Variables de entorno actualizadas en {env_path}.")

def main():
    parser = argparse.ArgumentParser(description="Configuración del entorno de trabajo.")
    parser.add_argument('--crear', action='store_true', help="Crea el entorno virtual.")
    parser.add_argument('--activar', action='store_true', help="Activa el entorno virtual.")
    parser.add_argument('--instalar', action='store_true', help="Instala las dependencias.")
    parser.add_argument('--actualizar-env', action='store_true', help="Actualiza el archivo .env.")
    args = parser.parse_args()

    nombre_entorno = 'venv'

    if args.crear:
        crear_entorno_virtual(nombre_entorno)
    if args.activar:
        activar_entorno_virtual(nombre_entorno)
    if args.instalar:
        instalar_dependencias(nombre_entorno)
    if args.actualizar_env:
        actualizar_env()

if __name__ == "__main__":
    main()
