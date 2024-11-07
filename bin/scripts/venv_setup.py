import os
import subprocess
import sys

def crear_entorno_virtual(nombre_entorno):
    """Crea un entorno virtual si no existe."""
    if not os.path.exists(nombre_entorno):
        print(f"Creando el entorno virtual '{nombre_entorno}'...")
        subprocess.check_call([sys.executable, '-m', 'venv', nombre_entorno])
    else:
        print(f"El entorno virtual '{nombre_entorno}' ya existe.")

def activar_entorno_virtual(nombre_entorno):
    """Activa el entorno virtual."""
    activate_script = os.path.join(nombre_entorno, 'Scripts', 'activate')
    print(f"Activando el entorno virtual...")
    os.system(f'call {activate_script}')
    print(f"El entorno virtual '{nombre_entorno}' está activado.")

def instalar_paquetes(nombre_entorno, paquetes):
    """Instala paquetes en el entorno virtual."""
    if paquetes:  # Solo intenta instalar si hay paquetes
        print(f"Instalando paquetes: {', '.join(paquetes)}...")
        pip_path = os.path.join(nombre_entorno, 'Scripts', 'pip')
        for paquete in paquetes:
            subprocess.check_call([pip_path, 'install', paquete])
    else:
        print("No se especificaron paquetes para instalar.")

def main():
    nombre_entorno = 'venv'  # Nombre del entorno virtual

    crear_entorno_virtual(nombre_entorno)
    activar_entorno_virtual(nombre_entorno)

    # Pedir al usuario que ingrese los nombres de los paquetes
    paquetes_input = input("Introduce los nombres de los paquetes a instalar (separados por comas): ")
    paquetes_a_instalar = [paquete.strip() for paquete in paquetes_input.split(',')]  # Limpia espacios

    instalar_paquetes(nombre_entorno, paquetes_a_instalar)

if __name__ == "__main__":
    main()
